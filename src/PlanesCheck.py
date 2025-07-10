import NXOpen
import NXOpen.Layer
from typing import List

theSession = NXOpen.Session.GetSession()
workPart = theSession.Parts.Work
displayPart = theSession.Parts.Display

def move_object_to_layer(object: NXOpen.DisplayableObject, layer:int):
    objectArray1 = [NXOpen.DisplayableObject.Null] * 1
    objectArray1[0] = object
    workPart.Layers.MoveDisplayableObjects(layer, objectArray1)

def get_all_datum_planes() -> List[NXOpen.Body]:
    all_datums: List[NXOpen.Body] = []
    for item in workPart.Datums:
        all_datums.append(item)
    return all_datums




def main():
    

    # Erwartete Layer
    SKETCH_LAYER_EXPECTED = 21
    DATUM__PLANES_LAYER_EXPECTED = 62

    all_datum_planes: List[NXOpen.DatumPlane] = get_all_datum_planes()
    for i in range(len(all_datum_planes)):
        move_object_to_layer(all_datum_planes[i],DATUM__PLANES_LAYER_EXPECTED)

            



if __name__ == '__main__':
    main()
