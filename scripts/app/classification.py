from .lib import logger
import unicodedata
import MeCab
import app
import threading
import codecs
import json
import fastText as ft
from fastText import train_supervised
from . import master_file
import uuid as u


def classify(name, value):

    # fastText シングルトンクラスを取得
    f = FastTextML()
    # fastTextのスコアを取得
    result = f.predict(app.get_wakati(value['title']))
    uuid = result[0][0].replace('__label__', '')
    score = result[1][0]

    # Masterファイルを読み込み（シングルトン）
    master = master_file.MasterFile()

    if 0.5 < score:
        # 同じUUIDで上書き保存
        master.add(name, uuid, value)
    else:
        # UUIDを採番して保存
        master.add(name, str(u.uuid4()), value)

        # 結果がどの程度違うのか、差分をログに出力
        if master.get(name, uuid) is not None:
            if value['title'] != master.get(name, uuid)['title']:
                print(value['title'] + ' or ' + master.get(name, uuid)['title'])

    master.save()


class FastTextML:
    """
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance._lock = None
        return cls._instance

    def __init__(self):
        try:
            if self._lock is None:
                self._lock = threading.Lock()
                self._model = ft.load_model(app.get_output_fasttext_model())
            
        except IOError:
            raise NotImplementedError('load error to model.bin')

    def predict(self, wakati_text):
        return self._model.predict(wakati_text)

    def train(self):
        self._model = train_supervised(
            input="output/temp.txt", epoch=200, lr=0.7, wordNgrams=2,
            loss="hs", dim=100
        )
        with self._lock:
            self.__print_results(*self._model.test("output/temp.txt"))
            self._model.save_model('output/model.bin')

    def __print_results(self, N, p, r):
        print("N\t" + str(N))
        print("P@{}\t{:.3f}".format(1, p))
        print("R@{}\t{:.3f}".format(1, r))
