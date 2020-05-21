# FLASK_APP=run.py FLASK_DEBUG=1 flask run
from flask import Flask, render_template, request, jsonify
import json
import bs4
import os
import sys
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)


@app.route('/')
def main():
    print(sys.version)
    return render_template('index.html')


@app.route('/countries/', methods=["POST"])
def send_data_by_country():
    if request.method == 'POST':
        year = request.json['year']
        country = request.json['country']
        if country == 'Ukraine':
            country = 'UA'
        elif country == 'Russia':
            country = 'RU'
        elif country == 'Belarus':
            country = 'BY'
        elif country == 'Uzbekistan':
            country = 'UZ'
        elif country == 'USA':
            country = 'US'
        url = f"https://calendarific.com/holidays/{year}/{country}"
        # os.system(f"wget {url} -O templates/parse_data.html")
        parse_file = "templates/parse_data.html"
        with open(parse_file, "r") as f:
            content = f.read()
            soup = bs4.BeautifulSoup(content, 'lxml')
            response_content = soup.find("table")
            response_content.find("tbody")['id'] = "event_tbody"

            return jsonify({
                "data": str(response_content)
            })


@app.route('/icoTab/', methods=["POST"])
def send_ico_by_day():
    if request.method == "POST":
        try:
            response = "OK"
            month_day = request.json['month_day']
            input_path_img = str(os.path.abspath('static/img/defaultIcoTab.png'))
            output_path_img = str(os.path.abspath('static/img/icoTab.png'))
            img = Image.open(input_path_img)
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype(os.path.abspath('static/fonts/Aller/Aller_Lt.ttf'), 190)
            if len(str(month_day)) > 1:
                draw.text((17, 40), str(month_day), font=font, fill=(0, 0, 0))
            else:
                draw.text((70, 40), str(month_day), font=font, fill=(0, 0, 0))
            img.save(output_path_img)
            return response
        except Exception as e:
            return str(e)
