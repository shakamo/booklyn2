import sys
import os
import shutil
from pathlib import Path
import MeCab
import re
import unicodedata
from . import lib
from . import classification


ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT))


def get_root_path():
    return ROOT


def get_wakati(resource):
    """
    文書を分かち書きし単語単位に分割する
    """
    text = unicodedata.normalize('NFC', resource)
    text = re.sub('[^ぁ-んァ-ンーa-zA-Z0-9一-龠０-９\-\r\s]+', '', text)
    text = re.sub('[\s]+', ' ', text)
    text = re.sub(r'[\n|\r|\t]', '', text)
    text = re.sub(r'[１]', '1', text)
    text = re.sub(r'[２]', '2', text)
    text = re.sub(r'[３]', '3', text)
    text = re.sub(r'[４]', '4', text)
    text = re.sub(r'[５]', '5', text)
    text = re.sub(r'[６]', '6', text)
    text = re.sub(r'[７]', '7', text)
    text = re.sub(r'[８]', '8', text)
    text = re.sub(r'[９]', '9', text)
    text = re.sub(r'[０]', '0', text)

    tagger = MeCab.Tagger(
        '-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
    text = tagger.parse(text).replace(' \n', '')
    if len(text) + 3 < len(resource):
        print(resource + ' : ' + text)
    if len(text) < 1:
        print(resource + ' : ' + text)
    return text


def sanitize(resource):
    """
    サニタイズ処理を行う
    UTF-8-MAC を UTF-8 に変換
    """
    text = unicodedata.normalize('NFC', resource)
    text = re.sub('[^ぁ-んァ-ンーa-zA-Z0-9一-龠０-９\-\r\s]+', '', text)
    text = re.sub('[\s]+', ' ', text)
    text = re.sub(r'[\n|\r|\t]', '', text)
    text = re.sub(r'[１]', '1', text)
    text = re.sub(r'[２]', '2', text)
    text = re.sub(r'[３]', '3', text)
    text = re.sub(r'[４]', '4', text)
    text = re.sub(r'[５]', '5', text)
    text = re.sub(r'[６]', '6', text)
    text = re.sub(r'[７]', '7', text)
    text = re.sub(r'[８]', '8', text)
    text = re.sub(r'[９]', '9', text)
    text = re.sub(r'[０]', '0', text)

    if len(text) + 3 < len(resource):
        print(resource + ' : ' + text)
    if len(text) < 3:
        print(resource + ' : ' + text)
    return text


def get_input_path():
    os.makedirs(ROOT.joinpath('input'), exist_ok=True)
    return ROOT.joinpath('input')


def get_output_path():
    os.makedirs(ROOT.joinpath('output'), exist_ok=True)
    return ROOT.joinpath('output')


def remove_output_unknown_file():
    if exists_output_unknown_file():
        os.remove(ROOT.joinpath('output').joinpath('unknown.json'))


def exists_output_unknown_file():
    return os.path.exists(ROOT.joinpath('output').joinpath('unknown.json'))


def get_output_unknown_file():
    return os.path.join(ROOT.joinpath('output'), 'unknown.json')


def get_output_train_text():
    return os.path.join(ROOT.joinpath('output'), 'training.txt')


def remove_output_train_text():
    if exists_output_train_text():
        os.remove(ROOT.joinpath('output').joinpath('train.txt'))


def exists_output_train_text():
    return os.path.exists(ROOT.joinpath('output').joinpath('train.txt'))


def get_output_fasttext_model():
    return os.path.join(ROOT.joinpath('output'), 'fasttext.bin')


def exists_output_fasttext_model():
    return os.path.exists(ROOT.joinpath('output').joinpath('fasttext.bin'))


def remove_output_fasttext_model():
    if exists_output_fasttext_model():
        os.remove(ROOT.joinpath('output').joinpath('fasttext.bin'))
