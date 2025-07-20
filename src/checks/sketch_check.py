# SketchCheck.py
import NXOpen
import NXOpen.Layer
from typing import List

theSession = NXOpen.Session.GetSession()
workPart = theSession.Parts.Work

SKETCH_LAYER_EXPECTED = 21

def move_object_to_layer(obj: NXOpen.DisplayableObject, layer: int):
    workPart.Layers.MoveDisplayableObjects(layer, [obj])

def get_all_sketches() -> List[NXOpen.Sketch]:
    return list(workPart.Sketches)

def assign_sketches_to_layer():
    for sketch in get_all_sketches():
        move_object_to_layer(sketch, SKETCH_LAYER_EXPECTED)
