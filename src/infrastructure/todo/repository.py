import sqlite3
from typing import List, Optional, TypedDict

# 型の定義（TypeScriptの TodoRow に相当）
class TodoRow(TypedDict):
    id: int
    title: str
    done: bool

# データベースの接続
# FastAPIなどのWebフレームワークで使う場合、スレッド間の共有を許可する設定が必要です
conn = sqlite3.connect("todo.db", check_same_thread=False)
# SQLiteの取得結果を、タプルではなく辞書のように（row["title"]など）扱えるようにする設定
conn.row_factory = sqlite3.Row

# テーブルの作成
conn.execute("""
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        done INTEGER NOT NULL DEFAULT 0
    )
""")
conn.commit()

def _todo_from_sqlite_row(row: sqlite3.Row) -> TodoRow:
    """DBの行データをTodoRow型に変換するヘルパー関数"""
    return {
        "id": row["id"],
        "title": row["title"],
        # 1ならTrue、0ならFalseに変換
        "done": bool(row["done"]) 
    }

def find_all_todos() -> List[TodoRow]:
    cursor = conn.execute("SELECT * FROM todos ORDER BY id DESC")
    rows = cursor.fetchall()
    
    todos: List[TodoRow] = []
    for row in rows:
        todos.append(_todo_from_sqlite_row(row))
    return todos

def insert_todo(title: str) -> TodoRow:
    # プレースホルダ（?）に値を埋め込む場合は、第2引数にタプルで渡します
    cursor = conn.execute("INSERT INTO todos (title) VALUES (?)", (title,))
    conn.commit()  # 書き込み操作の後は必ずコミットが必要
    
    return {
        "id": cursor.lastrowid,  # info.lastInsertRowid に相当
        "title": title,
        "done": False,
    }

def find_todo_by_id(todo_id: int) -> Optional[TodoRow]:
    cursor = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    row = cursor.fetchone()  # get() に相当
    
    if row is None:
        return None
        
    return _todo_from_sqlite_row(row)

def update_todo_done(todo_id: int, done: bool) -> Optional[TodoRow]:
    done_for_sqlite = 1 if done else 0
    
    cursor = conn.execute("UPDATE todos SET done = ? WHERE id = ?", (done_for_sqlite, todo_id))
    conn.commit()
    
    # result.changes === 0 に相当（更新された行数を確認）
    if cursor.rowcount == 0:
        return None
        
    return find_todo_by_id(todo_id)

def delete_todo_by_id(todo_id: int) -> bool:
    cursor = conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    
    # result.changes > 0 に相当
    return cursor.rowcount > 0