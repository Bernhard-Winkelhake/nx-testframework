import os
import sys
from types import SimpleNamespace

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from check_result import Status
from check_runner import CheckRunner
from checks.plane_check import DatumPlaneLayerCheck
from checks.sketch_check import SketchLayerCheck


class FakePart:
    Leaf = "TEST_PART.prt"

    def __init__(self):
        self.Datums = [SimpleNamespace(Name="XY", Layer=62), SimpleNamespace(Name="XZ", Layer=10)]
        self.Sketches = [SimpleNamespace(Name="SKETCH_001", Layer=21)]


def test_runner_collects_results_without_nxopen():
    config = {
        "layers": {"plane": 62, "sketch": 21},
        "checks": {"enable_plane_check": True, "enable_sketch_check": True},
    }
    runner = CheckRunner(FakePart(), config=config, checks=[DatumPlaneLayerCheck(), SketchLayerCheck()])
    results = runner.run()

    assert len(results) == 3
    assert sum(r.status == Status.FAILED for r in results) == 1
    assert results[1].object_name == "XZ"


def test_report_is_dashboard_ready():
    config = {"layers": {"plane": 62}, "checks": {"enable_plane_check": True}}
    runner = CheckRunner(FakePart(), config=config, checks=[DatumPlaneLayerCheck()])
    report = runner.build_report()

    assert report["schema_version"] == 1
    assert report["part"] == "TEST_PART.prt"
    assert report["status"] == "FAILED"
    assert report["summary"]["failed"] == 1
