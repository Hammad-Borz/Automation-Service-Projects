ROUTES = {
    "lead.created": "lead_automation",
    "lead.updated": "lead_update_automation",
    "order.created": "order_automation",
    "payment.received": "payment_automation",
    "support.ticket_created": "support_automation",
}


def route_event(event_type: str) -> str:
    return ROUTES.get(event_type, "general_noop")
