def voucher_api(customer_id: str, scenario: str) -> dict:
    if scenario == "api_timeout":
        raise TimeoutError("Voucher API timed out")

    if scenario in ["unknown_customer", "missing_backend_data"]:
        return {
            "customer_id": customer_id,
            "voucher_found": None,
            "voucher_id": None,
            "amount": None,
            "currency": "USD",
            "status": "unavailable",
            "delivery_method": None,
            "location": None,
        }

    if scenario == "low_risk":
        return {
            "customer_id": customer_id,
            "voucher_found": True,
            "voucher_id": "VCH-1001",
            "amount": 500,
            "currency": "USD",
            "status": "issued",
            "delivery_method": "email",
            "location": "My Rewards",
        }

    return {
        "customer_id": customer_id,
        "voucher_found": False,
        "voucher_id": None,
        "amount": 0,
        "currency": "USD",
        "status": "missing",
        "delivery_method": None,
        "location": None,
    }
