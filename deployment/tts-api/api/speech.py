import io
import soundfile as sf
import config
import traceback

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO

from utils.helpers import normalization_id, normalization_en
from models.dia.dia import VoiceCloning as dia

text_to_speech_id = APIRouter(
    prefix="/text_to_speech",
    tags=["ID"]
)

text_to_speech_en = APIRouter(
    prefix="/text_to_speech",
    tags=['EN']
)

check_router = APIRouter(
    prefix="/my_endpoint"
)

model_name = config.MODEL_NAME
if model_name == "dia":
    model = dia()
else:
    raise ValueError(f"Model '{model_name}' is not supported / select your model name!")

normalizer_id = normalization_id()
normalizer_en = normalization_en()

@text_to_speech_id.get("/id/predict")
async def read_sentence(text: str):

    text_cl = normalizer_id.preprocess(text)
    
    if model_name == "dia":
        try:
            sr, wav = model.predict(text_cl)
            audio_io = io.BytesIO()
            sf.write(audio_io, wav, sr, format="WAV")

        except Exception as e:
            error = e.__str__()
            traceback.print_exc()
            raise HTTPException(status_code=404, detail=error)
        
    else:
        raise HTTPException(status_code=404, detail=f"Model '{model_name}' is not supported / select your model name!")

    audio_io.seek(0)

    return StreamingResponse(audio_io, media_type="audio/wav")


@text_to_speech_en.get("/en/predict")
async def read_sentence(text: str):

    text_cl = normalizer_en.preprocess(text)
        
    if model_name == "dia":
        try:
            sr, wav = model.predict(text_cl)
            audio_io = io.BytesIO()
            sf.write(audio_io, wav, sr, format="WAV")

        except Exception as e:
            error = e.__str__()
            traceback.print_exc()
            raise HTTPException(status_code=404, detail=error)

    else:
        raise HTTPException(status_code=404, detail=f"Model '{model_name}' is not supported / select your model name!")
    
    audio_io.seek(0)

    return StreamingResponse(audio_io, media_type="audio/wav")