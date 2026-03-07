from dotenv import load_dotenv
import os

load_dotenv()

with open("versions.txt", "r") as f:
    API_VERSION=f.read().strip()

API_TITLE="DIA TTS API"
API_DESC="Text to Speech"

RESOURCES = str(os.environ.get('RESOURCES'))
MODEL_NAME = str(os.environ.get("MODEL_NAME"))
HARDWARE= str(os.environ.get('HARDWARE'))
MODEL_DIR = os.path.join(RESOURCES, "models", MODEL_NAME, "model")

AUD_REF = str(os.environ.get('AUD_REF'))
SPEED_FACTOR = float(os.environ.get('SPEED_FACTOR'))

with open("{}/versions.txt".format(RESOURCES), "r") as f:
    MODEL_VERSION = f.read().strip()