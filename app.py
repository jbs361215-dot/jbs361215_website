from flask import Flask
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

    temp = ""
    sky = ""
    pty = ""

    for item in items:
        if item["category"] == "TMP":
            temp = item["fcstValue"]
        elif item["category"] == "SKY":
            sky = item["fcstValue"]
        elif item["category"] == "PTY":
            pty = item["fcstValue"]

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

    sky_text = sky_map.get(sky, "")
    rain_text = pty_map.get(pty, "")

    return temp, sky_text, rain_text


@app.route('/')
def index():
    temp, sky, rain = get_weather()

    html = f"""
    <html>
    <head>
        <title>전라북도 날씨</title>
        <style>
            body {{
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                text-align: center;
                font-family: Arial;
                margin-top: 100px;
            }}
            .card {{
                background: rgba(255,255,255,0.2);
                padding: 30px;
                border-radius: 20px;
                display: inline-block;
            }}
            .temp {{
                font-size: 50px;
                font-weight: bold;
            }}
        </style>
    </head>

    <body>
        <h1>📍 전라북도 날씨</h1>

        <div class="card">
            <div class="temp">{temp}°C</div>
            <p>{sky}</p>
            <p>{rain}</p>
        </div>
    </body>
    </html>
    """

    return html


if __name__ == '__main__':
    app.run(debug=True)
