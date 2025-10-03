import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
PERSONA = os.getenv("PERSONA", "comunicador especializado em saúde")
EVENTO = os.getenv("EVENTO", "coletiva de imprensa")
TOM = os.getenv("TOM", "profissional e acessível")
PUBLICO = os.getenv("PUBLICO", "leitores interessados no tema")


class ContentCreator:
    def __init__(self, model: str = "gpt-4o", temperature: float = 0.7):
        self.model = model
        self.temperature = temperature

    def generate_articles(self, transcript: str, bullets: list = [], timestamp: str = "") -> list[tuple[str, str]]:
        """
        Gera até 3 artigos diferentes, baseados na transcrição e bullets.
        Retorna uma lista de tuplas [(titulo, artigo), ...].
        """
        prompt = f"""
Você é um {PERSONA}.
A partir da transcrição de uma palestra no {EVENTO}, crie até 3 artigos diferentes para blog.
O tom {TOM} e o público são {PUBLICO}.

Regras:
- Cada artigo deve ser distinto (ângulo, tom ou estilo).
- Não invente informações, apenas refine e organize o que está na transcrição.
- Crie títulos chamativos diferentes entre si.
- Estrutura: título, introdução, corpo (2 a 4 parágrafos) e conclusão.
- Evite separadores como '---'.
- Se houver palavras estranhas, corrija pelo contexto.
- Escreva textos sem usar travessões (—) e de forma profissional e correta.
- Busque referências científicas reais que possam embasar o conteúdo

Formato de saída esperado:
(Título 1)
Artigo 1

(Título 2)
Artigo 2

(Título 3)
Artigo 3

---
Resumo em tópicos: {bullets}
---
Transcrição completa:
{transcript}
"""

        resp = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature
        )

        raw_output = resp.choices[0].message.content.strip()

        # Parser simples
        articles = []
        parts = raw_output.split("(Título")
        for part in parts:
            if not part.strip():
                continue
            lines = part.strip().split("\n", 1)
            title_line = "(Título" + lines[0].strip()
            content = lines[1].strip() if len(lines) > 1 else ""
            articles.append((title_line, content))

        return articles


# Função atalho para desktop_app.py
def generate_article(transcript: str, bullets: list = [], timestamp: str = ""):
    creator = ContentCreator()
    return creator.generate_articles(transcript, bullets, timestamp)
