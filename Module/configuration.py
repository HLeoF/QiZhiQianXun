import os
from dotenv import load_dotenv

load_dotenv("D:/LLMs Projects/enviroment.env")

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

MODELS = [
    "gpt-4o",
    "gpt-4-turbo",
    "gpt-4",
    "gpt-3.5-turbo",
]

# Default model: GPT-3.5-turbo
DEFAULT_MODEL = MODELS[3]

MODEL_TO_MAX_TOKENS = {
    "gpt-4o":4096,
    "gpt-4-turbo":4096,
    "gpt-4":8192,
    "gpt-3.5-turbo":4096,
}

QDRANT_HOST = "localhost"
QDRANT_PORT = 6333

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

DEFAULT_MAX_TOKENS = 2000

VOICE_LANGUAGE = [
    'zh-CN',
    'en-US',
    'es-ES',
]


DEFAULT_VOICE_LANGUAGE = VOICE_LANGUAGE[0]

VOICE_MODEL = [
    "zh-CN-shaanxi-XiaoniNeural",
    "zh-CN-liaoning-XiaobeiNeural",
    "zh-HK-WanLungNeural"
    "zh-CN-XiaoxiaoNeural",
    "zh-CN-YunxiNeural",
    "zh-CN-liaoning-XiaobeiNeural",
    "en-US-AriaNeural",
    "en-US-GuyNeural",
    "es-ES-ElviraNeural",
    "es-ES-AlvaroNeural",
]

DEFAULT_VOICE_MODEL = VOICE_MODEL[1]