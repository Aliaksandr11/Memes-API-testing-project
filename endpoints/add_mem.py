import requests
import allure
import logging

from endpoints.base_endpoint import BaseEndpoints
from endpoints.JSON_schemas import SchemaAddMeme

logging.getLogger(__name__)

PAYLOAD = {
    "text": "Me trying to reach my goals",
    "url": "https://9gag.com/gag/a1mvBqR",
    "tags": ['funny', 'dog'],
    "info": {
        'rating': 4,
        'type': ['gif',
                 'mp4'],
        'user': 'chzel979'}
}


class AddMem(BaseEndpoints):

    @allure.step('Add new mem')
    def add_mem(self, auth_token, payload=None):
        payload = payload if payload else PAYLOAD
        headers = {'Authorization': auth_token}
        logging.info(f'autorization token: {auth_token}')
        self.response = requests.post(f'{self.url}/meme', json=payload, headers=headers)
        self.status_code = self.response.status_code
        if self.status_code == 200:
            self.response_json = self.response.json()
            self.response_schema = SchemaAddMeme(**self.response.json())
            self.mem_id = self.response_schema.id
            logging.info(f'mem_id: {self.mem_id}')

    @allure.step('Check mem text')
    def check_mem_text(self, text):
        assert self.response.json()['text'] == text

    @allure.step('Check mem url')
    def check_mem_url(self, url):
        assert self.response_schema.url == url

    @allure.step('Check mem tags')
    def check_mem_tags(self, tags):
        assert self.response_schema.tags == tags

    @allure.step('Check mem info')
    def check_mem_info(self, info):
        assert self.response_schema.info.rating == info['rating']
        assert self.response_schema.info.type == info['type']
        assert self.response_schema.info.user == info['user']

    @allure.step('Check that mem was added by user')
    def check_updated_by_user(self, user):
        assert self.response_schema.updated_by == user
        logging.info(f'mem was added by user: {user}')


    @allure.step('Check mem text')
    def check_mem_text(self, text):
        assert self.response_schema.text == text
        logging.info(f'mem text: {text}')

    @allure.step('Check message invalid parameters')
    def check_message_invalid_parameters(self):
        assert 'Invalid parameters' in self.response.text




