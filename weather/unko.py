import json
import requests


def basicWeatherInfo(jsonBasicData):
    try:
        response = requests.get(jsonBasicData) 
        response.raise_for_status()           
        data = response.json()           

        report_datetime = data.get('reportDatatime', '発表日時不明')
        text = data.get('text', '本文なし')

        result = f"【発表日時】{report_datetime}\n【本文】\n{text}"
        return result 
    except requests.RequestException as e:  
        return f"基本情報取得中にエラー: {e}"


def detailWeatherInfo(jsonDetailData):
    try:
        response = requests.get(jsonDetailData)
        response.raise_for_status()
        data = response.json()

        for area in data:
            time_series = area.get('timeSeries', [])  # Jsonファイルの構造に従う
            for series in time_series:
                if 'weathers' in series.get('areas', [{}])[0]:
                    for region in series['areas']:
                        if region.get('area', {}).get('name') == '会津':
                            times = series.get('timeDefines', [])
                            weathers = region.get('weathers', [])
                            weather_info = '\n'.join(
                                f"{time}: {weather}" for time, weather in zip(times, weathers)
                            )
                            return f" [会津の天気予報] \n{weather_info}"
        return "会津地域の天気情報が見つかりませんでした"
    except requests.RequestException as e:

        return f"詳細情報取得中にエラー: {e}"
