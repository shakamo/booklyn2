import sys
import os
import shutil
from pathlib import Path

from . import scraping
from . import lib

ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT))


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
    return os.path.join(ROOT.joinpath('output'), 'train.txt')


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

