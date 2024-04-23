from locust import task, HttpUser
import random


class AddAndSearchForMemesByUser(HttpUser):
    add_memes_ids = set()
    meme_id = None
    auth_token = None
    all_memes = None
    added_meme_id = None

    def on_start(self):
        response = self.client.post('/authorize', json={'name': 'Sanek'}).json()
        self.auth_token = response['token']
        self.all_memes = self.client.get('/meme', headers={'Authorization': self.auth_token}).json()
        self.meme_id = random.choice([meme['id'] for meme in self.all_memes['data']])

    @task(5)
    def get_meme(self):
        self.client.get(f'/meme/{self.meme_id}', headers={'Authorization': self.auth_token})

    @task(1)
    def add_meme(self):
        payload = {
            "text": "Me trying to reach my goals",
            "url": "https://9gag.com/gag/a1mvBqR",
            "tags": ['funny', 'dog'],
            "info": {
                'rating': 5,
                'type': ['gif',
                         'mp4'],
                'user': 'chzel979'}
        }
        response = self.client.post('/meme', json=payload, headers={'Authorization': self.auth_token})
        response_json = response.json()
        self.added_meme_id = response_json['id']
        self.add_memes_ids.add(self.added_meme_id)

    def on_stop(self):
        for ids in self.add_memes_ids:
            self.client.delete(f'/meme/{ids}', headers={'Authorization': self.auth_token})
