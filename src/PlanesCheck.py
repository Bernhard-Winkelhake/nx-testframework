# Planescheck.py
import NXOpen
import NXOpen.Layer
from typing import List

theSession = NXOpen.Session.GetSession()
workPart = theSession.Parts.Work

DATUM_PLANES_LAYER_EXPECTED = 62

def move_object_to_layer(obj: NXOpen.DisplayableObject, layer: int):
    workPart.Layers.MoveDisplayableObjects(layer, [obj])

def get_all_datum_planes() -> List[NXOpen.DatumPlane]:
    return list(workPart.Datums)

def assign_datum_planes_to_layer():
    for datum in get_all_datum_planes():
        move_object_to_layer(datum, DATUM_PLANES_LAYER_EXPECTED)
