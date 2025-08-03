FROM python:3.11.13-bullseye

ENV PYTHONBUFFERED=1

# install system deps
# RUN apt-get update \
#     && apt-get install -y libpq-dev build-essential \
#     && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# copy and install Python deps
COPY requirements.txt ./

RUN pip3 install -r requirements.txt

# copy your code
COPY . ./

# collect static, run migrations at container start
CMD gunicorn videoshare.wsgi:application --bind 0.0.0.0:8000

EXPOSE 8000
