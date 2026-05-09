from flask import Flask, render_template
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = "12d58f38afab181ee27e3d1f1cb83b44e01fdede2b000778d197488640d1c6a9"

# 전북 익산 좌표
NX = 63
NY = 89

def get_weather():
    now = datetime.now()
    base_date = now.strftime("%Y%m%d")
    base_time = "0200"

    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"

    params = {
        "serviceKey": API_KEY,
        "numOfRows": "1000",
        "pageNo": "1",
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": NX,
        "ny": NY
    }

    response = requests.get(url, params=params)
    data = response.json()

    items = data["response"]["body"]["items"]["item"]

    weather = {
        "temp": None,
        "sky": None,
        "pty": None
    }

    for item in items:
        if item["category"] == "TMP":
            weather["temp"] = item["fcstValue"]
        elif item["category"] == "SKY":
            weather["sky"] = item["fcstValue"]
        elif item["category"] == "PTY":
            weather["pty"] = item["fcstValue"]

    return weather


@app.route('/')
def index():
    weather = get_weather()

    sky_map = {
        "1": "맑음 ☀️",
        "3": "구름 많음 ⛅",
        "4": "흐림 ☁️"
    }

    pty_map = {
        "0": "강수 없음",
        "1": "비 🌧",
        "2": "비/눈 🌨",
        "3": "눈 ❄️"
    }

    sky = sky_map.get(weather["sky"], "")
    rain = pty_map.get(weather["pty"], "")

    return render_template("index.html",
                           temp=weather["temp"],
                           sky=sky,
                           rain=rain)


if __name__ == '__main__':
    app.run(debug=True)
