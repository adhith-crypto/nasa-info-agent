import requests

PDS_URL = "https://pds.nasa.gov/api/search/1/products"


def search_nasa(query: str):
    params = {
        "q": query,
        "limit": 10
    }

    try:
        response = requests.get(
            PDS_URL,
            params=params,
            headers={"Accept": "application/json"},
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

    except requests.RequestException as e:
        return [{
            "error": f"NASA PDS request failed: {str(e)}"
        }]

    results = []

    for item in data.get("data", []):
        results.append({
            "title": item.get("title"),
            "identifier": item.get("lidvid"),
            "start_time": item.get("start_date_time"),
            "target": item.get("target_name"),
            "instrument": item.get("instrument_name"),
            "source": "NASA Planetary Data System"
        })

    return results
