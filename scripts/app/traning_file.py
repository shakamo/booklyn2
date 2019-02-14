import threading
import codecs
import os


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
        self.file = 'output/training.txt'

    def reset(self):
        if os.path.exists(self.file):
            os.remove(self.file)

    def append(self, value):
        with open(self.file, 'a') as f:
            f.write(value + '\n')

    def save_all(self, values):
        try:
            with self._lock:
                with codecs.open(self.file, 'w', "utf-8") as f:
                    eol = '\n'
                    print(*values, sep=eol, end=eol, file=f)
        except IOError:
            raise NotImplementedError('save error to master.json')
