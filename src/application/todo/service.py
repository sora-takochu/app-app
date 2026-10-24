from typing import List, Optional, Any

# ※実際のフォルダ構成に合わせてimportパス（from以降）は調整してください
from domain.todo.types import TodoRow
from domain.todo.validate import validate_title
from infrastructure.todo.repository import (
    delete_todo_by_id,
    find_all_todos,
    find_todo_by_id,
    insert_todo,
    update_todo_done,
)

def list_todos() -> List[TodoRow]:
    return find_all_todos()

def create_todo(raw_title: Any) -> TodoRow:
    title = validate_title(raw_title)
    return insert_todo(title)

def toggle_todo_done(todo_id: int) -> Optional[TodoRow]:
    todo = find_todo_by_id(todo_id)
    
    if not todo:
        return None
        
    # 前回定義したTodoRowは辞書（TypedDict）なので、
    # todo.done ではなく todo["done"] で値にアクセスします
    return update_todo_done(todo_id, not todo["done"])

def remove_todo(todo_id: int) -> bool:
    return delete_todo_by_id(todo_id)