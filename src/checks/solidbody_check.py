# solidBodyCheck.py
import NXOpen
from typing import List

theSession = NXOpen.Session.GetSession()
workPart = theSession.Parts.Work

HOLE_LAYER_EXPECTED = 1

def move_object_to_layer(obj: NXOpen.DisplayableObject, layer: int):
    workPart.Layers.MoveDisplayableObjects(layer, [obj])

def assign_holes_to_layer():
    all_features = workPart.Features

    for feature in all_features:
        if feature.FeatureType == "HOLE":
            bodies = feature.GetBodies()
            for body in bodies:
                if isinstance(body, NXOpen.Body) and body.IsSolidBody:
                    move_object_to_layer(body, HOLE_LAYER_EXPECTED)
