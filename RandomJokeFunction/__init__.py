import azure.functions as func
import json
import logging
import os
import requests

app = func.FunctionApp()

REQUIRED_STRING = "Chuck"

@app.function_name("RandomJokeFunction")
@app.route(route="random_joke", auth_level=func.AuthLevel.ANONYMOUS)
def random_joke(req: func.HttpRequest) -> func.HttpResponse:
    if req.method != "GET":
        return func.HttpResponse(
            "Only GET requests are allowed.",
            status_code=405
        )

    joke_url = os.getenv("JOKE_URL")
    if not joke_url:
        logging.error("Environment variable JOKE_URL is not set.")
        return func.HttpResponse(
            "Internal server error.",
            status_code=500
        )

    try:
        resp = requests.get(joke_url)
        resp.raise_for_status()
        joke_data = dict(value=resp.json().get("value", ""))
    except requests.RequestException as e:
        logging.error(f"Error fetching joke: {e}")
        return func.HttpResponse(
            "Failed to fetch joke.",
            status_code=500
        )
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing joke response: {e}")
        return func.HttpResponse(
            "Error processing joke response.",
            status_code=500
        )

    try:
        joke_data["giffs"] = list(load_image(joke_data.get("value", "chuck norris")))
    except Exception as e:
        logging.error(f"Error loading GIFs: {e}")
        return func.HttpResponse(
            "Failed to load GIFs.",
            status_code=500
        )

    return func.HttpResponse(
        body=json.dumps(joke_data),
        mimetype="application/json",
        status_code=200
    )

def process_query(query):
    if REQUIRED_STRING not in query[:3]:
        query.insert(0, "Chuck Norris")

    return " ".join(query[:7])

def load_image(query):
    logging.info(f'Acquiring gif for: {query}')

    api_key = os.getenv("GIPHY_TOKEN")
    if not api_key:
        logging.error("Environment variable GIPHY_TOKEN is not set.")
        raise ValueError("GIPHY_TOKEN is not set")

    gif_limit = os.getenv("GIFF_LIMIT", "5")

    url = f'http://api.giphy.com/v1/gifs/search?q={process_query(query.split())}&api_key={api_key}&limit={gif_limit}'

    try:
        resp = requests.get(url)
        resp.raise_for_status()
        gif_data = resp.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching GIFs: {e}")
        return []
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing GIF response: {e}")
        return []

    gifs = []
    for gif in gif_data.get("data", []):
        original_image = gif.get("images", {}).get("original", {})
        logging.info(original_image)
        gifs.append(original_image)

    return gifs
