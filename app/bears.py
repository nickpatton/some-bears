from flask import Flask, make_response, render_template
import random
import logging
import os
import requests

app = Flask(__name__, template_folder='templates', static_folder='static')
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class InvalidBearFood(Exception):
    pass

def fetch_a_bear():
    bear_gif_links = open('bears.txt').read().splitlines()
    return random.choice(bear_gif_links)

@app.route('/', methods=['GET'])
def index():
    gif_link = fetch_a_bear()
    return render_template('index.jinja', gif_link=gif_link)

@app.route('/refresh_bear', methods=['POST'])
def refresh_bear():
    gif_link = fetch_a_bear()
    logger.info("rendering bear gif: %s", gif_link)
    return f"<img src={gif_link} />"

@app.route('/health', methods=['GET'])
def health():
    return "Hi Bear!!", 200

# Test DNS resolution/ability to connect to an external endpoint
@app.route('/external_request', methods=['GET'])
def external_request():
    response = requests.get(
        "https://api.coingecko.com/api/v3/coins/markets/?vs_currency=usd&ids=bitcoin")
    logger.info("response code from CoinGecko: %s", response.status_code)
    return response.json(), response.status_code

@app.route('/exception', methods=['GET'])
def exception():
    try:
        food = 'almonds'
        if food not in ['honey', 'peanutbutter', 'pancakes', 'maple-syrup']:
            raise InvalidBearFood(f'{food} is/are NOT valid food for bears!')
    except InvalidBearFood:
        logger.critical("You tried to feed the bear invalid food.")
        raise

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
