# パッケージ(jsonなど)追加するものがあれば、追加してOK！
import json

#=====================================#
# 福島県全体の天気情報を戻り値(文字列)とする関数
# 基本情報のJsonデータ: https://www.jma.go.jp/bosai/forecast/data/overview_forecast/070000.json 
# Args: Jsonデータ（追加したいものがあれば、追加してOK！）
# Return: 福島全体の天気データ（文字列）
#=====================================#
def basicWeatherInfo(jsonBasicData):
    return 


#=====================================#
# 会津の天気情報を戻り値(文字列)とする関数
# 詳細情報のJsonデータ：https://www.jma.go.jp/bosai/forecast/data/forecast/070000.json 
# (上記のJsonデータは　https://www.jma.go.jp/bosai/forecast/#area_type=offices&area_code=070000 で見やすくなっています！)
# Args: Jsonデータ（追加したいものがあれば、追加してOK！）
# Return: 会津の天気データ（文字列）
#=====================================#
def detailWeatherInfo(jsonDetailData):
    return 


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