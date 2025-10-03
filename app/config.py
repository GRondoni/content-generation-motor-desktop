from dotenv import load_dotenv
import os

load_dotenv()  # Carrega variáveis do arquivo .env

# Whisper
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")
WHISPER_LANGUAGE = os.getenv("WHISPER_LANGUAGE", "pt")
CHUNK_SECONDS = int(os.getenv("CHUNK_SECONDS", 5))
SAMPLERATE = int(os.getenv("SAMPLERATE", 16000))  # 🔥 novo: taxa de amostragem

# Dispositivo de áudio
AUDIO_DEVICE_INDEX = os.getenv("AUDIO_DEVICE_INDEX", "")
AUDIO_DEVICE_NAME = os.getenv("AUDIO_DEVICE_NAME", "")

# Device e compute type do Whisper (opcionais)
WHISPER_DEVICE = os.getenv("WHISPER_DEVICE", "") or None
WHISPER_COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "") or None

# WordPress
WP_URL = os.getenv("WP_URL")
WP_USER = os.getenv("WP_USER")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")
WP_STATUS = os.getenv("WP_STATUS", "draft")
PUBLISH_WORDPRESS = os.getenv("PUBLISH_WORDPRESS", "false").lower() == "true"

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUMMARY_SENTENCES = int(os.getenv("SUMMARY_SENTENCES", 5))

# Personalização
PERSONA = os.getenv("PERSONA", "")
EVENTO = os.getenv("EVENTO", "")
TOM = os.getenv("TOM", "")
PUBLICO = os.getenv("PUBLICO", "")
