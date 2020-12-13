import os

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import Response, RedirectResponse

from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException

fake_db = {
    'john@doe.com': {
        'name': 'John',
        'surname': 'Doe',
        'email': 'john@doe.com',
        'password': 'hunter2'
    },

    'sandra@johnson.com': {
        'name': 'Sandra',
        'surname': 'Johnson',
        'email': 'sandra@johnson.com',
        'password': 'sandra1243'
    }
}
SECRET = os.urandom(24).hex()
TOKEN_URL = '/auth/token'


def load_user(email: str):
    user = fake_db.get(email)
    if not user:
        return None

    return user


class NotAuthenticatedException(Exception):
    pass


def handle_exc(request, exc):
    print(request, exc)
    return RedirectResponse(url='/redirect')


# app setup
app = FastAPI()
app.add_exception_handler(NotAuthenticatedException, handle_exc)

# Manager setup
manager = LoginManager(SECRET, tokenUrl=TOKEN_URL)
manager.user_loader(load_user)


# routes

@app.post(TOKEN_URL)
def login(response: Response, data: OAuth2PasswordRequestForm = Depends()):
    user_identifier = data.username
    password = data.password

    user = load_user(user_identifier)
    if not user:
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=user_identifier)
    )

    return {'access_token': access_token, 'token_type': 'bearer'}


@app.get('/redirect')
def redirected_here():
    return {'data': 'redirected'}


@app.get('/protected')
def protected(_=Depends(manager)):
    return {'status': 'Success'}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
