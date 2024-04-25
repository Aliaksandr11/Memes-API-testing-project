import requests
import allure
import logging

from endpoints.base_endpoint import BaseEndpoints


logging.getLogger(__name__)


class GetAllMemes(BaseEndpoints):

    @allure.step('Get all memes')
    def get_all_memes(self, auth_token):
        headers = {'Authorization': auth_token}
        self.response = requests.get(f'{self.url}meme', headers=headers)
        self.status_code = self.response.status_code
        if self.status_code == 200:
            self.response_json = self.response.json()
            self.meme_ids = [mem['id'] for mem in self.response_json['data']]

    @allure.step('id uniqueness check')
    def check_uniqueness_ids(self):
        assert len(set(self.meme_ids)) == len(self.meme_ids)

    @allure.step('Checking the expected and actual number of memes')
    def check_memes_count(self):
        assert len(self.response_json['data']) == len(self.meme_ids)

    @allure.step('Check that keys in data')
    def check_keys_in_data(self):
        for meme in self.response_json['data']:
            assert "id" in meme
            assert "info" in meme
            assert "tags" in meme
            assert "text" in meme
            assert "updated_by" in meme
            assert "url" in meme

    @allure.step('Check that mem text is str')
    def check_mem_text_is_str(self):
        for meme in self.response_json['data']:
            assert isinstance(meme['text'], str)

    @allure.step('Check that mem url is str')
    def check_mem_url_is_str(self):
        for meme in self.response_json['data']:
            assert isinstance(meme['url'], str)

    @allure.step('Check that mem tags is list')
    def check_mem_tags_is_list(self):
        for meme in self.response_json['data']:
            assert isinstance(meme['tags'], list)

    @allure.step('Check that mem info is dict')
    def check_mem_info_is_dict(self):
        for meme in self.response_json['data']:
            assert isinstance(meme['info'], dict)

    @allure.step('Check that mem updated_by is str')
    def check_mem_updated_by_is_str(self):
        for meme in self.response_json['data']:
            assert isinstance(meme['updated_by'], str)

    @allure.step('Check that mem id is int')
    def check_mem_id_is_int(self):
        for meme in self.response_json['data']:
            assert isinstance(meme['id'], int), f'{meme["id"]} is not int'
