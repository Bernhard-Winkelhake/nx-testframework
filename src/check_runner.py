import json
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional

from check_result import CheckResult, Severity, Status
from checks.buypart_check import BuyPartCheck
from checks.plane_check import DatumPlaneLayerCheck
from checks.responsiblePerson_check import ResponsiblePersonCheck
from checks.sketch_check import SketchLayerCheck
from utils.config_loader import load_config
from checks.datumCsys_check import DatumCsysLayerCheck


DEFAULT_CHECKS = [
    DatumPlaneLayerCheck,
    DatumCsysLayerCheck,
    SketchLayerCheck,
    ResponsiblePersonCheck,
    BuyPartCheck,
]


class CheckRunner:
    """Executes registered checks against one NX work part.

    The runner never changes or saves the part. This makes the output suitable
    for later upload to a REST API / web dashboard.
    """

    def __init__(self, work_part, config=None, checks: Optional[Iterable] = None):
        self.work_part = work_part
        self.config = config or load_config()
        self.checks = list(checks) if checks is not None else [c() for c in DEFAULT_CHECKS]

    @classmethod
    def from_active_nx_part(cls, config=None, checks=None):
        import NXOpen
        work_part = NXOpen.Session.GetSession().Parts.Work
        if work_part is None:
            raise RuntimeError("No active NX work part.")
        return cls(work_part, config=config, checks=checks)

    def run(self) -> List[CheckResult]:
        results = []
        for check in self.checks:
            if not check.is_enabled(self.config):
                continue
            try:
                results.extend(check.run(self.work_part, self.config))
            except Exception as exc:
                results.append(CheckResult(
                    rule_id=getattr(check, "rule_id", check.__class__.__name__),
                    check_name=getattr(check, "name", check.__class__.__name__),
                    status=Status.FAILED,
                    severity=Severity.ERROR,
                    message=f"Check crashed: {exc}",
                ))
        return results

    def build_report(self, results=None):
        results = self.run() if results is None else results
        failed = sum(1 for r in results if r.status == Status.FAILED)
        warnings = sum(1 for r in results if r.status == Status.FAILED and r.severity == Severity.WARNING)
        part_name = getattr(self.work_part, "Leaf", None) or getattr(self.work_part, "Name", None) or "unknown"
        return {
            "schema_version": 1,
            "part": part_name,
            "checked_at": datetime.now().astimezone().isoformat(),
            "status": "FAILED" if failed else "PASSED",
            "summary": {
                "total": len(results),
                "failed": failed,
                "warnings": warnings,
                "passed": sum(1 for r in results if r.status == Status.PASSED),
                "skipped": sum(1 for r in results if r.status == Status.SKIPPED),
            },
            "results": [r.to_dict() for r in results],
        }

    def write_json(self, path, results=None):
        report = self.build_report(results)
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        return report
