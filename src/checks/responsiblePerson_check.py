from check_result import CheckResult, Severity, Status
from checks.base import BaseCheck

STANDARDTEXT_NAME = {"hier deinen namen eintragen","hier namen eintragen"}


def _get_string_attr(work_part, name):
    try:
        import NXOpen
        return work_part.GetUserAttributeAsString(
            name, NXOpen.NXObject.AttributeType.String, -1
        ).strip()
    except Exception:
        return ""


class ResponsiblePersonCheck(BaseCheck):
    rule_id = "RESPONSIBLE_PERSON"
    name = "Responsible person"
    config_key = "enable_responsible_person_check"

    def run(self, work_part, config):
        attr_name = config.get("attributes", {}).get(
            "responsible_person", "00_ResponsiblePerson"
        )
        value = _get_string_attr(work_part, attr_name)
        invalid = not value or value.lower() in STANDARDTEXT_NAME
        if invalid:
            return [CheckResult(self.rule_id, self.name, Status.FAILED, Severity.ERROR,
                                f"Attribute '{attr_name}' is missing or invalid.")]
        return [CheckResult(self.rule_id, self.name, Status.PASSED, Severity.ERROR,
                            f"Responsible person is set to '{value}'.")]
