FROM python:latest

WORKDIR /srv/
COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

CMD [ "python3", "channelcopybot.py" ]
