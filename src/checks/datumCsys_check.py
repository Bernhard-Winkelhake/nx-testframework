
from typing import List

from check_result import CheckResult, Severity, Status
from checks.base import BaseCheck


class DatumCsysLayerCheck(BaseCheck):
    rule_id = "DATUM_CSYS_LAYER"
    name = "Datum CSYS layer"
    config_key = "enable_csys_check"

    def run(self, work_part, config: dict) -> List[CheckResult]:
        expected = config.get("layers", {}).get("csys", 61)
        results = []

        datum_csys_features = []

        for feature in work_part.Features:
            if getattr(feature, "FeatureType", "") != "DATUM_CSYS":
                continue

            name = (getattr(feature, "Name", None) or "").strip()

            # Interne / unbenannte DATUM_CSYS-Features ignorieren.
            if not name:
                continue

            datum_csys_features.append(feature)

        if not datum_csys_features:
            return [
                CheckResult(
                    self.rule_id,
                    self.name,
                    Status.PASSED,
                    Severity.INFO,
                    "No named datum coordinate systems found.",
                )
            ]

        for feature in datum_csys_features:
            feature_name = feature.Name.strip()

            try:
                entities = list(feature.GetEntities())
            except Exception as exc:
                results.append(
                    CheckResult(
                        self.rule_id,
                        self.name,
                        Status.FAILED,
                        Severity.ERROR,
                        f"Could not read Datum CSYS entities: {exc}",
                        feature_name,
                        "DatumCSYS",
                    )
                )
                continue

            wrong_entities = []

            for entity in entities:
                layer = getattr(entity, "Layer", None)

                # Nicht darstellbare Objekte haben keinen Layer.
                if layer is None:
                    continue

                if layer != expected:
                    wrong_entities.append(
                        (type(entity).__name__, layer)
                    )

            if wrong_entities:
                details = ", ".join(
                    f"{entity_type}: layer {layer}"
                    for entity_type, layer in wrong_entities
                )

                results.append(
                    CheckResult(
                        self.rule_id,
                        self.name,
                        Status.FAILED,
                        Severity.ERROR,
                        f"Datum CSYS '{feature_name}' must be on "
                        f"layer {expected}. Wrong entities: {details}.",
                        feature_name,
                        "DatumCSYS",
                    )
                )
            else:
                results.append(
                    CheckResult(
                        self.rule_id,
                        self.name,
                        Status.PASSED,
                        Severity.INFO,
                        f"Datum CSYS '{feature_name}' is completely "
                        f"on layer {expected}.",
                        feature_name,
                        "DatumCSYS",
                    )
                )

        return results
