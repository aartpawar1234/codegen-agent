from pydantic import BaseModel

class TodoBase(BaseModel):
    title: str
    description: str = ""
    completed: int = 0

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: str = None
    description: str = None
    completed: int = None

class TodoResponse(TodoBase):
    id: int

    class Config:
        orm_mode = True
