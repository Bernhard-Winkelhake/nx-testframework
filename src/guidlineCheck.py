import NXOpen

def main():
    theSession = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    ui = NXOpen.UI.GetUI()

    # Erwartete Layer
    SKETCH_LAYER_EXPECTED = 21
    PLANE_LAYER_EXPECTED = 62

    fully_constrained_sketches = []
    under_constrained_sketches = []
    wrong_layer_sketches = []
    wrong_layer_planes = []

    # Skizzen prüfen
    for sketch in workPart.Sketches:
        name = sketch.Name
        status, dof_needed = sketch.GetStatus()

        if status.value == 3:
            fully_constrained_sketches.append(name)
        else:
            under_constrained_sketches.append(f"{name} (Status: {status}, DOF Needed: {dof_needed})")

        if sketch.Layer != SKETCH_LAYER_EXPECTED:
            wrong_layer_sketches.append(f"{name} (Layer: {sketch.Layer})")

    # Ebenen prüfen und ggf. Layer korrigieren
    for plane in workPart.Planes:
        name = plane.Name
        if plane.Layer != PLANE_LAYER_EXPECTED:
            wrong_layer_planes.append(f"{name} (Layer: {plane.Layer})")
            plane.Layer = PLANE_LAYER_EXPECTED  # Plane auf richtigen Layer verschieben


    # Attribut "Ansprechpartner" prüfen
    attribute_value = None
    try:
        attributes = workPart.GetUserAttributes()
        for attr in attributes:
            if attr.Title.strip().lower() == "ansprechpartner":
                attribute_value = attr.StringValue.strip()
                break
    except Exception:
        attribute_value = None



    # Ergebnisnachricht zusammenstellen
    message = ""

    # Ansprechpartner-Attribut prüfen
    if attribute_value and attribute_value.lower() != "hier deinen namen eintragen":
        message += f"✅ Attribut 'Ansprechpartner' ist gesetzt: {attribute_value}\n\n"
    else:
        message += f"⛔️ Attribut 'Ansprechpartner' ist NICHT korrekt gesetzt!\n\n"

    # Skizzenstatus prüfen
    if under_constrained_sketches:
        message += "⛔️ Nicht vollständig bestimmte Skizzen:\n"
        message += "\n".join(f" - {name}" for name in sorted(under_constrained_sketches)) + "\n\n"
    else:
        message += "✅ Alle Skizzen sind vollständig bestimmt.\n\n"

    # Layer der Skizzen prüfen
    if wrong_layer_sketches:
        message += f"⚠️ Skizzen nicht auf Layer {SKETCH_LAYER_EXPECTED}:\n"
        message += "\n".join(f" - {name}" for name in sorted(wrong_layer_sketches)) + "\n\n"
    else:
        message += f"✅ Alle Skizzen sind auf Layer {SKETCH_LAYER_EXPECTED}.\n\n"

    # Layer der Ebenen prüfen
    if wrong_layer_planes:
        message += f"⚠️ Ebenen nicht auf Layer {PLANE_LAYER_EXPECTED}:\n"
        message += "\n".join(f" - {name}" for name in sorted(wrong_layer_planes)) + "\n\n"
    else:
        message += f"✅ Alle Ebenen sind auf Layer {PLANE_LAYER_EXPECTED}.\n\n"

    # Ergebnis anzeigen
    ui.NXMessageBox.Show("Skizzen-, Ebenen- und Attributprüfung", NXOpen.NXMessageBox.DialogType.Information, message)

if __name__ == '__main__':
    main()
