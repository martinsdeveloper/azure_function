import azure.functions as func
import datetime
import json
import logging
import requests
import os

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

    resp = requests.get(os.getenv("JOKE_URL"))

    joke_data = resp.json()
    joke_data["giffs"] = list(load_image(joke_data.get("value", "chuck norris")))
    joke_json = json.dumps(joke_data)

    return func.HttpResponse(body=joke_json, mimetype="application/json", status_code=200)

def process_query(query):
    if REQUIRED_STRING not in query[:3]:
        query.insert(0, "Chuck Norris")

    return " ".join(query[:7])

def load_image(query):
    logging.info(f'Aquiring gif for: {query}')

    api_key = os.getenv("GIPHY_TOKEN")
    url = f'http://api.giphy.com/v1/gifs/search?q={process_query(query.split())}&api_key={api_key}&limit={os.getenv("GIFF_LIMIT")}'

    resp = requests.get(url)
    joke_data = resp.json()

    for i in joke_data.get("data", {}):
        logging.info(i.get("images", {}).get("original", {}))
        yield i.get("images", {}).get("original", {})