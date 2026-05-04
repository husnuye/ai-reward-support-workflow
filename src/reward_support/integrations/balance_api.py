def balance_api(customer_id: str, scenario: str) -> dict:
    if scenario == "api_timeout":
        raise TimeoutError("Balance API timed out")

    if scenario == "unknown_customer":
        return {
            "customer_id": customer_id,
            "balance_deducted": None,
            "amount": None,
            "currency": "USD",
            "transaction_status": "customer_not_found",
            "transaction_id": None,
        }

    if scenario == "missing_backend_data":
        return {
            "customer_id": customer_id,
            "balance_deducted": None,
            "amount": None,
            "currency": "USD",
            "transaction_status": "unavailable",
            "transaction_id": None,
        }

    if scenario in ["high_risk", "low_risk"]:
        return {
            "customer_id": customer_id,
            "balance_deducted": True,
            "amount": 500,
            "currency": "USD",
            "transaction_status": "completed",
            "transaction_id": "TXN-9001",
        }

    return {
        "customer_id": customer_id,
        "balance_deducted": False,
        "amount": 0,
        "currency": "USD",
        "transaction_status": "not_found",
        "transaction_id": None,
    }
