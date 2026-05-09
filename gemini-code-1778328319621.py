from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def get_air_quality():
    # 제공해주신 인증키 사용
    auth_key = "12d58f38afab181ee27e3d1f1cb83b44e01fdede2b000778d197488640d1c6a9"
    url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty"
    
    params = {
        'serviceKey': auth_key,
        'returnType': 'json',
        'numOfRows': '10',
        'pageNo': '1',
        'sidoName': '전북', # 학교 위치인 전북 기준
        'ver': '1.0'
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        items = data['response']['body']['items']
        # 첫 번째 측정소 데이터 가져오기
        air_data = items[0] 
    except:
        air_data = {"stationName": "데이터 오류", "pm10Value": "-", "pm25Value": "-", "khaiGrade": "-"}

    return render_template('index.html', air=air_data)

if __name__ == '__main__':
    app.run(debug=True)