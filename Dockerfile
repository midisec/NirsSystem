FROM python:3.7

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD python app.py
