import threading
import codecs
import json
import app


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
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._data = None
        return cls._instance

    def __init__(self):
        try:
            if self._data is None:
                self._lock = threading.Lock()
                with codecs.open('output/master.json', 'r', "utf-8") as f:
                    self._data = json.load(f)
        except IOError:
            with self._lock:
                with codecs.open('output/master.json', 'w', "utf-8") as f:
                    json.dump({}, f, ensure_ascii=False)

    def add(self, name, uuid, value):
        with self._lock:
            if self._data.get(name) is None:
                self._data[name] = {}
            self._data[name][uuid] = value

    def get(self, name, uuid):
        with self._lock:
            if self._data.get(name) is None:
                return None
            if self._data[name].get(uuid) is None:
                return None
        
        return self._data[name][uuid]

    def save(self):
        try:
            with self._lock:
                with codecs.open('output/master.json', 'w', "utf-8") as f:
                    json.dump(self._data, f, ensure_ascii=False)
        except IOError:
            raise NotImplementedError('save error to master.json')
