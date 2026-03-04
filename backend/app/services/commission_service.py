def calculate_commission(gross_revenue: float, revenue_share_percent: float) -> float:
    return round(gross_revenue * (revenue_share_percent / 100), 6)
