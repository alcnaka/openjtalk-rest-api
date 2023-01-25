from logging import getLogger

from fastapi import FastAPI
from fastapi.responses import Response, HTMLResponse

from openjtalk_rest_api.jtalk import SynQuery, tts
from openjtalk_rest_api.config import available_voices

logger = getLogger(__name__)

app = FastAPI()

class WavResponse(Response):
    media_type = 'audio/wav'

@app.get('/hello')
def get_hello():
    return "hello"


@app.get('/available_voices')
def get_available_voices():
    return available_voices


@app.post('/synthesize', response_class=WavResponse)
async def post_synthesize(q: SynQuery,):
    data = await tts(q)
    return WavResponse(data)
