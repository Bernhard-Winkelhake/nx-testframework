# Planescheck.py
import NXOpen
import NXOpen.Layer
import json
from typing import List


from config_loader import load_config

config = load_config()


theSession = NXOpen.Session.GetSession()
workPart = theSession.Parts.Work

DATUM_PLANES_LAYER_EXPECTED = config["layers"]["plane"]

def move_object_to_layer(obj: NXOpen.DisplayableObject, layer: int):
    workPart.Layers.MoveDisplayableObjects(layer, [obj])

def get_all_datum_planes() -> List[NXOpen.DatumPlane]:
    return list(workPart.Datums)

def assign_datum_planes_to_layer():
    for datum in get_all_datum_planes():
        move_object_to_layer(datum, DATUM_PLANES_LAYER_EXPECTED)
