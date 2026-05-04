def campaign_api(customer_id: str, scenario: str) -> dict:
    if scenario == "api_timeout":
        raise TimeoutError("Campaign API timed out")

    if scenario in ["unknown_customer", "missing_backend_data"]:
        return {
            "customer_id": customer_id,
            "checked": False,
            "campaign_visible": None,
            "campaign_active": None,
            "issue": "campaign_data_unavailable",
            "message": "Campaign data could not be validated.",
        }

    if scenario == "medium_risk":
        return {
            "customer_id": customer_id,
            "checked": True,
            "campaign_visible": True,
            "campaign_active": False,
            "issue": "expired_campaign_still_visible",
            "message": "Campaign is visible but no longer active in the backend.",
        }

    return {
        "customer_id": customer_id,
        "checked": False,
        "campaign_visible": False,
        "campaign_active": None,
        "issue": None,
        "message": None,
    }
