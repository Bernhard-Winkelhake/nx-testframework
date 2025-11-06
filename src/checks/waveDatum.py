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
WAVEDATUM_PLANES_LAYER_EXPECTED = config.get("layers", {}).get("wavedatum", 81)
  

def move_object_to_layer(obj: NXOpen.DisplayableObject, layer: int):
    workPart.Layers.MoveDisplayableObjects(layer, [obj])

def get_all_waveDatum_planes() -> List[NXOpen.WaveDatum]:
    return list(workPart.WaveDatums)

def assign_datum_planes_to_layer():
    for waveDatum in get_all_datum_planes():
        move_object_to_layer(waveDatum, DATUM_PLANES_LAYER_EXPECTED)
