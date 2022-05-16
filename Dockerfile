FROM python:3.10.4

RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /usr/src/siffredi-bot

COPY . .

RUN pip3 install -r requirements.txt

CMD [ "python" , "launcher.py"]