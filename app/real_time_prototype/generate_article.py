import os
from datetime import datetime
import nltk
from dotenv import load_dotenv

from app.real_time_prototype.summarizer import summarize_text
from app.real_time_prototype.content_creator import ContentCreator  # importa a classe

# ==============================
# CARREGA VARIÁVEIS DO .ENV
# ==============================
load_dotenv()
SUMMARY_SENTENCES = int(os.getenv("SUMMARY_SENTENCES", "5"))

# ==============================
# VERIFICA RECURSOS NLTK
# ==============================
try:
    nltk.data.find("tokenizers/punkt_tab/portuguese")
except LookupError:
    nltk.download("punkt_tab")


def generate_article_from_file(transcript_file: str):
    """
    Recebe o caminho de um arquivo de transcrição, gera bullets e artigos via ContentCreator.
    Retorna lista de tuplas [(titulo, artigo), ...]
    """
    if not os.path.exists(transcript_file):
        raise FileNotFoundError(f"Arquivo não encontrado: {transcript_file}")

    # Lê o arquivo
    with open(transcript_file, "r", encoding="utf-8") as f:
        transcript_full = f.read().strip()

    if not transcript_full:
        raise ValueError("O arquivo de transcrição está vazio.")

    # ==============================
    # GERA RESUMO EM BULLETS
    # ==============================
    bullets = summarize_text(transcript_full, language="portuguese", sentences=SUMMARY_SENTENCES)

    # ==============================
    # CRIA ARTIGOS COM CONTENTCREATOR
    # ==============================
    creator = ContentCreator()
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    articles = creator.generate_articles(transcript_full, bullets, ts)

    return articles
