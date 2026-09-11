from typing import Any


def generate_insights(analytics: dict[str, Any]) -> list[dict[str, Any]]:
    insights = []
    trends = analytics["trends"]; comparison = analytics["comparison"]
    growth = trends["revenue_growth_percent"]
    if growth >= 10 or growth <= -10:
        direction = "increased" if growth > 0 else "declined"
        insights.append({"type": "revenue", "severity": "high" if growth < -10 else "medium", "title": f"Revenue {direction}", "description": f"Revenue changed {growth:.2f}% versus the previous month.", "metric": "revenue_growth_percent", "value": growth, "recommendation": "Review categories, regions, and channels driving the period change."})
    for key, label, field in (("categories", "category", "category"), ("regions", "region", "region"), ("channels", "sales channel", "sales_channel")):
        top = analytics[key].get("top")
        if top and top["revenue_share_percent"] >= 50:
            insights.append({"type": key, "severity": "medium", "title": f"{label.title()} concentration", "description": f"{top[field]} contributes {top['revenue_share_percent']:.2f}% of revenue.", "metric": f"{key}.revenue_share_percent", "value": top["revenue_share_percent"], "recommendation": "Monitor concentration and diversify growth opportunities."})
    for anomaly in analytics["anomalies"]:
        insights.append({"type": "anomaly", "severity": anomaly["severity"], "title": f"Revenue {anomaly['anomaly_type']} detected", "description": f"{anomaly['metric'].title()} on {anomaly['date']} was {abs(anomaly['deviation']):.2f} standard deviations from baseline.", "metric": anomaly["metric"], "value": anomaly["value"], "recommendation": "Review operational events and source transactions for this date."})
    return insights
