import NXOpen
from utils.notify import popup

STANDARDTEXT_NAME = {"hier deinen namen eintragen"}


def check_responsiblePerson():
    session = NXOpen.Session.GetSession()
    workPart = session.Parts.Work

    def get_attr(name):
        try:
            return workPart.GetUserAttributeAsString(name, NXOpen.NXObject.AttributeType.String, -1).strip().lower()
        except:
            return ""
        
    

    currentResponsiblePerson = get_attr("00_ResponsiblePerson")

    if currentResponsiblePerson == "":
        popup("Responsible Person Check", f"⚠️ Ungültiger Wert für '00_ResponsiblePerson': '{currentResponsiblePerson}'", "error")
    elif not currentResponsiblePerson or currentResponsiblePerson in STANDARDTEXT_NAME:
        popup("Responsible Person Check", f"⚠️ Ungültiger Wert für '00_ResponsiblePerson': '{currentResponsiblePerson}'", "error")
    
