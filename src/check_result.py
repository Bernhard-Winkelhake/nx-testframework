from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Dict, Optional


class Severity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class Status(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


@dataclass
class CheckResult:
    rule_id: str
    check_name: str
    status: Status
    severity: Severity = Severity.ERROR
    message: str = ""
    object_name: Optional[str] = None
    object_type: Optional[str] = None

    @property
    def is_failure(self) -> bool:
        return self.status == Status.FAILED

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        data["severity"] = self.severity.value
        return data
