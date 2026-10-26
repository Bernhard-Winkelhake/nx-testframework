from check_result import CheckResult, Severity, Status
from checks.base import BaseCheck
from checks.responsiblePerson_check import _get_string_attr

STANDARDTEXT_PRICE = {"0", "n/a", "-", "hier einzelteilpreis eintragen", "hier einzelpreis eintragen"}
STANDARDTEXT_ORDERLINK = {"n/a", "kein link", "-", "hier link hinterlegen", "hier link eintragen"}
STANDARDTEXT_FLAG = {"ja/nein eintragen, sonst undefiniert" }


class BuyPartCheck(BaseCheck):
    rule_id = "BUY_PART"
    name = "Buy part attributes"
    config_key = "enable_buy_part_check"

    def run(self, work_part, config):
        attrs = config.get("attributes", {})
        flag_name = attrs.get("buy_part_flag", "01_Part_isBuyPart")
        price_name = attrs.get("price", "02_Part_price")
        link_name = attrs.get("order_link", "03_Part_orderLink")
        flag = _get_string_attr(work_part, flag_name).lower()

        if flag == "nein":
            return [CheckResult(self.rule_id, self.name, Status.SKIPPED, Severity.INFO,
                                "Part is not a buy part; price/link checks skipped.")]
        if not flag or flag == STANDARDTEXT_FLAG or flag not in {"ja", "nein"}:
            return [CheckResult(self.rule_id, self.name, Status.FAILED, Severity.WARNING,
                                f"Attribute '{flag_name}' must be 'ja' or 'nein'.")]

        results = []
        price = _get_string_attr(work_part, price_name).lower()
        link = _get_string_attr(work_part, link_name).lower()
        results.append(CheckResult(
            "BUY_PART_PRICE", "Buy part price",
            Status.FAILED if (not price or price in STANDARDTEXT_PRICE) else Status.PASSED,
            Severity.ERROR,
            f"Attribute '{price_name}' is " + ("missing or invalid." if (not price or price in STANDARDTEXT_PRICE) else "valid.")
        ))
        results.append(CheckResult(
            "BUY_PART_ORDER_LINK", "Buy part order link",
            Status.FAILED if (not link or link in STANDARDTEXT_ORDERLINK) else Status.PASSED,
            Severity.ERROR,
            f"Attribute '{link_name}' is " + ("missing or invalid." if (not link or link in STANDARDTEXT_ORDERLINK) else "valid.")
        ))
        return results
