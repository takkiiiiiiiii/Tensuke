import json

# JSONファイルの読み込み
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# JSONデータの解析と出力
def print_people_info(data):
    for key, person in data.items():
        print(f"{key}:")
        print(f"  名前: {person['name']}")
        print(f"  年齢: {person['age']}")
        print(f"  職業: {person['job']}")
        print("-")

if __name__ == "__main__":
    file_path = "./human.json"  # JSONファイルのパス
    people_data = load_json(file_path)
    print_people_info(people_data)

