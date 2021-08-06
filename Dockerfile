FROM python:3.9-slim

WORKDIR /usr/src/app

COPY . .

RUN apt update && apt install -y \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install -r ./requirements.txt --no-cache-dir

# 保存時にファイルモードを変えない、なんか改行コードがうまくいく
RUN git config --global core.filemode false

CMD [ "python", "./src/main.py" ]
