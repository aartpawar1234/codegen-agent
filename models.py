from pydantic import BaseModel
from typing import List

class Todo(BaseModel):
    id: int
    title: str
    done: bool = False

class TodoCreate(BaseModel):
    title: str

class TodoListResponse(BaseModel):
    todos: List[Todo]
