import allure
import pytest
import random
from faker import Faker

from data.defolt_payload import defolt_payload
from data.user_authorization_payload import user_authorization_payload
from data.user_authorization_payload import user_authorization_payload_with_empty
from data.user_authorization_payload import user_authorization_payload_without_name
from data.defolt_payload import invalid_add_mem_payload_with_int_in_text
from data.defolt_payload import invalid_add_mem_payload_with_text_empty
faker = Faker()


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
    authorize_user.authorize_user(user_authorization_payload_with_empty)
    authorize_user.check_status_code_is_200()
    authorize_user.authorize_user(user_authorization_payload_without_name)
    authorize_user.check_status_code_is_400()


@allure.title('Check activity token test')
@allure.story('Activity token')
@allure.feature('Token')
@pytest.mark.regression
def test_check_activity_token(activity_token, auth_token, user_name):
    activity_token.activity_token(auth_token)
    activity_token.check_status_code_is_200()
    activity_token.check_token_is_active(user_name)
    activity_token.activity_token('123')
    activity_token.check_status_code_is_404()
    activity_token.check_text_is_token_not_found()


@allure.title('Add meme test')
@allure.story('Add meme')
@allure.feature('Meme')
@pytest.mark.smoke
def test_add_meme(add_mem, auth_token, user_name):
    payload = defolt_payload
    add_mem.add_mem(auth_token, payload)
    add_mem.check_status_code_is_200()
    add_mem.check_updated_by_user(user_name)
    add_mem.check_mem_text(payload['text'])
    add_mem.check_mem_url(payload['url'])
    add_mem.check_mem_tags(payload['tags'])
    add_mem.check_mem_info(payload['info'])
    add_mem.add_mem(auth_token, invalid_add_mem_payload_with_text_empty)
    add_mem.check_status_code_is_200()


@allure.title('Get meme by id test')
@allure.story('Get meme by id')
@allure.feature('Meme')
@pytest.mark.smoke
def test_get_mem_by_id(get_mem_by_id, auth_token, meme_id):
    get_mem_by_id.get_mem_by_id(auth_token, meme_id)
    get_mem_by_id.check_status_code_is_200()
    get_mem_by_id.check_mem_id(meme_id)
    get_mem_by_id.check_mem_text('Me trying to reach my goals')
    get_mem_by_id.check_keys_in_data()
    get_mem_by_id.get_mem_by_id(auth_token, 0)
    get_mem_by_id.check_status_code_is_404()
    get_mem_by_id.get_mem_by_id('123', meme_id)
    get_mem_by_id.check_status_code_is_401()


@allure.title('Get all memes test')
@allure.story('Get all memes')
@allure.feature('Meme')
@pytest.mark.smoke
def test_get_all_memes(get_all_memes, auth_token):
    get_all_memes.get_all_memes(auth_token)
    get_all_memes.check_status_code_is_200()
    get_all_memes.check_uniqueness_ids()
    get_all_memes.check_memes_count()
    get_all_memes.check_keys_in_data()
    get_all_memes.get_all_memes('123')
    get_all_memes.check_status_code_is_401()


@allure.title('Delete meme test')
@allure.story('Delete meme')
@allure.feature('Meme')
@pytest.mark.smoke
def test_delete_meme(auth_token, delete_meme, meme_id, get_mem_by_id):
    delete_meme.delete_meme(auth_token, meme_id)
    delete_meme.check_status_code_is_200()
    delete_meme.check_delete_meme(meme_id)
    get_mem_by_id.get_mem_by_id(auth_token, meme_id)
    get_mem_by_id.check_status_code_is_404()
    delete_meme.delete_meme(auth_token, 0)
    delete_meme.check_status_code_is_404()
    delete_meme.delete_meme('123', meme_id)
    delete_meme.check_status_code_is_401()


@allure.title('Change meme test')
@allure.story('Change meme')
@allure.feature('Meme')
@pytest.mark.parametrize('text, url, info', [
    ('1', '.com', {'rating': random.randint(0, 10), 'type': [5, 'avi'], 'user': faker.name()}),
    ('Name' * 10, "https://google.com'", {'rating': random.randint(-1, 11), 'type': [{}, 'JPEG'], 'user': '*/-_-\\'}),
])
@pytest.mark.skip('BUG #1')
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
    change_meme.change_meme(auth_token, meme_id, invalid_add_mem_payload_with_int_in_text)
    change_meme.check_status_code_is_400()


@allure.title('Add meme with invalid data test')
@pytest.mark.regresion
@pytest.mark.parametrize('text, url, tags, info', [(
        1, 'https://9gag.com/gag/a1mvBqR', ['funny', 'dog'], {'rating': 4, 'type': ['gif', 'mp4'], 'user': 'chzel)'}),
    ('Me trying', 'https://9gag.com/gag/a1mvBqR', 'funny', {'rating': 4, 'type': ['gif', 'mp4'], 'user': 'chzel979'}),
    ('Me trying', 1, ['funny', 'dog'], {'rating': 4, 'type': ['gif', 'mp4'], 'user': 'chzel979'}),
    ('Me trying to reach my goals', 'https://9gag.com/gag/a1mvBqR', ['funny', 'dog'], ['rating', 'type', 'user'])])
def test_add_meme_with_invalid_data(add_mem, auth_token, text, url, tags, info):
    payload = {
        "text": text,
        "url": url,
        "tags": tags,
        "info": info
    }
    add_mem.add_mem(auth_token, payload)
    add_mem.check_status_code_is_400()
    add_mem.check_message_invalid_parameters()


@allure.title('User authorization with invalid data test')
@pytest.mark.regresion
@pytest.mark.parametrize('name', [
    1, ['User'], {'name': 'User'}, {}, [], dict()])
def test_authorization_with_invalid_user_name(authorize_user, name):
    payload = {
        'name': name,
    }
    authorize_user.authorize_user(payload)
    authorize_user.check_status_code_is_400()
