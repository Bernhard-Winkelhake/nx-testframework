import NXOpen
from utils.notify import popup

STANDARDTEXT_PRICE = {"0", "n/a", "-", "hier einzelteilpreis eintragen"}
STANDARDTEXT_ORDERLINK = {"n/a", "kein link", "-", "hier link hinterlegen"}


def check_is_buy_part():
    session = NXOpen.Session.GetSession()
    workPart = session.Parts.Work

    def get_attr(name):
        try:
            return workPart.GetUserAttributeAsString(name, NXOpen.NXObject.AttributeType.String, -1).strip().lower()
        except:
            return ""
        
    

    is_buy_part = get_attr("01_Part_isBuyPart")

    if is_buy_part == "ja":
        # Wenn Kaufteil: Preis & Link prüfen
        price = get_attr("02_Part_price")
        order_link = get_attr("03_Part_orderLink")

        errors = []

        if not price or price in STANDARDTEXT_PRICE:
            errors.append("❌ '02_Part_price' ist ungültig oder nicht gesetzt.")

        if not order_link or order_link in STANDARDTEXT_ORDERLINK:
            errors.append("❌ '03_Part_orderLink' ist ungültig oder nicht gesetzt.")

        if errors:
            msg = "Kaufteil-Check fehlgeschlagen:\n\n" + "\n".join(errors)
            popup("Kaufteil-Check", msg, "error")
        else:
            popup("Kaufteil-Check", "✔️ Preis und Bestelllink sind gültig.", "info")

    elif is_buy_part == "ja/nein eintragen, sonst undefiniert":
        popup("Kaufteil-Check", "⚠️ Attribut '01_Part_isBuyPart' ist auf Standardwert gesetzt – bitte 'ja' oder 'nein' eintragen.", "warning")

    elif is_buy_part == "nein":
        popup("Kaufteil-Check", "ℹ️ Kein Kaufteil: Check übersprungen.", "note")

    elif not is_buy_part:
        popup("Kaufteil-Check", "⚠️ Attribut '01_Part_isBuyPart' ist nicht gesetzt.", "warning")

    else:
        popup("Kaufteil-Check", f"⚠️ Ungültiger Wert für '01_Part_isBuyPart': '{is_buy_part}'", "warning")
