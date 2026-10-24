from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Any

# ※実際のフォルダ構成に合わせてimportパスは調整してください
from application.todo.service import (
    create_todo,
    list_todos,
    remove_todo,
    toggle_todo_done,
)

app = FastAPI()

# POSTリクエストのJSON（req.body）を受け取るための型定義
class TodoCreateRequest(BaseModel):
    title: Any # サービス層のvalidate_titleで検証するためAnyとしています

@app.get("/api/todos")
def get_todos():
    # res.json(listTodos()) に相当
    return list_todos()

@app.post("/api/todos", status_code=201)
def post_todos(req: TodoCreateRequest):
    try:
        todo = create_todo(req.title)
        return todo
    except ValueError as error:
        # validate_titleで発生したエラーを400として返す
        raise HTTPException(status_code=400, detail=str(error))

@app.put("/api/todos/{todo_id}")
def put_todos(todo_id: int):
    # Expressの req.params.id に相当する部分は、関数の引数(todo_id: int)として自動で数値化されて渡されます
    todo = toggle_todo_done(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="見つかりません")
    return todo

@app.delete("/api/todos/{todo_id}")
def delete_todos(todo_id: int):
    deleted = remove_todo(todo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="見つかりません")
    return {"message": "削除しました"}

# 静的ファイルの配信（Expressの express.static に相当）
# ※APIのルート（/api/...）と競合しないよう、一番最後に記述します
app.mount("/", StaticFiles(directory="public", html=True), name="public")