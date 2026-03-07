# Dia TTS API

### Prerequisites
- Python >= 3.10.12
- libsndfile1 == 1.2.0
- espeak-ng == 1.51
- ffmpeg == 5.1.6
- libportaudio2 == 19.6.0
- libsqlite3-dev == 3.40.1

### Model Compatibility
This API supports for models: `nari-labs/dia-1.6b`

## How to Run
### Setup
- Download resources models

- Copy .env.example to .env

- Set up server host, port, and machine learning configuration in .env file.
    ```
   # Directory path where the model and audio reference are stored.
    RESOURCES=<RESOURCES>

    # The model architecture (currently accepted: dia).
    MODEL_NAME=<MODEL_NAME>

    #Select hardware: CPU or CUDA
    HARDWARE=<HARDWARE>

    # The audio reference path during generating sound.
    AUD_REF=<AUD_REF>

    # Audio speed multiplier for generated speech
    SPEED_FACTOR=<SPEED_FACTOR>
    ```
### Run via Local Environment
- Install all dependency / python modules. Better using virtualenv and separate the environment between one and other services.
    ```
    (dia-tts-api) $ pip install -r requirements.txt
    ```

- Run server
    ```
    (dia-tts-api) $ uvicorn main:app --host 0.0.0.0 --port 8080
    ```

- Access API
    ```
    http://localhost:8080
    ```

- Access API Documentation
    ```
    http://localhost:8080/api/docs
    ```

- Help
    ```
    (dia-tts-api) $ uvicorn --help
    ```

### Run via Container

- Build
    ```
    docker build -t dia-tts-api:[TAG VERSION] .
    ```
- Setup `.env` file
- Run using CPU
    ```
    docker run --rm --name dia-tts-api -it -p "8080:8080" --env-file .env dia-tts-api:[TAG VERSION]
    ```
- Run using GPU
    
    Make sure `NVIDIA Container Toolkit` is installed in your system. This toolkit allows Docker containers to utilize NVIDIA GPUs for accelerated computations. For installation instructions, visit [NVIDIA Container Toolkit Installation](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).
    ```
    docker run --rm --name dia-tts-api -it -p "8080:8080" --env-file .env --gpus all dia-tts-api:[TAG VERSION]
    ```
- Access API
    ```
    http://localhost:8080
    ```
- Access API Documentation
    ```
    http://localhost:8080/api/docs
    ```

## How to Use

### 1. Endpoint GET /text_to_speech/id/predict or /text_to_speech/en/predict
```
Description: This endpoint is used for direct inference on the entire input text at once, in either indonesian or english.

Usage:
- Simply type or paste the input text without any additional formatting.
- API will process the inference and returns the complete result after the process is finished.

Response:
Status code 200 on succes, including the generated audio.
```