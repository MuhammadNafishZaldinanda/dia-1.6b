import sys
import config

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from api.speech import text_to_speech_id, text_to_speech_en, check_router
from api.ping import ping_router

logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")

origins = [
    "http://localhost",
]
app = FastAPI(title=config.API_TITLE)

api_app = FastAPI(title=config.API_TITLE, version=config.API_VERSION, description=config.API_DESC)
model_name = config.MODEL_NAME


api_app.include_router(text_to_speech_id)
api_app.include_router(text_to_speech_en)
api_app.include_router(check_router)
api_app.include_router(ping_router)
    
app.mount("/api", api_app)

@app.api_route("/")
def get():
    return {"api_version": config.API_VERSION, "model_version": config.MODEL_VERSION}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)