FROM python:3.10.19-alpine3.23
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "fastapi", "dev" ]
