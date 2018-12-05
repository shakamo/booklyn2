import argparse
import re
import unicodedata
import urllib.request as req
import MeCab
import scrapy
import json
import uuid
import app
from app.lib import logger
from fastText import train_supervised, BOW
from . import master_file
from . import traning_file
import threading

logger = logger.get_module_logger(__name__)
