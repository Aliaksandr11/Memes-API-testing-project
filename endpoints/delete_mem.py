import requests
import allure
import logging

from endpoints.base_endpoint import BaseEndpoints

logging.getLogger(__name__)


class DeleteMeme(BaseEndpoints):
    @allure.step('Delete meme')
    def delete_meme(self, auth_token, meme_id):
        headers = {'Authorization': auth_token}
        self.response = requests.delete(f'{self.url}meme/{meme_id}', headers=headers)
        logging.info(f'Delete meme by id: {meme_id}')
        self.status_code = self.response.status_code

    @allure.step('Check delete meme')
    def check_delete_meme(self, meme_id):
        assert self.response.text == f'Meme with id {meme_id} successfully deleted'
        logging.info(f'Meme with id {meme_id} successfully deleted')
