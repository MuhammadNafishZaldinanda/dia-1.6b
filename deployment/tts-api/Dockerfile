FROM python:3.10-slim
LABEL description="DIA TTS API"
LABEL maintainer="Muhammad Nafish Zaldinanda"
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    ca-certificates \
    g++ \
    git \
    libsndfile1 \
    espeak-ng \
    ffmpeg \
    libasound-dev \
    libportaudio2 \
    libsqlite3-dev && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /usr/src/app/
COPY . /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt

ENV LC_ALL="C.UTF-8"
ENV LANG="C.UTF-8"
ENV TZ="Asia/Jakarta"

EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]