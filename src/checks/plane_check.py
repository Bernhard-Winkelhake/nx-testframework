
from typing import List

from check_result import CheckResult, Severity, Status
from checks.base import BaseCheck


class DatumPlaneLayerCheck(BaseCheck):
    rule_id = "DATUM_PLANE_LAYER"
    name = "Datum plane layer"
    config_key = "enable_plane_check"

    def run(self, work_part, config: dict) -> List[CheckResult]:
        expected = config.get("layers", {}).get("plane", 62)
        results = []

        # Nur echte, eigenständige DATUM_PLANE-Features prüfen.
        # DatumPlanes, die Bestandteil eines DATUM_CSYS sind,
        # werden dadurch nicht erfasst.
        datum_plane_features = [
            feature
            for feature in work_part.Features
            if getattr(feature, "FeatureType", "") == "DATUM_PLANE"
        ]

        if not datum_plane_features:
            return [
                CheckResult(
                    self.rule_id,
                    self.name,
                    Status.PASSED,
                    Severity.INFO,
                    "No standalone datum planes found.",
                )
            ]

        for feature in datum_plane_features:
            feature_name = (
                getattr(feature, "Name", None)
                or "Unnamed Datum Plane"
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
                        f"Could not read Datum Plane entities: {exc}",
                        feature_name,
                        "DatumPlane",
                    )
                )
                continue

            # Layer steckt bei NX häufig auf dem erzeugten
            # DisplayableObject und nicht auf dem Feature selbst.
            displayable_entities = [
                entity
                for entity in entities
                if getattr(entity, "Layer", None) is not None
            ]

            if not displayable_entities:
                results.append(
                    CheckResult(
                        self.rule_id,
                        self.name,
                        Status.FAILED,
                        Severity.ERROR,
                        "Datum Plane has no displayable entity with a layer.",
                        feature_name,
                        "DatumPlane",
                    )
                )
                continue

            wrong_layers = [
                entity.Layer
                for entity in displayable_entities
                if entity.Layer != expected
            ]

            if not wrong_layers:
                results.append(
                    CheckResult(
                        self.rule_id,
                        self.name,
                        Status.PASSED,
                        Severity.INFO,
                        f"Datum Plane '{feature_name}' is on layer {expected}.",
                        feature_name,
                        "DatumPlane",
                    )
                )
            else:
                found = ", ".join(
                    str(layer)
                    for layer in sorted(set(wrong_layers))
                )

                results.append(
                    CheckResult(
                        self.rule_id,
                        self.name,
                        Status.FAILED,
                        Severity.ERROR,
                        f"Datum Plane '{feature_name}' must be on layer "
                        f"{expected}. Found layer {found}.",
                        feature_name,
                        "DatumPlane",
                    )
                )

        return results
