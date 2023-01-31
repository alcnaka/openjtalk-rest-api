from logging import getLogger
from io import BytesIO

from pydub import AudioSegment
from pydub.effects import normalize as _normalize


logger = getLogger(__name__)


def normalize(data: bytes) -> bytes:
    """Wav形式のbytesオブジェクトをnormalize

    Args:
        data (bytes): wav data

    Returns:
        bytes: normalized wav data
    """
    # pydubのAudioSegmentとして読み込み
    seg = AudioSegment(data)
    # normalize処理
    normalied_seg = _normalize(seg)
    # メモリ上の領域にbytesを持つ
    tmp = BytesIO()
    # メモリ上にwav形式のbytesで書き出し
    normalied_seg.export(tmp, format="wav")
    return tmp.read()
