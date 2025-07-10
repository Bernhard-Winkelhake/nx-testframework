from planesCheck import assign_datum_planes_to_layer
from sketchCheck import assign_sketches_to_layer
from savePart import save_active_part
from solidBodyCheck import assign_holes_to_layer

def main():
    #  Check and correct layers if necessary
    assign_datum_planes_to_layer()
    assign_sketches_to_layer()
    #assign_holes_to_layer()
    save_active_part()

if __name__ == '__main__':
    main()

