import os
import sys
from types import SimpleNamespace

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from check_result import Status
from checks.plane_check import DatumPlaneLayerCheck


def test_datum_plane_layer_check_reports_wrong_layer():
    work_part = SimpleNamespace(Datums=[
        SimpleNamespace(Name="XY", Layer=62),
        SimpleNamespace(Name="XZ", Layer=10),
    ])
    config = {"layers": {"plane": 62}}

    results = DatumPlaneLayerCheck().run(work_part, config)

    assert len(results) == 2
    assert results[0].status == Status.PASSED
    assert results[1].status == Status.FAILED
    assert results[1].object_name == "XZ"
