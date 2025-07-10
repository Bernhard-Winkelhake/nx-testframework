# savePart.py
import NXOpen

def save_active_part():
    session = NXOpen.Session.GetSession()
    workPart = session.Parts.Work
    workPart.Save(0,0)
