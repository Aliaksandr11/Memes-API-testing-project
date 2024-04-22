import allure
import requests
import logging

from endpoints.base_endpoint import BaseEndpoints


logging.getLogger(__name__)

class GetMemeById(BaseEndpoints):

    @allure.step('Get meme by id')
    def get_mem_by_id(self, auth_token, mem_id):
        headers = {'Authorization': auth_token}
        self.response = requests.get(f'http://167.172.172.115:52355/meme/{mem_id}', headers=headers)
        logging.info(f'Get meme by id: {mem_id}')
        self.status_code = self.response.status_code

    @allure.step('Check mem id')
    def check_mem_id(self, mem_id):
        assert self.response.json()['id'] == mem_id

    @allure.step('Check that mem text')
    def check_mem_text(self, text):
        assert self.response.json()['text'] == text

    @allure.step('Check that keys in data')
    def check_keys_in_data(self):
        assert "id" in self.response.json()
        assert "info" in self.response.json()
        assert "tags" in self.response.json()
        assert "text" in self.response.json()
        assert "updated_by" in self.response.json()
        assert "url" in self.response.json()







