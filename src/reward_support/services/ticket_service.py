import json
import os
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_TICKET_PATH = "data/support_tickets.json"


def load_json(path: str):
    ticket_path = Path(path)
    if not ticket_path.exists():
        return []

    with ticket_path.open("r") as f:
        return json.load(f)


def save_json(path: str, data):
    ticket_path = Path(path)
    ticket_path.parent.mkdir(parents=True, exist_ok=True)

    with ticket_path.open("w") as f:
        json.dump(data, f, indent=2)


def create_review_ticket(
    customer_id: str,
    reason: str,
    trace_id: str,
    priority: str = "normal",
    assigned_queue: str = "reward_support_review",
    path: str | None = None,
) -> dict:
    ticket_path = path or os.getenv("SUPPORT_TICKET_PATH", DEFAULT_TICKET_PATH)
    tickets = load_json(ticket_path)

    ticket = {
        "ticket_id": f"REV-{trace_id[:8].upper()}",
        "customer_id": customer_id,
        "priority": priority,
        "status": "pending_review",
        "reason": reason,
        "assigned_queue": assigned_queue,
        "trace_id": trace_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    existing_index = next(
        (
            index
            for index, existing_ticket in enumerate(tickets)
            if existing_ticket.get("ticket_id") == ticket["ticket_id"]
        ),
        None,
    )

    if existing_index is None:
        tickets.append(ticket)
    else:
        tickets[existing_index] = ticket

    save_json(ticket_path, tickets)
    return ticket


def create_ticket(customer_id: str, risk_res: dict, path: str = DEFAULT_TICKET_PATH) -> dict:
    return create_review_ticket(
        customer_id=customer_id,
        reason=risk_res["reason"],
        trace_id=risk_res.get("trace_id", f"legacy-{customer_id}"),
        priority="high" if risk_res["risk_level"] == "high" else "normal",
        path=path,
    )
