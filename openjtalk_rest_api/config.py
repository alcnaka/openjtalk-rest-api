"""
設定の読み込み等

- 環境変数の読み込み
- OpenJTalk関連ファイルの読み込み
    - 辞書
    - htsvoice
- デフォルト値の設定
"""

from glob import glob
import os
from logging import getLogger
from logging import basicConfig

import dotenv

logger = getLogger(__name__)
basicConfig(level="DEBUG")

dotenv.load_dotenv()

HTSVOICE_EXT = ".htsvoice"


def _add_htsvocie_ext(s: str) -> str:
    if s.endswith(HTSVOICE_EXT):
        return s
    else:
        return s + HTSVOICE_EXT


def _get_voice_name(s: str) -> str:
    filename = os.path.basename(s)
    return os.path.splitext(filename)[0]


def _env_get(env_name: str, fallback: str) -> str:
    e = os.environ.get(env_name)
    if (e is None) or (e == ""):
        return fallback
    return e


DICT_PATH = _env_get("DICT_PATH", "/var/lib/mecab/dic/open-jtalk/naist-jdic")
HTSVOICE_DIR = _env_get("HTSVOICE_DIR", "/usr/local/share/htsvoice")
DEFAULT_VOICE = _env_get("DEFAULT_VOICE", "mei_normal")

logger.debug(f"DICT: {DICT_PATH}")
logger.debug(f"HTSVOICE_DIR: {HTSVOICE_DIR}")
logger.debug(f"DEFAULT_VOICE: {DEFAULT_VOICE}")


_search_path = os.path.join(HTSVOICE_DIR, _add_htsvocie_ext("*"))
htsvoice_files = glob(_search_path)

logger.debug(f"htsvoice file found: {len(htsvoice_files)}")

voice_dict = {_get_voice_name(f): f for f in htsvoice_files}


def get_voice_path(voice_name: str) -> str:
    return voice_dict[voice_name]


available_voices = list(voice_dict.keys())
