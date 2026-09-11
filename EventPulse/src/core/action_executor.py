from typing import Any


def execute_actions(rule_results: list[dict[str, Any]]) -> list[dict[str, str]]:
    messages = {
        "notify_sales": "Sales notification prepared",
        "route_support": "Support routing prepared",
        "flag_high_value_order": "High-value order flagged",
        "record_payment": "Payment recorded locally",
        "prepare_confirmation": "Payment confirmation prepared",
        "no_action": "No automation action required",
    }
    return [
        {"action": item["action"], "status": "prepared", "message": messages[item["action"]]}
        for item in rule_results
    ]
