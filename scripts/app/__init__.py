import sys
import os
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
