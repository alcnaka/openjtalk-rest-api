import asyncio
from typing import NoReturn

from logging import getLogger
from pydantic import BaseModel, Field, validator
from fastapi import HTTPException

from openjtalk_rest_api.config import get_voice_path, DICT_PATH, available_voices
from openjtalk_rest_api.effects import normalize

logger = getLogger(__name__)


def _raise_no_phoneme_exception() -> NoReturn:
    raise HTTPException(
        status_code=422,
        detail={
            "loc": ["body", "syn_text"],
            "msg": "no phoneme.",
            "type": "value_error",
        },
    )


class SynQuery(BaseModel):
    voice: str = Field(default="mei_normal")
    speed: float = Field(default=1, ge=0.5, le=2)
    pitch: float = Field(default=0, ge=-24, le=24)
    vtype: float = Field(default=0.5, ge=-0.8, le=0.8)
    syn_text: str = Field(min_length=1, max_length=200)
    normalize: bool | None = Field(default=True)

    @validator("voice")
    def is_available_voice(cls, v):
        if v not in available_voices:
            raise ValueError(f"Non-available voice was specified: {v}")
        return v


def construct_command(q: SynQuery):
    return " ".join(
        [
            "open_jtalk",
            "-x",
            DICT_PATH,
            "-m",
            get_voice_path(q.voice),
            "-r",
            str(q.speed),
            "-fm",
            str(q.pitch),
            "-a",
            str(q.vtype),
            "-ow /dev/stdout",
        ]
    )


async def _tts(q: SynQuery) -> bytes:
    cmd = construct_command(q)
    logger.debug(f"EXE: {cmd}")
    logger.debug(f"syntext: {q.syn_text}")
    sp = await asyncio.subprocess.create_subprocess_shell(
        cmd,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout_data, stderr_data = await asyncio.wait_for(
        sp.communicate(input=q.syn_text.encode()), timeout=10
    )
    if sp.returncode != 0:
        if "jcomon_label.c: No phoneme." in stderr_data.decode():
            _raise_no_phoneme_exception()

        logger.error(stderr_data.decode())
        raise RuntimeError("openjtalk command failed")

    return stdout_data


async def tts(q: SynQuery) -> bytes:
    data = await _tts(q)
    if q.normalize:
        data = normalize(data)
    return data
