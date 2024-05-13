import allure
import pytest
import random
from faker import Faker

from data.defolt_payload import defolt_payload
from data.user_authorization_payload import user_authorization_payload
from data.user_authorization_payload import user_authorization_payload_with_empty
from data.defolt_payload import invalid_add_mem_payload_with_int_in_text
from data.defolt_payload import invalid_add_mem_payload_with_text_empty
from data.user_authorization_payload import invalid_user_authorization_payload_with_int
faker = Faker()


# Тесты для авторизации пользователя

@allure.title('User authorization test')
@allure.story('User authorization')
@allure.feature('User authorization')
@pytest.mark.smoke
def test_user_authorization(authorize_user):
    payload = user_authorization_payload
    authorize_user.authorize_user(payload)
    authorize_user.check_status_code_is_200()
    authorize_user.check_user_name(payload['name'])
    authorize_user.check_token()


@allure.title('User authorization with empty name test')
@allure.story('User authorization with empty name')
@allure.feature('User authorization')
@pytest.mark.regression
def test_user_authorize_with_empty_name(authorize_user):
    authorize_user.authorize_user(user_authorization_payload_with_empty)
    authorize_user.check_status_code_is_200()


@allure.title('User authorization with int name test')
@allure.story('User authorization with int name')
@allure.feature('User authorization')
@pytest.mark.regression
def test_user_authorize_with_int_name(authorize_user):
    authorize_user.authorize_user(invalid_user_authorization_payload_with_int)
    authorize_user.check_status_code_is_400()


@allure.title('User authorization with invalid data')
@pytest.mark.regresion
@pytest.mark.parametrize('name', [
    1, ['User'], {'name': 'User'}, {}, [], dict()])
def test_authorization_with_invalid_user_name(authorize_user, name):
    payload = {
        'name': name,
    }
    authorize_user.authorize_user(payload)
    authorize_user.check_status_code_is_400()


def test_authorization_with_invalid_data(authorize_user):
    payload = {
        'name': 'User',
    }
    authorize_user.authorize_user(payload)
    authorize_user.check_status_code_is_200()


# Тесты на проверки токена

@allure.title('Check activity token test')
@allure.story('Activity token')
@allure.feature('Token')
@pytest.mark.regression
def test_check_activity_token(activity_token, auth_token, user_name):
    activity_token.activity_token(auth_token)
    activity_token.check_status_code_is_200()
    activity_token.check_token_is_active(user_name)


@allure.title('Test: Checking the activity of a nonexistent token')
@allure.story('Invalid token')
@allure.feature('Token')
@pytest.mark.regression
def test_check_invalid_token(activity_token):
    activity_token.activity_token('123')
    activity_token.check_status_code_is_404()
    activity_token.check_text_is_token_not_found()


@allure.title('Checking the activity of an empty token')
@allure.story('Empty token')
@allure.feature('Token')
@pytest.mark.regression
def test_check_empty_token(activity_token):
    activity_token.activity_token(' ')
    activity_token.check_status_code_is_404()
    activity_token.check_text_is_token_not_found()


@allure.title('Check expired token')
@allure.story('Expired token')
@allure.feature('Token')
@pytest.mark.regression
def test_check_expired_token(activity_token):
    expired_token = 'z3rK3gzN2OKjUI4'
    activity_token.activity_token(expired_token)
    activity_token.check_status_code_is_404()


@allure.title('Check token with invalid characters')
@allure.story('Invalid token')
@allure.feature('Token')
@pytest.mark.regression
def test_check_invalid_characters_token(activity_token):
    activity_token.activity_token('!@#$%^&*()')
    activity_token.check_status_code_is_404()
    activity_token.check_text_is_token_not_found()


# Тесты на добавление мема

@allure.title('Add meme test')
@allure.story('Add meme')
@allure.feature('Meme')
@pytest.mark.smoke
def test_add_meme(add_mem, auth_token, user_name, delete_meme):
    payload = defolt_payload
    add_mem.add_mem(auth_token, payload)
    add_mem.check_status_code_is_200()
    add_mem.check_mem_added_by_user(user_name)
    delete_meme.delete_meme(auth_token, add_mem.mem_id)


@allure.title('Test: Check that response match payload')
@allure.story('Check that response match payload')
@allure.feature('Meme')
@pytest.mark.smoke
def test_check_response_match_payload(add_mem, auth_token, user_name, delete_meme):
    payload = defolt_payload
    add_mem.add_mem(auth_token, payload)
    add_mem.check_mem_text(payload['text'])
    add_mem.check_mem_url(payload['url'])
    add_mem.check_mem_tags(payload['tags'])
    add_mem.check_mem_info(payload['info'])
    delete_meme.delete_meme(auth_token, add_mem.mem_id)


@allure.title('Add meme with empty text')
@allure.story('Add meme')
@allure.feature('Meme')
@pytest.mark.regression
def test_add_meme_with_empty_text(add_mem, auth_token, delete_meme):
    payload = invalid_add_mem_payload_with_text_empty
    add_mem.add_mem(auth_token, payload)
    add_mem.check_status_code_is_200()
    add_mem.check_mem_text(payload['text'])
    delete_meme.delete_meme(auth_token, add_mem.mem_id)


@allure.title('Add meme with int text')
@allure.story('Add meme')
@allure.feature('Meme')
@pytest.mark.regression
def test_add_meme_with_int_text(add_mem, auth_token, delete_meme):
    payload = invalid_user_authorization_payload_with_int
    add_mem.add_mem(auth_token, payload)
    add_mem.check_status_code_is_400()


@allure.title('Add meme with invalid data test')
@pytest.mark.regresion
@pytest.mark.parametrize('text, url, tags, info', [
    (1, 'https://9gag.com/gag/a1mvBqR', ['funny', 'dog'], {'rating': 4, 'type': ['gif', 'mp4'], 'user': 'chzel)'}),
    ('Me trying', 'https://9gag.com/gag/a1mvBqR', 'funny', {'rating': 4, 'type': ['gif', 'mp4'], 'user': 'chzel979'}),
    ('Me trying', 1, ['funny', 'dog'], {'rating': 4, 'type': ['gif', 'mp4'], 'user': 'chzel979'}),
    ('Me trying to reach my goals', 'https://9gag.com/gag/a1mvBqR', ['funny', 'dog'], ['rating', 'type', 'user'])])
def test_add_meme_with_invalid_data(add_mem, auth_token, text, url, tags, info, delete_meme):
    payload = {
        "text": text,
        "url": url,
        "tags": tags,
        "info": info
    }
    add_mem.add_mem(auth_token, payload)
    add_mem.check_status_code_is_400()
    add_mem.check_message_invalid_parameters()


# Тесты на получение мема по ID

@allure.title('Get meme by id test')
@allure.story('Get meme by id')
@allure.feature('Meme')
@pytest.mark.smoke
def test_get_mem_by_id(get_mem_by_id, auth_token, meme_id):
    get_mem_by_id.get_mem_by_id(auth_token, meme_id)
    get_mem_by_id.check_status_code_is_200()
    get_mem_by_id.check_mem_id(meme_id)


@allure.title('Check meme text, when get meme by id')
@allure.story('Get meme by id')
@allure.feature('Meme')
@pytest.mark.smoke
def test_check_meme_text_match(get_mem_by_id, auth_token, meme_id):
    get_mem_by_id.get_mem_by_id(auth_token, meme_id)
    get_mem_by_id.check_mem_text("Me trying to reach my goals")


@allure.title('Check data keys, when get meme by id')
@allure.story('Get meme by id')
@allure.feature('Meme')
@pytest.mark.smoke
def test_check_data_keys(get_mem_by_id, auth_token, meme_id):
    get_mem_by_id.get_mem_by_id(auth_token, meme_id)
    get_mem_by_id.check_keys_in_data()


@allure.title('Check get meme by invalid meme id')
@allure.story('Get meme by id')
@allure.feature('Meme')
@pytest.mark.regression
def test_get_meme_by_invalid_id(get_mem_by_id, auth_token, meme_id):
    get_mem_by_id.get_mem_by_id(auth_token, meme_id)
    get_mem_by_id.get_mem_by_id(auth_token, 0)
    get_mem_by_id.check_status_code_is_404()


@allure.title('Check get meme by invalid token')
@allure.story('Get meme by id')
@allure.feature('Meme')
@pytest.mark.regression
def test_get_meme_by_invalid_token(get_mem_by_id, auth_token, meme_id):
    get_mem_by_id.get_mem_by_id('123', meme_id)
    get_mem_by_id.check_status_code_is_401()


# Тесты на получение всех мемов

@allure.title('Get all memes test')
@allure.story('Get all memes')
@allure.feature('Meme')
@pytest.mark.smoke
def test_get_all_memes(get_all_memes, auth_token):
    get_all_memes.get_all_memes(auth_token)
    get_all_memes.check_status_code_is_200()


@allure.title('Check uniqueness ids, when get all memes')
@allure.story('Get all memes')
@allure.feature('Meme')
@pytest.mark.regression
def test_check_uniqueness_ids(get_all_memes, auth_token):
    get_all_memes.get_all_memes(auth_token)
    get_all_memes.check_uniqueness_ids()
    get_all_memes.check_memes_count()


@allure.title('Check data keys, when get all memes')
@allure.story('Get all memes')
@allure.feature('Meme')
@pytest.mark.regression
def test_check_data_keys_in_memes(get_all_memes, auth_token):
    get_all_memes.get_all_memes(auth_token)
    get_all_memes.check_keys_in_data()


@allure.title('Check data types, when get all memes')
@allure.story('Get all memes')
@allure.feature('Meme')
@pytest.mark.regression
def test_check_data_types(get_all_memes, auth_token):
    get_all_memes.get_all_memes(auth_token)
    get_all_memes.check_mem_text_is_str()
    get_all_memes.check_mem_url_is_str()
    get_all_memes.check_mem_tags_is_list()
    get_all_memes.check_mem_info_is_dict()
    get_all_memes.check_mem_updated_by_is_str()


@allure.title('Check memes is int, when get all memes')
@allure.story('Get all memes')
@allure.feature('Meme')
@pytest.mark.bug('Id\'s is int after change meme')
def test_check_meme_id_is_int(get_all_memes, auth_token):
    get_all_memes.get_all_memes(auth_token)
    get_all_memes.check_mem_id_is_int()


@allure.title('Check get all memes, when token is invalid')
@allure.story('Get all memes')
@allure.feature('Meme')
@pytest.mark.regression
def test_check_get_all_memes_by_invalid_token(get_all_memes, auth_token):
    get_all_memes.get_all_memes('123')
    get_all_memes.check_status_code_is_401()


# Тесты на удаление мема

@allure.title('Delete meme test')
@allure.story('Delete meme')
@allure.feature('Meme')
@pytest.mark.smoke
def test_delete_meme(delete_meme, auth_token, meme_id):
    delete_meme.delete_meme(auth_token, meme_id)
    delete_meme.check_status_code_is_200()
    delete_meme.check_delete_meme(meme_id)


@allure.title('Test: Get meme after deleted it')
@allure.story('Get meme after deleted it')
@allure.feature('Meme')
@pytest.mark.smoke
def test_get_meme_after_delete(delete_meme, auth_token, meme_id, get_mem_by_id):
    delete_meme.delete_meme(auth_token, meme_id)
    delete_meme.check_status_code_is_200()
    get_mem_by_id.get_mem_by_id(auth_token, meme_id)
    get_mem_by_id.check_status_code_is_404()


@allure.title('Test: Delete meme with invalid user id')
@allure.story('Delete meme with invalid user id')
@allure.feature('Meme')
@pytest.mark.regression
def test_delete_meme_with_invalid_id(delete_meme, auth_token, meme_id):
    delete_meme.delete_meme(auth_token, '')
    delete_meme.check_status_code_is_404()


@allure.title('Test: Delete meme with invalid token')
@allure.story('Delete meme with invalid token')
@allure.feature('Meme')
@pytest.mark.regression
def test_delete_meme_with_invalid_token(delete_meme, auth_token, meme_id):
    delete_meme.delete_meme('123', meme_id)
    delete_meme.check_status_code_is_401()


@allure.title('Test: Delete meme with invalid meme id')
@allure.story('Delete meme with invalid meme id')
@allure.feature('Meme')
@pytest.mark.regression
def test_delete_meme_with_invalid_meme_id(delete_meme, auth_token, meme_id):
    delete_meme.delete_meme(auth_token, 0)
    delete_meme.check_status_code_is_404()


# Тесты на изменение мема

@allure.title('Change meme test')
@allure.story('Change meme')
@allure.feature('Meme')
@pytest.mark.parametrize('text, url, info', [
    ('1', '.com', {'rating': random.randint(0, 10), 'type': [5, 'avi'], 'user': faker.name()}),
    ('Name' * 10, "https://google.com'", {'rating': random.randint(-1, 11), 'type': [{}, 'JPEG'], 'user': '*/-_-\\'}),
])
@pytest.mark.bug('Id type is str, after changing meme')
def test_change_meme(auth_token, meme_id, change_meme, user_name, text, url, info):
    payload = {
        "id": meme_id,
        "text": text,
        "url": url,
        "tags": ['funny', 'dog'],
        "info": info
    }
    change_meme.change_meme(auth_token, meme_id, payload)
    change_meme.check_status_code_is_200()
    change_meme.check_mem_text(text)
    change_meme.check_mem_url(url)
    change_meme.check_mem_tags(payload['tags'])
    change_meme.check_mem_info(info)
    change_meme.check_updated_by_user(user_name)
    change_meme.check_mem_id(meme_id)


@allure.title('Test: Change one meme value')
@allure.story('Change one meme value')
@allure.feature('Meme')
@pytest.mark.regression
def test_change_one_meme_value(change_meme, auth_token, meme_id):
    payload = {'text': 'Hello'}
    change_meme.change_meme(auth_token, meme_id, payload)
    change_meme.check_status_code_is_400()


@allure.title('Test: Change text meme to int')
@allure.story('Change text meme to int')
@allure.feature('Meme')
@pytest.mark.regression
def test_change_text_meme_to_int(change_meme, auth_token, meme_id):
    change_meme.change_meme(auth_token, meme_id, invalid_add_mem_payload_with_int_in_text)
    change_meme.check_status_code_is_400()


@allure.title('Test: Change meme with empty id in payload')
@allure.story('Change meme with empty id in payload')
@allure.feature('Meme')
@pytest.mark.regression
def test_change_meme_with_empty_id(change_meme, auth_token, meme_id):
    payload = {
        "id": '',
        "text": 'Hello',
        "url": 'https://google.com',
        "tags": ['funny', 'dog'],
        "info": {'rating': 4, 'type': ['gif', 'mp4'], 'user': 'chzel979'}
    }
    change_meme.change_meme(auth_token, meme_id, payload)
    change_meme.check_status_code_is_400()


@allure.title('Test: Change meme with str id in payload')
@allure.story('Change meme with str id in payload')
@allure.feature('Meme')
@pytest.mark.regression
def test_change_meme_with_str_id(change_meme, auth_token, meme_id):
    payload = {
        "id": str(meme_id),
        "text": 'Hello',
        "url": 'https://google.com',
        "tags": ['funny', 'dog'],
        "info": {'rating': 4, 'type': ['gif', 'mp4'], 'user': 'chzel979'}
    }
    change_meme.change_meme(auth_token, meme_id, payload)
    change_meme.check_status_code_is_400()


@allure.title('Test: Change meme with invalid token')
@allure.story('Change meme with invalid token')
@allure.feature('Meme')
@pytest.mark.regression
def test_change_meme_with_invalid_token(change_meme, auth_token, meme_id):
    payload = {
        "id": meme_id,
        "text": 'Hello',
        "url": 'https://google.com',
        "tags": ['funny', 'dog'],
        "info": {'rating': 4, 'type': ['gif', 'mp4'], 'user': 'chzel979'}
    }
    change_meme.change_meme('123', meme_id, payload)
    change_meme.check_status_code_is_401()


@allure.title('Test: Change meme with invalid user id')
@allure.story('Change meme with invalid user id')
@allure.feature('Meme')
@pytest.mark.regression
def test_change_meme_with_invalid_id(change_meme, auth_token, meme_id):
    payload = {
        "id": meme_id,
        "text": 'Hello',
        "url": 'https://google.com',
        "tags": ['funny', 'dog'],
        "info": {'rating': 4, 'type': ['gif', 'mp4'], 'user': 'chzel979'}
    }
    change_meme.change_meme(auth_token, 0, payload)
    change_meme.check_status_code_is_404()
