import os
from datetime import datetime
from dotenv import load_dotenv
from faster_whisper import WhisperModel

load_dotenv()

class ProcessBigFile:
    def __init__(self,
                 model_size: str = None,
                 language: str = None,
                 device: str = None):
        """
        model_size: base, small, medium, large
        language: 'pt' ou None para autodetect
        device: 'cuda' ou 'cpu'
        """
        self.model_size = model_size or os.getenv("WHISPER_MODEL", "base")
        self.language = language or os.getenv("WHISPER_LANGUAGE", None)
        self.device = device or ("cuda" if self._gpu_available() else "cpu")

        print(f"[MODEL] Carregando modelo {self.model_size} em {self.device}...")
        self.model = WhisperModel(self.model_size, device=self.device, compute_type="float16" if self.device=="cuda" else "int8")

    def _gpu_available(self):
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False

    def process_file(self, audio_path: str):
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {audio_path}")

        print(f"[PROCESS] Processando arquivo: {audio_path}")

        # Novo modo compatível com faster-whisper 1.2.0
        segments, info = self.model.transcribe(
            audio_path,
            language=self.language,
            beam_size=1,
            vad_filter=True
        )

        transcript_full = " ".join(seg.text.strip() for seg in segments)

        os.makedirs("out", exist_ok=True)
        base_name = os.path.basename(audio_path).replace(".wav", ".txt")
        out_path = os.path.join("out", base_name)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(transcript_full)

        print(f"[DONE] Transcrição salva em: {out_path}")
        return out_path, transcript_full


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python process_big_file.py <arquivo.wav>")
        exit(1)

    audio_file = sys.argv[1]
    processor = ProcessBigFile()
    processor.process_file(audio_file)
