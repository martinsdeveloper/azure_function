import azure.functions as func
import datetime
import json
import logging
import requests

app = func.FunctionApp()

REQUIRED_STRING = "Chuck"

# @app.function_name("RandomJokeFunction")
@app.route(route="random_joke", auth_level=func.AuthLevel.ANONYMOUS)
def main(req: func.HttpRequest, msg: func.Out[str]) -> func.HttpResponse:
    if req.method != "GET":
        return func.HttpResponse(
            "Only GET requests are allowed.",
            status_code=405
        )
    
    resp = requests.get("https://api.chucknorris.io/jokes/random")

    joke_data = resp.json()
    joke_data["giffs"] = list(load_image(joke_data.get("value", "chuck norris")))
    joke_json = json.dumps(joke_data)

    return func.HttpResponse(body=joke_json, mimetype="application/json", status_code=200)

def process_query(query):
    if REQUIRED_STRING not in query[:3]:
        query.insert(0, "Chuck Norris")

    return " ".join(query[:5])

def load_image(query):
    logging.info(f'Aquiring gif for: {query}')

    api_key = ""
    limit = 1
    url = f'http://api.giphy.com/v1/gifs/search?q={process_query(query.split())}&api_key={api_key}&limit={limit}'

    resp = requests.get(url)
    joke_data = resp.json()

    for i in joke_data.get("data", {}):
        logging.info(i.get("images", {}).get("original", {}))
        yield i.get("images", {}).get("original", {})


# def main(req: func.HttpRequest, msg: func.Out[str]) -> func.HttpResponse:
#     msg.set("This is test. 1227")
#     return func.HttpResponse("This is a test.")
