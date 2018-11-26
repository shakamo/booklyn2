FROM python:latest

RUN cat /etc/issue

RUN apt update

RUN apt -y install python3-dev
RUN apt -y install mecab libmecab-dev
RUN apt -y install mecab-ipadic-utf8
RUN apt -y install swig

RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
RUN ls -l
RUN cd /mecab-ipadic-neologd
RUN apt -y install sudo
RUN /mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -n -y
RUN echo `mecab-config --dicdir`"/mecab-ipadic-neologd"

RUN git clone https://github.com/facebookresearch/fastText.git
RUN cd fastText/
RUN make

RUN pip install pipenv

RUN mkdir /app
COPY ./Pipfile /app

WORKDIR /app

RUN pipenv install


ENTRYPOINT ["pipenv", "run"]
CMD ["python", "scraping_anikore.py"]



