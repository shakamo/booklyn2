import threading
import codecs
import json
import uuid as u
import os
from app.lib import logger
from app import traning_file

logger = logger.get_module_logger(__name__)


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
                cls._instance._lock = None
        return cls._instance

    def __init__(self):
        self.file = 'output/master.json'
        try:
            if self._lock is None:
                self._lock = threading.Lock()
            with self._lock:
                # ファイルが存在するかどうか
                if os.path.exists(self.file):
                    with codecs.open(self.file, 'r', "utf-8") as f:
                        self._data = json.load(f)
                else:
                    # 空ファイルを作成
                    with codecs.open(self.file, 'w', "utf-8") as f:
                        json.dump({}, f, ensure_ascii=False)
                        self._data = {}
        except IOError:
            logger.error('load error to master.json')
            raise NotImplementedError('load error to master.json')

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
                with codecs.open(self.file, 'w', "utf-8") as f:
                    json.dump(self._data, f, ensure_ascii=False)
        except IOError:
            raise NotImplementedError('save error to master.json')

    def save_traning_file(self):
        try:
            with self._lock:
                traning_file.TraningFile().create(self._data)
        except IOError:
            raise NotImplementedError('save error to master.json')

    def append(self, name, key, value):
        with self._lock:
            for uuid in self._data:
                if self._data[uuid].get(name) is not None:
                    if self._data[uuid][name].get(key) is not None:
                        self._data[uuid][name][key] = value
                        return

            uuid = str(u.uuid4())
            self._data[uuid] = {}
            self._data[uuid][name] = {}
            self._data[uuid][name][key] = value
