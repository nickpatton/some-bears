from flask import Flask, make_response, render_template
import random
import logging
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
logging.basicConfig()
logger = logging.getLogger(__name__)


class InvalidBearFood(Exception):
    pass


def fetch_a_bear():
    lines = open('bears.txt').read().splitlines()
    return random.choice(lines)


@app.route('/', methods=['GET'])
def index():
    gif_link = fetch_a_bear()
    return render_template('index.jinja', gif_link=gif_link)


@app.route('/refresh_bear', methods=['POST'])
def refresh_bear():
    gif_link = fetch_a_bear()
    return f"<img src={gif_link} />"


@app.route('/health', methods=['GET'])
def health():
    return "Hi Shawn!!", 200


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
