import allure
import pytest
import random
from faker import Faker

from data.defolt_payload import defolt_payload
from data.user_authorization_payload import user_authorization_payload
from data.user_authorization_payload import invalid_user_authorization_payload_with_int
from data.user_authorization_payload import user_authorization_payload_with_empty
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
    authorize_user.authorize_user(invalid_user_authorization_payload_with_int)
    authorize_user.check_status_code_is_400()
    authorize_user.authorize_user(user_authorization_payload_with_empty)
    authorize_user.check_status_code_is_200()


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
def test_add_meme(add_mem, auth_token, delete_meme, user_name):
    payload = defolt_payload
    add_mem.add_mem(auth_token, payload)
    add_mem.check_status_code_is_200()
    add_mem.check_updated_by_user(user_name)
    add_mem.check_mem_text(payload['text'])
    add_mem.check_mem_url(payload['url'])
    add_mem.check_mem_tags(payload['tags'])
    add_mem.check_mem_info(payload['info'])
    add_mem.add_mem(auth_token, payload)
    add_mem.add_mem(auth_token, invalid_add_mem_payload_with_int_in_text)
    add_mem.check_status_code_is_400()
    add_mem.check_message_invalid_parameters()
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


@allure.title('Change meme test')
@allure.story('Change meme')
@allure.feature('Meme')
@pytest.mark.retest
@pytest.mark.parametrize('text, url, info', [
    ('1', '.com', {'rating': random.randint(0, 10), 'type': [5, 'avi'], 'user': faker.name()}),
    ('Name' * 10, "https://google.com'", {'rating': random.randint(-1, 11), 'type': [{}, 'JPEG'], 'user': '*/-_-\\'}),
])
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
