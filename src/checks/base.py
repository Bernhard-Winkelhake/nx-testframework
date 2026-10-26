from abc import ABC, abstractmethod
from typing import List

from check_result import CheckResult


class BaseCheck(ABC):
    """Base class for all NX model checks.

    Checks only inspect the model and return CheckResult objects. They must not
    modify or save the part. Corrections belong in a separate fixer layer.
    """

    rule_id = "BASE"
    name = "Base check"
    config_key = None

    def is_enabled(self, config: dict) -> bool:
        if not self.config_key:
            return True
        return bool(config.get("checks", {}).get(self.config_key, True))

    @abstractmethod
    def run(self, work_part, config: dict) -> List[CheckResult]:
        raise NotImplementedError
