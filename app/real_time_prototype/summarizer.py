import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.nlp.tokenizers import Tokenizer
from nltk.tokenize import sent_tokenize


try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

def summarize_text(text: str, language: str = "portuguese", sentences: int = 5):
    if not text or len(text.strip()) < 50:
        return []

    try:

        sentences_list = sent_tokenize(text, language=language)
        text_for_parser = "\n".join(sentences_list)


        parser = PlaintextParser.from_string(text_for_parser, Tokenizer(language))
        
        summarizer = TextRankSummarizer()
        summary_sentences = summarizer(parser.document, sentences)
        return [str(s) for s in summary_sentences]

    except Exception as e:
        print(f"[ERRO] Erro ao resumir texto: {e}")
        return []
