from flask import Flask, make_response
import random
import logging
import os

app = Flask(__name__)
logging.basicConfig()
logger = logging.getLogger(__name__)

class InvalidBearFood(Exception):
    pass

@app.route('/', methods=['GET'])
def index():
    gif = fetch_a_bear()
    response = format_bear_response(gif)
    return response, 200

@app.route('/health', methods=['GET'])
def health():
    return "Hi Shawn!!", 200

def fetch_a_bear():
    lines = open('bears.txt').read().splitlines()
    return random.choice(lines)

def format_bear_response(gif_link):
    html = f'''<html>
    <head>
        <title>Some Bears...</title>
    </head>
    <body>
        <img src="{gif_link}"/>
    </body>
</html>'''
    response = make_response(html)                                           
    response.headers['Content-Type'] = 'text/html; charset=utf-8'  
    return response

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