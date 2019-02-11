import threading
import uuid as u

import fastText as ft
from fastText import train_supervised

import app

from . import learning, master_file, traning_file

lock = threading.Lock()


def classify(name, value, isLock=True):
    if isLock:
        with lock:
            __classify(name, value, isLock)
    else:
        __classify(name, value, isLock)


def __classify(name, value, isLock):
    # Masterファイルを読み込み（シングルトン）
    master = master_file.MasterFile()

    data = master.get_training_data()
    for name in data:
        for uuid in data[name]:
            if data[name][uuid]['key'] == value['key']:
                data[name][uuid] = value
                print('ある！')
                return

    # fastTextクラスを取得（シングルトン）
    f = FastTextML()

    # fastTextのスコアを取得
    uuid, score = f.predict(app.get_wakati(value['title']))

    if uuid and 0.5 < score:
        # 同じUUIDで上書き保存
        master.add(name, uuid, value)
    else:
        # UUIDを採番して保存
        uuid = str(u.uuid4())
        master.add(name, uuid, value)
        # 再学習前にマスタデータを保存
        master.save()
        # 再学習
        if isLock:
            learning.learn(uuid, app.get_wakati(value['title']))

    # 結果がどの程度違うのか、差分をログに出力
    if master.get(name, uuid) is not None:
        if value['title'] != master.get(name, uuid)['title']:
            print(value['title'] + ' or ' + master.get(name, uuid)['title'])
    else:
        print('何かがおかしい')


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
                if app.exists_output_fasttext_model():
                    self._model = ft.load_model(
                        app.get_output_fasttext_model())

        except IOError:
            raise NotImplementedError('load error to model.bin')

    def predict(self, wakati_text):
        if hasattr(self, '_model'):
            result = self._model.predict(wakati_text)
            uuid = result[0][0].replace('__label__', '')
            score = result[1][0]
            return uuid, score
        return None, None

    def train(self):
        master = master_file.MasterFile()
        data = master.get_training_data()

        traning = traning_file.TraningFile()
        traning.reset()

        hasText = False
        for name in data:
            for uuid in data[name]:
                traning.append('__label__' + uuid + ' , ' +
                               app.get_wakati(data[name][uuid]['title']))
                hasText = True

        if hasText is False:
            return

        self._model = train_supervised(
            input=app.get_output_train_text(), epoch=200, lr=0.7, wordNgrams=2,
            loss="hs", dim=100
        )
        with self._lock:
            self.__print_results(
                *self._model.test(app.get_output_train_text()))
            self._model.save_model(app.get_output_fasttext_model())

    def __print_results(self, N, p, r):
        print("N\t" + str(N))
        print("P@{}\t{:.3f}".format(1, p))
        print("R@{}\t{:.3f}".format(1, r))
