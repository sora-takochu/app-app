import requests
from typing import TypedDict, List

# TypeScriptの `type` に相当する型定義
class TodoFromAPI(TypedDict):
    userId: int
    id: int
    title: str
    completed: bool

def fetch_todos() -> None:
    print("APIからTODOを取得中...")

    # APIからデータを取得
    # URLパラメータの ?_limit=5 は params 引数で渡すことも可能です
    response = requests.get("https://jsonplaceholder.typicode.com/todos?_limit=5")
    
    # JSONレスポンスをPythonの辞書（dict）のリストに変換
    todos: List[TodoFromAPI] = response.json()

    print(f"{len(todos)} 件取得しました\n")

    # 取得したTODOをループ処理
    for todo in todos:
        # Pythonの三項演算子（条件式）を使ってシンプルに記述
        status = "✅" if todo["completed"] else "⬜"
        
        # f-string を使って文字列をフォーマット
        print(f"{status} [{todo['id']}] {todo['title']}")

# スクリプトとして直接実行された場合のみ関数を呼び出す
if __name__ == "__main__":
    fetch_todos()