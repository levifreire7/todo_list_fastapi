import asyncio
import sys
from http import HTTPStatus

from fastapi import FastAPI

from todo_list_fastapi.routers import auth, todos, users
from todo_list_fastapi.schemas import Message

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI(title='To Do List Project')

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
async def read_root():
    return Message(message='Olá, mundo!')
