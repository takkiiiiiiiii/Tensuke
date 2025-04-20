# パッケージ(jsonなど)追加するものがあれば、追加してOK！
import json
import requests

#=====================================#
# 福島県全体の天気情報を戻り値(文字列)とする関数
# 基本情報のJsonデータ: https://www.jma.go.jp/bosai/forecast/data/overview_forecast/070000.json 
# Args: Jsonデータ（追加したいものがあれば、追加してOK！）
# Return: 福島全体の天気データ（文字列）
#=====================================#
def basicWeatherInfo(jsonBasicData):
    try:
        response = requests.get(jsonBasicData) # URLにアクセスしてデータを取得
        response.raise_for_status()            # 通信のチェック
        data = response.json()                 # 取得したJSON文字列を Python の辞書形式に変換

        report_datetime = data.get('reportDatatime', '発表日時不明')
        text = data.get('text', '本文なし')

        result = f"【発表日時】{report_datetime}\n【本文】\n{text}"
        return result 
    except requests.RequestException as e:   # エラーを e という名前で受け取る
        return f"基本情報取得中にエラー: {e}"  # 謎の文字列説明 → https://note.nkmk.me/python-f-strings/


#=====================================#
# 会津の天気情報を戻り値(文字列)とする関数
# 詳細情報のJsonデータ：https://www.jma.go.jp/bosai/forecast/data/forecast/070000.json 
# (上記のJsonデータは　https://www.jma.go.jp/bosai/forecast/#area_type=offices&area_code=070000 で見やすくなっています！)
# Args: Jsonデータ（追加したいものがあれば、追加してOK！）
# Return: 会津の天気データ（文字列）
#=====================================#
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
                        if region.get('area', {}).get('name') == '会津':  # '会津' という地域名を見つけたら、その天気予報だけを取り出す
                            times = series.get('timeDefines', [])
                            weathers = region.get('weathers', [])
                            weather_info = '\n'.join(
                                f"{time}: {weather}" for time, weather in zip(times, weathers)  # 複数のリストを同時に組み合わせる関数
                            )
                            return f" [会津の天気予報] \n{weather_info}"
        return "会津地域の天気情報が見つかりませんでした"
    except requests.RequestException as e:

        return f"詳細情報取得中にエラー: {e}"


#=====================================#
# ここは修正しなくて大丈夫です！
#=====================================#
def main():
    jsonBasicData = "https://www.jma.go.jp/bosai/forecast/data/overview_forecast/070000.json"
    jsonDetailData = "https://www.jma.go.jp/bosai/forecast/data/forecast/070000.json"
    basicInfo = basicWeatherInfo(jsonBasicData)
    detailInfo = detailWeatherInfo(jsonDetailData)
    print(f'基本情報: {basicInfo}\n')
    print(f'詳細情報: {detailInfo}')

if __name__ == '__main__':
    main()
