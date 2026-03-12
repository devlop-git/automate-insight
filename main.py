from flask import Flask, jsonify
from app.clients.superset_client import SupersetClient
from app.clients.insight_script import bulid_dashboard_insight, generate_all_insights
# from app.database.dbConfig import DatabaseConnection

app = Flask(__name__)

client = SupersetClient()

@app.route("/")
def healthCheck():
    return jsonify({"status": "ok"})


@app.route("/dashboard/<int:id>", methods=["GET"])
def generate_insights(id):
    chart_details = []
    charts = client.getChartList(id)
    charts = charts[:5]
    for chart in charts:
        sliceInfo, query_context = client.explore(chart)
        chart_details.append(client.chartDetails(sliceInfo, query_context))
    results = generate_all_insights(chart_details)
    return jsonify(results)

@app.route("/dashboard/insights", methods=["GET"])
def get_dashboard_insights():
    charts = [
        {
            "chart_id": 1462,
            "chart_name": "CoA %| Day on Day | MTD",
            "insight": {
                "executive_insight": "The Cost of Acquisition (CoA) percentage shows an upward Day-on-Day trend, increasing from 17.6% to 19.1% over the initial observed period. A critical observation is the absence of CoA data for the last two recorded days, marked as null. This data gap requires immediate attention to ensure complete performance visibility."
            },
        },
        {
            "chart_id": 1463,
            "chart_name": "Revenue | Day on Day | MTD",
            "insight": {
                "executive_insight": "Latest daily revenue reached $264,244, demonstrating a robust 31.3% increase year-over-year. However, a consecutive day-on-day decline in revenue has been observed within the current period, falling from an initial $330K to the current value. This recent downward trend warrants further investigation to understand contributing factors and potential impacts on overall Month-to-Date performance."
            },
        },
        {
            "chart_id": 1082,
            "chart_name": "Revenue & Expenditure | Brand | Day Before",
            "insight": {
                "executive_insight": "Diamonds Factory led in revenue ($152K) and orders (162) for the period. Austen & Blake, despite lower overall volume ($112K revenue, 108 orders), demonstrated superior per-transaction profitability with a higher Average Order Value ($1,039) and a significantly better Expected Gross Margin (56.14% vs. 47.55%). Notably, SACET recorded no sales activity."
            },
        },
        {
            "chart_id": 1086,
            "chart_name": "Actual Vs Expected Daily Revenue | MTD",
            "insight": {
                "executive_insight": "Daily revenue has shown a consistent downward trend over the past four days, with the most recent daily revenue recorded at $264,244. This represents a decline from an initial $329,996, indicating a significant drop in MTD performance. Crucially, the absence of expected revenue figures prevents a complete assessment of performance against set targets."
            },
        },
        {
            "chart_id": 1116,
            "chart_name": "Revenue & Expenditure | Brand | MTD",
            "insight": {
                "executive_insight": "Month-to-date revenue for the analyzed brands totals approximately $1.2 million. Diamonds Factory leads performance with $682.4K in revenue from 698 orders, while Austen & Blake follows with $519.1K from 551 orders. A significant anomaly is SACET's exceptionally high Cost of Acquisition (CoA) at 76.4%, warranting immediate review given its minimal contribution of one order and $1K in revenue."
            },
        },
    ]
    
    result = bulid_dashboard_insight(charts)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
