# booklyn2

#### Python 環境構築
1. Pythonのインストール
    * brew install python3
    * brew install pipenv
2. venv の作成
    * python3 -m venv .venv
3. venv を有効にする
    * source .venv/bin/activate
4. fastText のインストール
    * pipenv install
5. Pipfile のインストール
    * pipenv install


####
    export PIPENV_VENV_IN_PROJECT=true


#### pylint
conda install --channel https://conda.anaconda.org/anaconda pylint


#### fastText
    git clone https://github.com/facebookresearch/fastText.git
    cd fastText
    make
    pip install cython
    pip install fasttext

#### Mecab
    brew install mecab mecab-ipadic
    brew install swig
    pip install mecab-python3`

#### Scrapy
    pip install scrapy

##### Scrapy run
    scrapy runspider scraping.py -o a.json --set=FEED_EXPORT_ENCODING='utf-8'

![Alt text](./Booklyn.svg)


#### Docker
    cd scripts
    docker build -t scraping .
    docker run -it --rm -v $(pwd):/app --entrypoint /bin/bash -t scraping
    docker run --rm -v $(pwd):/app scraping scrapy runspider scraping_anikore.py --set=FEED_EXPORT_ENCODING='utf-8'

#### Execute
    . .venv/bin/activate
    scrapy runspider scraping_anikore.py --set=FEED_EXPORT_ENCODING='utf-8'
    scrapy runspider scraping_amazon.py --set=FEED_EXPORT_ENCODING='utf-8'

