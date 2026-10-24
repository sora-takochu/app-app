from pydantic import BaseModel

class TodoRow(BaseModel):
    id: int
    title: str
    done: bool