from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# 1. データベースの準備（sqlite3）
conn = sqlite3.connect("todo.db", check_same_thread=False)
conn.row_factory = sqlite3.Row
conn.execute("""
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        done INTEGER NOT NULL DEFAULT 0
    )
""")
conn.commit()

# 2. POSTで受け取るJSONデータの型定義
class TodoCreateRequest(BaseModel):
    title: str

# 3. APIエンドポイント（一覧取得）
@app.get("/api/todos")
def get_todos():
    cursor = conn.execute("SELECT * FROM todos ORDER BY id DESC")
    rows = cursor.fetchall()
    return [{"id": row["id"], "title": row["title"], "done": bool(row["done"])} for row in rows]

# 4. APIエンドポイント（新規作成）
@app.post("/api/todos", status_code=201)
def post_todos(req: TodoCreateRequest):
    title = req.title.strip()
    if len(title) == 0 or len(title) > 100:
        raise HTTPException(status_code=400, detail="タイトルは1〜100文字で入力してください")
        
    cursor = conn.execute("INSERT INTO todos (title) VALUES (?)", (title,))
    conn.commit()
    return {"id": cursor.lastrowid, "title": title, "done": False}

# 5. APIエンドポイント（完了状態の切り替え）
@app.put("/api/todos/{todo_id}")
def put_todos(todo_id: int):
    cursor = conn.execute("SELECT done FROM todos WHERE id = ?", (todo_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="見つかりません")
        
    # 現在が0なら1に、1なら0に切り替える
    new_done = 0 if row["done"] else 1
    conn.execute("UPDATE todos SET done = ? WHERE id = ?", (new_done, todo_id))
    conn.commit()
    return {"id": todo_id, "done": bool(new_done)}

# 6. APIエンドポイント（削除）
@app.delete("/api/todos/{todo_id}")
def delete_todos(todo_id: int):
    cursor = conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="見つかりません")
    return {"message": "削除しました"}

# 7. 静的ディレクトリの配信（必ず一番下に書く）
app.mount("/", StaticFiles(directory="public", html=True), name="public")