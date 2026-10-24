#Todo型の定義をする
from dataclasses import dataclass

@dataclass
class Todo:
    id: int
    title: str
    done: bool

# Todoの配列を作成する
todos: list[Todo] = [
    Todo(id=1, title="牛乳を買う", done=False),
    Todo(id=2, title="日報を書く", done=True),
    Todo(id=3, title="TypeScriptを学ぶ", done=False),
]

# todoを追加する関数
def add_todo(todos: list[Todo], title: str) -> list[Todo]:
    new_id = len(todos) + 1
    new_todo = Todo(id=new_id, title=title, done=False)
    # リストを結合して新しいリストを作って返す（TypeScriptの [...todos, newTodo] に相当）
    return [*todos, new_todo]

updated_todos = add_todo(todos, "掃除をする")

#一覧を表示する関数
def show_todos(todos: list[Todo]) -> None:
    for todo in updated_todos:
        status = "✅" if todo.done else "⬜"
        print(f"{status} [{todo.id}] {todo.title}")

#実行
print("=== TODO 一覧 ===")
show_todos(updated_todos)