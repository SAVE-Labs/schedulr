FROM python:3.12-slim AS baseimage


ARG USERNAME=app
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    python3-dev \
    libpq-dev \
    sqlite3 \
    gettext \
    curl

RUN curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/download/v3.4.1/tailwindcss-linux-x64
RUN chmod +x tailwindcss-linux-x64
RUN mv tailwindcss-linux-x64 /usr/bin/tailwindcss

RUN mkdir /usr/app && chown $USERNAME:$USERNAME /usr/app
RUN mkdir /usr/.venv && chown $USERNAME:$USERNAME /usr/.venv

USER $USERNAME

RUN python -m venv /usr/.venv
ENV PATH="/usr/.venv/bin:$PATH"

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --require-hashes --no-deps -r requirements.txt

WORKDIR /usr/app

COPY . .

FROM baseimage AS prod

RUN SECRET_KEY=placeholder python manage.py collectstatic --no-input

CMD [ "gunicorn", "securetransfer.wsgi", "--bind", "0.0.0.0:8000", "--timeout", "3600", "--workers", "6" ]

FROM baseimage AS dev

RUN pip install pip-tools

CMD ["python", "manage.py", "runserver"]
