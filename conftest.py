import pytest
import logging
import os

from endpoints.activity_token import ActivityToken
from endpoints.authorize_user import AuthorizeUser
from endpoints.add_mem import AddMem
from endpoints.get_mem_by_id import GetMemeById
from endpoints.delete_mem import DeleteMeme
from endpoints.get_mems import GetAllMemes
from endpoints.change_mem import ChangeMeme


logging.getLogger(__name__)

TOKEN_FILE_PATH = 'auth_token.txt'


def load_token():
    if os.path.exists(TOKEN_FILE_PATH):
        with open(TOKEN_FILE_PATH, 'r', encoding='UTF-8') as file:
            return file.read()
    return None


def save_token(token):
    with open(TOKEN_FILE_PATH, 'w', encoding='UTF-8') as file:
        file.write(token)


def is_token_valid(token):
    active_token = ActivityToken()
    active_token.activity_token(token)
    return active_token.status_code == 200


@pytest.fixture(scope='session', autouse=True)
def auth_token(authorize_user):
    token = load_token()
    if token and is_token_valid(token):
        return token
    else:
        authorize_user.authorize_user()
        assert authorize_user.response.status_code == 200
        token = authorize_user.token
        save_token(token)
        return token


@pytest.fixture()
def meme_id(auth_token, add_mem, delete_meme):
    add_mem.add_mem(auth_token)
    meme_id = add_mem.mem_id
    yield meme_id
    delete_meme.delete_meme(auth_token, meme_id)
    assert delete_meme.check_status_code_is_200


@pytest.fixture()
def user_name(authorize_user):
    authorize_user.authorize_user()
    user_name = authorize_user.user_name
    return user_name


@pytest.fixture()
def activity_token():
    return ActivityToken()


@pytest.fixture()
def authorize_user():
    return AuthorizeUser()


@pytest.fixture()
def add_mem():
    return AddMem()


@pytest.fixture()
def get_mem_by_id():
    return GetMemeById()


@pytest.fixture()
def delete_meme():
    return DeleteMeme()


@pytest.fixture()
def get_all_memes():
    return GetAllMemes()


@pytest.fixture()
def change_meme():
    return ChangeMeme()
