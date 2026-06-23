import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base, SessionLocal
from src.models import Todo
from src.schemas import TodoCreate, TodoUpdate
from src.crud import create_todo, get_todo, get_all_todos, update_todo, delete_todo

@pytest.fixture(scope='module')
def test_db():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(engine)


def test_create_todo(test_db):
    todo_data = TodoCreate(title='Test Todo', description='Test Description')
    todo = create_todo(test_db, todo_data)
    assert todo.id is not None
    assert todo.title == todo_data.title


def test_get_todo(test_db):
    todo = get_todo(test_db, 1)
    assert todo is not None
    assert todo.title == 'Test Todo'


def test_get_all_todos(test_db):
    todos = get_all_todos(test_db)
    assert len(todos) == 1


def test_update_todo(test_db):
    update_data = TodoUpdate(title='Updated Todo')
    updated_todo = update_todo(test_db, 1, update_data)
    assert updated_todo.title == 'Updated Todo'


def test_delete_todo(test_db):
    deleted_todo = delete_todo(test_db, 1)
    assert deleted_todo is not None
    assert get_todo(test_db, 1) is None
