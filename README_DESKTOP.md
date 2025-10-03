# Content Generation Motor - Desktop (Tkinter)

Este repositório contém uma interface desktop simples para o projeto **content-generation-motor**.
A interface usa **Tkinter** e chama os módulos já existentes em `app/real_time_prototype`.

## Arquivos adicionados
- `desktop_app.py` - aplicação desktop em Tkinter.
- `desktop_app.spec` - arquivo para uso com PyInstaller (nome do executável: **ContentGenerator**).
- `README_DESKTOP.md` - este arquivo.

## Requisitos
- Python 3.8+ (recomendado 3.9/3.10)
- Pip
- Dependências do projeto (ver `requirements.txt` caso exista no projeto)

## Instalação de dependências (exemplo)
```bash
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
.venv\Scripts\activate       # Windows (PowerShell/Command Prompt)
pip install --upgrade pip
# instalar dependências do projeto:
pip install -r requirements.txt || true
# instalar tkinter se não estiver disponível (em geral já vem com Python):
# Linux (Debian/Ubuntu): sudo apt install python3-tk
```

## Executando localmente
1. Ative seu ambiente virtual (veja acima).
2. Rode:
```bash
python desktop_app.py
```
3. A janela aparecerá com os 4 botões:
- **Iniciar Gravação/Transcrição**: tenta chamar `app/real_time_prototype/prototype.py` (import ou subprocess).
- **Selecionar Arquivo WAV**: abre diálogo para escolher um `.wav` e processa (salva resultado em `out/` se o código de transcrição fizer isso).
- **Criar Conteúdo (GPT)**: usa o arquivo `.txt` mais recente em `out/` e chama `app/real_time_prototype/generate_article.py` (import ou subprocess).
- **Enviar para Retool**: placeholder (apenas loga/print).

## Empacotando com PyInstaller
Instale PyInstaller:
```bash
pip install pyinstaller
```

### Comando (geral)
```bash
pyinstaller --onefile --add-data "app:app" --add-data ".env:." desktop_app.spec
```

> Observação: o formato de `--add-data` muda entre plataformas (use `;` em vez de `:` no Windows when necessary). O `desktop_app.spec` já tenta incluir `app/` e `.env`.

### Windows
```powershell
pyinstaller --onefile desktop_app.spec
# o executável ficará em dist\ContentGenerator.exe
```

### macOS / Linux
```bash
pyinstaller --onefile desktop_app.spec
# o executável ficará em dist/ContentGenerator
```

## Observações e dicas
- O código tenta importar funções dos módulos existentes em `app/real_time_prototype`. Se seus módulos tiverem entradas com nomes diferentes, ajuste `desktop_app.py` para chamar as funções corretas.
- Verifique se o diretório `out/` existe e é utilizado pelos seus módulos de transcrição/geração.
- Para suporte a microfone/gravação, garanta que as dependências do `prototype.py` (pyaudio, sounddevice, etc.) estejam instaladas.