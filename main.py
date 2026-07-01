from fastapi import FastAPI, HTTPException
from typing import List
from models import Todo, TodoCreate

app = FastAPI()

todos = {}
next_id = 1

@app.post("/todos", response_model=Todo)
async def create_todo(todo: TodoCreate):
    global next_id
    new_todo = Todo(id=next_id, title=todo.title)
    todos[next_id] = new_todo
    next_id += 1
    return new_todo

@app.get("/todos", response_model=List[Todo])
async def list_todos():
    return list(todos.values())

@app.put("/todos/{id}")
async def mark_done(id: int):
    if id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos[id].done = True

@app.delete("/todos/{id}")
async def delete_todo(id: int):
    if id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos[id]