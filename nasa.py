import requests


def search_nasa(query: str):
    url = "https://images-api.nasa.gov/search"

    params = {
        "q": query,
        "media_type": "image"
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    data = response.json()

    results = []

    for item in data.get("collection", {}).get("items", [])[:5]:
        info = item.get("data", [{}])[0]

        results.append({
            "title": info.get("title"),
            "description": info.get("description"),
            "date_created": info.get("date_created"),
            "nasa_id": info.get("nasa_id"),
            "center": info.get("center")
        })

    return results
