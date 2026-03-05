from flask import Flask, jsonify
from app.clients.superset_client import SupersetClient
from app.clients.insight_script import generate_all_insights

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


if __name__ == "__main__":
    app.run(debug=True)
