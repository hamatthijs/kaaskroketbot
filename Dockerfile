FROM python:3.11-slim-bullseye

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt --break-system-packages

COPY . .

CMD [ "python", "./main.py" ]
