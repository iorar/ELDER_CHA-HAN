FROM python:3.9-slim

WORKDIR /usr/src/app

COPY . .

RUN apt-get update && apt-get install -y \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install -r ./requirements.txt --no-cache-dir

CMD [ "python", "./src/main.py" ]
