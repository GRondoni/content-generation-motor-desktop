import os
import sys
from datetime import datetime, timezone
from dotenv import load_dotenv

from faster_whisper import WhisperModel
from .summarizer import summarize_text
from .content_creator import ContentCreator
from .wordpress_publisher import publish_to_wordpress

load_dotenv()

MODEL_SIZE = os.getenv("WHISPER_MODEL", "base")
LANG = os.getenv("WHISPER_LANGUAGE", "") or None
SUMMARY_SENTENCES = int(os.getenv("SUMMARY_SENTENCES", "5"))
PUBLISH_WORDPRESS = os.getenv("PUBLISH_WORDPRESS", "false").lower() == "true"

def process_audio_file(audio_path: str):
    print(f"[FILE] Processando arquivo: {audio_path}")

    model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(audio_path, language=LANG)

    transcript_full = " ".join(seg.text.strip() for seg in segments)

    bullets = summarize_text(transcript_full, language="portuguese", sentences=SUMMARY_SENTENCES)

    creator = ContentCreator()
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    title, article_html = creator.generate_article(transcript_full, bullets, ts)


    if PUBLISH_WORDPRESS:
        publish_to_wordpress(title, article_html)
    else:
        os.makedirs("out", exist_ok=True)
        fname = f"out/article_from_file_{int(os.path.getmtime(audio_path))}.html"
        with open(fname, "w", encoding="utf-8") as f:
            f.write(article_html)
        print(f"[LOCAL] Artigo salvo: {fname}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python process_file.py <arquivo_de_audio>")
    else:
        process_audio_file(sys.argv[1])
