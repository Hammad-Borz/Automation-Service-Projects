from typing import Any


def process_lead(lead: dict[str, Any]) -> dict[str, Any]:
    message = lead.get("message", "").lower()
    source = lead.get("source", "").lower()

    sales_keywords = [
        "interested",
        "automation",
        "services",
        "pricing",
        "quote",
        "buy",
        "purchase",
        "demo",
    ]

    support_keywords = [
        "problem",
        "issue",
        "error",
        "help",
        "support",
        "not working",
    ]

    billing_keywords = [
        "invoice",
        "payment",
        "billing",
        "refund",
        "charge",
    ]

    sales_score = sum(keyword in message for keyword in sales_keywords)
    support_score = sum(keyword in message for keyword in support_keywords)
    billing_score = sum(keyword in message for keyword in billing_keywords)

    if sales_score >= support_score and sales_score >= billing_score and sales_score > 0:
        lead_type = "sales"
    elif support_score >= billing_score and support_score > 0:
        lead_type = "support"
    elif billing_score > 0:
        lead_type = "billing"
    else:
        lead_type = "general"

    score = 50

    if lead_type == "sales":
        score += 20
    elif lead_type == "support":
        score += 10

    if "website" in source:
        score += 10

    if any(keyword in message for keyword in ["urgent", "asap", "immediately"]):
        score += 15

    score = min(score, 100)

    if score >= 75:
        priority = "high"
    elif score >= 50:
        priority = "medium"
    else:
        priority = "low"

    reason = (
        f"Lead classified as {lead_type} based on message content. "
        f"Calculated lead score: {score}/100."
    )

    return {
        "lead_type": lead_type,
        "priority": priority,
        "score": score,
        "reason": reason,
    }