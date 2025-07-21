# Planescheck.py
import NXOpen
import NXOpen.Layer

from typing import List

from utils.config_loader import load_config




# NX Session and Work Part
theSession = NXOpen.Session.GetSession()
workPart = theSession.Parts.Work

# Load Layer from config
config = load_config()
DATUM_PLANES_LAYER_EXPECTED = config.get("layers", {}).get("plane", 62)
  

def move_object_to_layer(obj: NXOpen.DisplayableObject, layer: int):
    workPart.Layers.MoveDisplayableObjects(layer, [obj])

def get_all_datum_planes() -> List[NXOpen.DatumPlane]:
    return list(workPart.Datums)

def assign_datum_planes_to_layer():
    for datum in get_all_datum_planes():
        move_object_to_layer(datum, DATUM_PLANES_LAYER_EXPECTED)
