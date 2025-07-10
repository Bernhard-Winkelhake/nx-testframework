from PlanesCheck import assign_datum_planes_to_layer
from SketchCheck import assign_sketches_to_layer
from savePart import save_active_part

def main():
    #  Check and correct layers if necessary
    assign_datum_planes_to_layer()
    assign_sketches_to_layer()
    save_active_part()

if __name__ == '__main__':
    main()

