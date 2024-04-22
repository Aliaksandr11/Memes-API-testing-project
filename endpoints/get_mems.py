import requests
import allure
import logging

from endpoints.base_endpoint import BaseEndpoints

logging.getLogger(__name__)


class GetAllMemes(BaseEndpoints):

    @allure.step('Get all memes')
    def get_all_memes(self, auth_token):
        headers = {'Authorization': auth_token}
        self.response = requests.get('http://167.172.172.115:52355/meme', headers=headers)
        self.status_code = self.response.status_code
        self.response_json = self.response.json()
        self.meme_ids = [mem['id'] for mem in self.response_json['data']]
        logging.info(f'Get all memes. Memes count: {self.meme_ids}')

    @allure.step('id uniqueness check')
    def check_uniqueness_ids(self):
        assert len(set(self.meme_ids)) == len(self.meme_ids)

    @allure.step('Сhecking the expected and actual number of memes')
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

















