import allure


class BaseEndpoints:
    url = 'http://167.172.172.115:52355/'
    response = None
    status_code = None
    response_json = None
    response_schema = None
    mem_id = None
    token = None
    user_name = None
    meme_ids = None

    @allure.step('Check the response status code is 200')
    def check_status_code_is_200(self):
        assert self.status_code == 200

    @allure.step('Check the response status code is 404')
    def check_status_code_is_404(self):
        assert self.status_code == 404

    @allure.step('Check the response status code is 400')
    def check_status_code_is_400(self):
        assert self.status_code == 400

    @allure.step('Check the response status code is 401')
    def check_status_code_is_401(self):
        assert self.status_code == 401
