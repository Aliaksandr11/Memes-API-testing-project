import pytest
import requests
import allure
import logging

from endpoints.base_endpoint import BaseEndpoints

logging.getLogger(__name__)


class ChangeMeme(BaseEndpoints):
    @allure.step('Change meme')
    def change_meme(self, auth_token, meme_id, payload):
        headers = {'Authorization': auth_token}
        self.response = requests.put(f'http://167.172.172.115:52355/meme/{meme_id}', json=payload, headers=headers)
        self.status_code = self.response.status_code
        if self.status_code == 200:
            self.response_json = self.response.json()

    @allure.step('Check that mem text')
    def check_mem_text(self, text):
        assert self.response_json['text'] == text

    @allure.step('Check that mem url')
    def check_mem_url(self, url):
        assert self.response_json['url'] == url

    @allure.step('Check that mem tags')
    def check_mem_tags(self, tags):
        assert self.response_json['tags'] == tags

    @allure.step('Check that mem info')
    def check_mem_info(self, info):
        assert self.response_json['info']['rating'] == info['rating']
        assert self.response_json['info']['type'] == info['type']
        assert self.response_json['info']['user'] == info['user']

    @allure.step('Check that mem was added by user')
    def check_updated_by_user(self, user):
        assert self.response_json['updated_by'] == user

    @allure.step('Check mem id')
    def check_mem_id(self, meme_id):
        assert self.response_json['id'] == meme_id





