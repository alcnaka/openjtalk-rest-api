from logging import getLogger
from io import BytesIO

from pydub import AudioSegment
from pydub.effects import normalize as _normalize


logger = getLogger(__name__)


def normalize(data: bytes) -> bytes:
    seg = AudioSegment(data)
    logger.debug(str(seg))
    _data = _normalize(seg)
    logger.debug(str(_data))
    result = BytesIO()
    _data.export(result, format="wav")
    return result.read()
