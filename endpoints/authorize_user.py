import requests
import allure
import logging

from endpoints.base_endpoint import BaseEndpoints
from endpoints.JSON_schemas import SchemaUserAuth

logging.getLogger(__name__)

PAYLOAD = {'name': 'Aleksandr'}


class AuthorizeUser(BaseEndpoints):

    @allure.step('Authorize user')
    def authorize_user(self, payload=None):
        payload = payload if payload else PAYLOAD
        self.response = requests.post(f'{self.url}authorize', json=payload)
        self.status_code = self.response.status_code
        if self.status_code == 200:
            self.response_json = self.response.json()
            self.response_schema = SchemaUserAuth(**self.response_json)
            self.token = self.response_schema.token
            self.user_name = self.response_schema.user

    @allure.step('Check user name')
    def check_user_name(self, user_name):
        assert self.response_schema.user == user_name

    @allure.step('Check token')
    def check_token(self):
        assert self.token is not None
