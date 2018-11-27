from . import logger

def get_wakati(text):
    """
    文書を分かち書きし単語単位に分割する
    """
    sanitized_text = sanitize(text)
    tagger = MeCab.Tagger(
        '-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
    return tagger.parse(sanitized_text).replace(' \n', '')

def sanitize(text):
    """
    サニタイズ処理を行う
    UTF-8-MAC を UTF-8 に変換
    """
    return unicodedata.normalize('NFC', text)
