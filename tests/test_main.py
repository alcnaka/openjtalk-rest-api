import wave
from tempfile import TemporaryFile

from fastapi.testclient import TestClient

from openjtalk_rest_api.main import app
from openjtalk_rest_api.jtalk import SynQuery

client = TestClient(app)

def test_hello():
    response = client.get('/hello')
    assert response.status_code == 200
    assert response.text == '"hello"'


def test_get_avilable_voices():
    response = client.get('/available_voices')
    assert response.status_code == 200
    voice_list = response.json()
    assert type(voice_list) == list
    assert len(voice_list) > 0


def test_gen_wav():
    data = {
        "voice": "mei_normal",
        "speed": 1,
        "pitch": 0,
        "vtype": 0.3,
        "syn_text": "テスト音声の合成です"
    }
    response = client.post('/synthesize', json=data)
    assert response.status_code == 200
    assert len(response.content) != 0
