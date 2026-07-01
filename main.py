from fastapi import FastAPI, HTTPException
from models import Todo, TodoCreate, TodoListResponse
from typing import Dict

app = FastAPI()

todos: Dict[int, Todo] = {}
next_id = 1

@app.post("/todos", response_model=Todo)
async def create_todo(todo_create: TodoCreate):
    global next_id
    if not todo_create.title:
        raise HTTPException(status_code=422, detail="Title cannot be empty")
    todo = Todo(id=next_id, title=todo_create.title)
    todos[next_id] = todo
    next_id += 1
    return todo

@app.get("/todos", response_model=TodoListResponse)
async def list_todos():
    return TodoListResponse(todos=list(todos.values()))

@app.put("/todos/{id}")
async def mark_todo_done(id: int):
    if id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos[id].done = True

@app.delete("/todos/{id}")
async def delete_todo(id: int):
    if id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos[id]
