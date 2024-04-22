import requests
import allure
import logging
from endpoints.base_endpoint import BaseEndpoints

logging.getLogger(__name__)


class ActivityToken(BaseEndpoints):

    @allure.step('Check activity token')
    def activity_token(self, token):
        self.response = requests.get(f'{self.url}/authorize/{token}')
        logging.info(f'Check activity token: {token}')
        self.status_code = self.response.status_code

    @allure.step('Check token is active')
    def check_token_is_active(self, user_name):
        assert self.response.text == f'Token is alive. Username is {user_name}'

    @allure.step('Check text is "Token not found"')
    def check_text_is_token_not_found(self):
        assert 'Token not found' in self.response.text
