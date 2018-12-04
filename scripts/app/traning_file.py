import threading
import codecs
import json
import os
import app


class TraningFile:
    """
    https://qiita.com/nirperm/items/af1f83925ba43dbf22eb
    file = FileObject()
    data = file.save()
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        print()

    def reset(self):
        if os.path.exists(app.get_root_path().joinpath('output').joinpath('training.txt')):
            os.remove(app.get_root_path().joinpath(
                'output').joinpath('training.txt'))

    def append(self, value):
        with open(app.get_root_path().joinpath('output').joinpath('training.txt'), 'a') as f:
            f.write(value + '\n')

    def save_all(self, values):
        try:
            with self._lock:
                with codecs.open(app.get_root_path().joinpath('output').joinpath('training.txt'), 'w', "utf-8") as f:
                    eol = '\n'
                    print(*values, sep=eol, end=eol, file=f)
        except IOError:
            raise NotImplementedError('save error to master.json')
