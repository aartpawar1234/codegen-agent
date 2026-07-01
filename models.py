from pydantic import BaseModel

class Todo(BaseModel):
    id: int
    title: str
    done: bool = False

class TodoCreate(BaseModel):
    title: str