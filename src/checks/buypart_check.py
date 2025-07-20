# buyPartCheck.py
import NXOpen

STANDARDTEXT_PRICE = {"0", "n/a", "-"}
STANDARDTEXT_ORDERLINK = {"n/a", "kein link", "-"}


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
        price = get_attr("02_Part_price")
        order_link = get_attr("03_Part_orderLink")

        errors = []

        if not price or price in STANDARDTEXT_PRICE:
            errors.append("❌ '02_Part_price' ist ungültig oder nicht gesetzt.")

        if not order_link or order_link in STANDARDTEXT_ORDERLINK:
            errors.append("❌ '03_Part_orderLink' ist ungültig oder nicht gesetzt.")

        if errors:
            print("⚠️ Kaufteil-Check fehlgeschlagen:")
            for err in errors:
                print(err)
        else:
            print("✔️ Kaufteil-Check bestanden: Preis und Bestelllink sind gültig.")
    else:
        print("ℹ️ Kein Kaufteil: Check übersprungen.")
