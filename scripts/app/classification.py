from .lib import logger
import unicodedata
import MeCab
import app
import threading
import codecs
import json
import fastText as ft
from fastText import train_supervised


def classify(name, value):
    f = FastTextML()
    result = f.predict(app.get_wakati(value['title']))
    uuid = result[0][0].replace('__label__', '')
    score = result[1][0]
    print(uuid)
    print(score)


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
