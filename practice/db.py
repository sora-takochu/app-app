import sqlite3
from typing import TypedDict, List

# --- アプリで使う TODO の形 ---
class TodoRow(TypedDict):
    id: int
    title: str
    done: bool

# --- データベースに接続 ---
conn = sqlite3.connect("todo.db")
# better-sqlite3のように、カラム名（row["title"]など）でアクセスできるようにする魔法の設定
conn.row_factory = sqlite3.Row

# --- テーブルを作る（なければ作る） ---
conn.execute("""
  CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done INTEGER NOT NULL DEFAULT 0
  )
""")

# --- TODO を追加する ---
def add_todo(title: str) -> None:
    # SQLインジェクションを防ぐため、? に値を入れる場合はタプル (title,) で渡します
    conn.execute("INSERT INTO todos (title) VALUES (?)", (title,))
    # Pythonのsqlite3では、データの追加・更新・削除後は commit() が必須です
    conn.commit()
    print(f"追加: {title}")

# --- TODO 一覧を取得する ---
def get_all_todos() -> List[TodoRow]:
    cursor = conn.execute("SELECT * FROM todos")
    rows = cursor.fetchall()  # stmt.all() に相当
    
    todos: List[TodoRow] = []
    for row in rows:
        # bool() を使うと、0はFalse、1以上の数値はTrueに変換されます
        todos.append({
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"])
        })
    return todos

# --- TODO 一覧を表示する ---
def show_todos() -> None:
    todos = get_all_todos()
    if not todos:
        print("TODOはありません")
        return
        
    for todo in todos:
        status = "✅" if todo["done"] else "⬜"
        print(f"{status} [{todo['id']}] {todo['title']}")

# --- 実行する ---
if __name__ == "__main__":
    print("=== TODO を追加 ===")
    add_todo("牛乳を買う")
    add_todo("日報を書く")
    add_todo("掃除をする")

    print("\n=== TODO 一覧 ===")
    show_todos()

    # --- データベースを閉じる ---
    conn.close()