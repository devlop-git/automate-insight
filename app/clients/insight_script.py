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
    Send chart data to Gemini Flash and get business insight.
    """
    prompt = f"""
    You are a business analyst.

    Generate a concise executive insight for the following chart data.
    Include:
    - Key metric value
    - Trend (YoY if available)
    - Any anomaly or observation
    - Keep it professional and short (3-4 sentences max)

    Chart Data:
    {json.dumps(chart, indent=2)}
    """

    response = model.generate_content(
        prompt, generation_config={"response_mime_type": "application/json"}
    )

    try:
        parsed = json.loads(response.text)
    except Exception:
        parsed = {
            "summary": response.text.strip(),
            "trend": "unknown",
            "confidence": "low",
        }

    return {
        "chart_id": chart.get("id"),
        "chart_name": chart.get("slice_name"),
        "insight": parsed,
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

def bulid_dashboard_insight(charts):
    chart_text = "\n\n".join(
        f"{i+1}. Chart: {c['chart_name']}\nInsight: {c['insight']['executive_insight']}"
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

    return parsed_result
