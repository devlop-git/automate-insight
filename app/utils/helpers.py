from urllib.parse import parse_qs, urlparse


def extract_form_data(slice_url: str):
    # Parse query parameters
    parsed = urlparse(slice_url)
    query_params = parse_qs(parsed.query)

    # Get encoded form_data
    encoded_form_data = query_params.get("form_data", [None])[0]

    return encoded_form_data