FROM python

WORKDIR /app

ADD . /app

RUN venv/bin/activate 

RUN apt-get update && apt-get install -y locales && \
    echo "ru_RU.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen ru_RU.UTF-8 && \
    update-locale LANG=ru_RU.UTF-8 LC_ALL=ru_RU.UTF-8 

RUN pip install -r requirements.txt

CMD ["python", "main.py"]