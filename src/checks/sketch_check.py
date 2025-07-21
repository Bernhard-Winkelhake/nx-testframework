# SketchCheck.py
import NXOpen
import NXOpen.Layer
from typing import List

from utils.config_loader import load_config

# NX Session and Work Part
theSession = NXOpen.Session.GetSession()
workPart = theSession.Parts.Work

# Load Layer from config
config = load_config()
SKETCH_LAYER_EXPECTED =  config.get("layers", {}).get("sketch", 21)



def move_object_to_layer(obj: NXOpen.DisplayableObject, layer: int):
    workPart.Layers.MoveDisplayableObjects(layer, [obj])

def get_all_sketches() -> List[NXOpen.Sketch]:
    return list(workPart.Sketches)

def assign_sketches_to_layer():
    for sketch in get_all_sketches():
        move_object_to_layer(sketch, SKETCH_LAYER_EXPECTED)
