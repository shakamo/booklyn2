import threading
import codecs
import json


class MasterFile:
    """
    https://qiita.com/nirperm/items/af1f83925ba43dbf22eb
    file = FileObject()
    data = file.save()
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        try:
            if self._lock is None:
                self._lock = threading.Lock()
                with codecs.open('output/master.json', 'r', "utf-8") as f:
                    self._data = json.load(f)
        except IOError:
            raise NotImplementedError('load error to master.json')

    def add(self, uuid, value):
        with self._lock:
            self._data[uuid] = value

    def get(self, uuid):
        with self._lock:
            return self._data[uuid]

    def save(self):
        try:
            with self._lock:
                with codecs.open('output/master.json', 'w', "utf-8") as f:
                    json.dump(self._data, f, ensure_ascii=False)
        except IOError:
            raise NotImplementedError('save error to master.json')
