import os
import json
from pathlib import Path
import re
import time
import google.generativeai as genai
from app.core.config import settings

# Configure API
genai.configure(api_key=settings.GEMINI_API_KEY)

# Use Gemini 1.5 Flash (fast + cheap)
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_insight_with_gemini(chart):
    """
    Send chart data to Gemini and generate business insight
    with confidence score and usage metadata.
    """

    prompt = f"""
You are a senior business analyst.

Analyze the chart data and generate a concise executive insight.

Return JSON in this format:

{{
  "insight_text": "short executive summary",
  "trend": "increasing | decreasing | stable | unknown",
  "confidence_score": 0-1,
  "anomaly_detected": true/false
}}

Rules:
- Maximum 3–4 sentences
- Mention key metric values if present
- Mention trend if visible
- Highlight anomalies if any

Chart Data:
{json.dumps(chart, indent=2)}
"""

    response = model.generate_content(
        prompt, generation_config={"response_mime_type": "application/json"}
    )

    # Parse model output
    try:
        insight_data = json.loads(response.text.strip())
        usage_metadata = {
            "prompt_tokens": response.usage_metadata.prompt_token_count,
            "completion_tokens": response.usage_metadata.candidates_token_count,
            "total_tokens": response.usage_metadata.total_token_count,
        }
    except Exception:
        return {
            "insight_text": response.text.strip(),
            "confidence_score": 0.3,
        }

    return {
        "chart_id": chart.get("chart_id"),
        "insight_text": insight_data.get("insight_text"),
        "confidence_score": insight_data.get("confidence_score"),
        "usage_metadata": usage_metadata,
    }


def generate_all_insights(charts):
    results = []

    for chart in charts:
        insight = generate_insight_with_gemini(chart)
        results.append(insight)
        time.sleep(6)  # 60 sec / 5 requests = 12 sec

    return results


def parse_llm_response(response_text):
    # remove ```json ``` wrappers
    cleaned = re.sub(r"```json|```", "", response_text).strip()

    # convert string to dict
    return json.loads(cleaned)


def build_dashboard_insight(charts):
    chart_text = "\n\n".join(
        f"{i+1}. Chart: {c['chart_name']}\nInsight: {c['insight_text']}"
        for i, c in enumerate(charts)
    )

    prompt = f"""
You are a senior business intelligence analyst.

Analyze the following insights from dashboard charts and produce consolidated insights.

{chart_text}

Output Rules:
- Return strictly valid JSON.
- Do NOT include markdown or explanations.
- Output must be pointer format only.
- Each pointer must contain:
    "insight": text
    "confidence_score": number between 0 and 1.

JSON Structure:

{{
  "overall_insight": [{{"insight": "...", "confidence_score": 0.0}}],
  "key_trends": [],
  "risks": [],
  "opportunities": [],
  "data_quality_issues": []
}}
"""

    response = model.generate_content(prompt)

    parsed_result = parse_llm_response(response.text)
    usage_metadata = {
        "prompt_tokens": response.usage_metadata.prompt_token_count,
        "completion_tokens": response.usage_metadata.candidates_token_count,
        "total_tokens": response.usage_metadata.total_token_count,
    }

    return {"insight":parsed_result,"usage_metadata":usage_metadata}
