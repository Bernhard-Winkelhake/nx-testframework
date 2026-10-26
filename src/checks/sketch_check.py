
from typing import List

from check_result import CheckResult, Severity, Status
from checks.base import BaseCheck


class SketchLayerCheck(BaseCheck):
    rule_id = "SKETCH_LAYER"
    name = "Sketch layer"
    config_key = "enable_sketch_check"

    def run(self, work_part, config: dict) -> List[CheckResult]:
        expected = config.get("layers", {}).get("sketch", 21)
        results = []

        # Nur echte SKETCH-Features aus der Modellhistorie.
        sketch_features = [
            feature
            for feature in work_part.Features
            if getattr(feature, "FeatureType", "").upper() == "SKETCH"
        ]

        if not sketch_features:
            return [
                CheckResult(
                    self.rule_id,
                    self.name,
                    Status.PASSED,
                    Severity.INFO,
                    "No sketches found.",
                )
            ]

        for index, feature in enumerate(sketch_features, start=1):
            feature_name = (
                getattr(feature, "Name", None)
                or f"Sketch {index}"
            )

            try:
                entities = list(feature.GetEntities())
            except Exception as exc:
                results.append(
                    CheckResult(
                        self.rule_id,
                        self.name,
                        Status.FAILED,
                        Severity.ERROR,
                        f"Could not read Sketch entities: {exc}",
                        feature_name,
                        "Sketch",
                    )
                )
                continue

            # Nur Objekte betrachten, die tatsächlich
            # eine Layer-Information besitzen.
            entities_with_layer = [
                entity
                for entity in entities
                if getattr(entity, "Layer", None) is not None
            ]

            if not entities_with_layer:
                results.append(
                    CheckResult(
                        self.rule_id,
                        self.name,
                        Status.FAILED,
                        Severity.ERROR,
                        "Sketch contains no entities with layer information.",
                        feature_name,
                        "Sketch",
                    )
                )
                continue

            wrong_entities = [
                entity
                for entity in entities_with_layer
                if entity.Layer != expected
            ]

            if not wrong_entities:
                results.append(
                    CheckResult(
                        self.rule_id,
                        self.name,
                        Status.PASSED,
                        Severity.INFO,
                        f"Sketch '{feature_name}' is completely on layer {expected}.",
                        feature_name,
                        "Sketch",
                    )
                )
                continue

            wrong_layers = sorted({
                entity.Layer
                for entity in wrong_entities
            })

            found = ", ".join(
                str(layer)
                for layer in wrong_layers
            )

            results.append(
                CheckResult(
                    self.rule_id,
                    self.name,
                    Status.FAILED,
                    Severity.ERROR,
                    f"Sketch '{feature_name}' must be on layer "
                    f"{expected}. Found layer {found}.",
                    feature_name,
                    "Sketch",
                )
            )

        return results


def assign_sketches_to_layer(work_part=None, layer=None):
    """
    Legacy fixer.
    Not called by CheckRunner.
    """
    if work_part is None:
        import NXOpen
        work_part = NXOpen.Session.GetSession().Parts.Work

    if layer is None:
        from utils.config_loader import load_config
        layer = load_config().get(
            "layers", {}
        ).get("sketch", 21)

    for feature in work_part.Features:
        if getattr(feature, "FeatureType", "").upper() != "SKETCH":
            continue

        try:
            entities = list(feature.GetEntities())
        except Exception:
            continue

        entities_with_layer = [
            entity
            for entity in entities
            if getattr(entity, "Layer", None) is not None
        ]

        if entities_with_layer:
            work_part.Layers.MoveDisplayableObjects(
                layer,
                entities_with_layer
            )
