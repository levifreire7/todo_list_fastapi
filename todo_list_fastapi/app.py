from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from todo_list_fastapi.database import get_session
from todo_list_fastapi.models import User
from todo_list_fastapi.schemas import (
    Message,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI(title='To Do List Project')


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return Message(message='Olá, mundo!')


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                detail='Username already exists',
                status_code=HTTPStatus.CONFLICT,
            )
        elif db_user.email == user.email:
            raise HTTPException(
                detail='Email already exists', status_code=HTTPStatus.CONFLICT
            )

    db_user = User(
        username=user.username, email=user.email, password=user.password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', response_model=UserList)
def read_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session = Depends(get_session)
):
    user_db = session.scalar(
        select(User).where(User.id == user_id)
    )

    if not user_db:
        raise HTTPException(
            detail='User not found!',
            status_code=HTTPStatus.NOT_FOUND
        )

    try:
        user_db.email = user.email
        user_db.username = user.username
        user_db.password = user.password

        session.add(user_db)
        session.commit()
        session.refresh(user_db)

        return user_db
    except IntegrityError:
        raise HTTPException(
            detail='Username or Email already exists',
            status_code=HTTPStatus.CONFLICT
        )


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_db = session.scalar(
        select(User).where(User.id == user_id)
    )

    if not user_db:
        raise HTTPException(
            detail='User not found!',
            status_code=HTTPStatus.NOT_FOUND
        )

    session.delete(user_db)
    session.commit()

    return Message(
        message='User deleted!'
    )


@app.get(
    '/users/{user_id}', response_model=UserPublic
)
def read_user__exercicio(
    user_id: int,
    session: Session = Depends(get_session)
):
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            detail='User not found!',
            status_code=HTTPStatus.NOT_FOUND
        )

    return user_db


@app.get('/exercicio-html/', response_class=HTMLResponse)
def exercicio_aula_02():
    return """
    <html>
        <head>
            <title>Olá mundo!</title>
        </head>
        <body>
            <h1>Olá mundo!</h1>
        </body>
    </html>"""
