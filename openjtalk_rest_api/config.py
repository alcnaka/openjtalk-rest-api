"""
設定の読み込み等

- 環境変数の読み込み
- OpenJTalk関連ファイルの読み込み
    - 辞書
    - htsvoice
- デフォルト値の設定
"""

import os
from logging import getLogger
from logging import basicConfig

logger = getLogger(__name__)

basicConfig(level='DEBUG')

logger.debug('test')

DICT_PATH = '/var/lib/mecab/dic/open-jtalk/naist-jdic'
MEI_NORMAL = 'mei_normal.htsvoice'
file_dir = os.path.dirname(__file__)
default_voice_path = os.path.join(file_dir, MEI_NORMAL)

# TODO: htsvoiceを追加できるように
voice_dict = {
    'mei_normal': default_voice_path,
}

def get_voice_path(voice_name: str) -> str:
    return voice_dict[voice_name]

available_voices = list(voice_dict.keys())
