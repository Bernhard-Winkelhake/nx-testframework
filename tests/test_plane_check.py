import pytest
import sys
import os

# Pfad zur src hinzufügen, aber NICHT sys.path.clear()
sys.path.append(os.path.abspath("../src"))

from checks import plane_check
from checks.plane_check import assign_datum_planes_to_layer
from unittest.mock import MagicMock, patch

@patch("checks.plane_check.workPart")
def test_assign_datum_planes_to_layer(mock_workPart):
    mock_object = MagicMock()
    mock_object.Layer = 10
    mock_workPart.Datums.ToArray.return_value = [mock_object]

    plane_check.DATUM_PLANES_LAYER_EXPECTED = 62

    assign_datum_planes_to_layer()

    mock_workPart.Layers.MoveDisplayableObjects.assert_called_with(
        62, [mock_object]
    )
