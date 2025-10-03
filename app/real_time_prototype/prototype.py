import os
import queue
import sounddevice as sd
import numpy as np
import threading
import datetime
import soundfile as sf
import tempfile

import faster_whisper as whisper
from app import config


class RealtimeTranscriber:
    def __init__(self, model_path=None, out_queue: queue.Queue = None):
        self.model_path = model_path or config.WHISPER_MODEL
        device = config.WHISPER_DEVICE or "cpu"
        compute_type = config.WHISPER_COMPUTE_TYPE or "int8"
        self.model = whisper.WhisperModel(self.model_path, device=device, compute_type=compute_type)
        self.out_queue = out_queue
        self.running = False
        self.thread = None
        self.stream = None
        self.audio_chunks = []

    def _transcribe_chunk(self, chunk):
        """
        Salva temporariamente o chunk em WAV e transcreve com Whisper.
        """
        tmp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=True)
        sf.write(tmp_file.name, chunk, config.SAMPLERATE)
        try:
            segments, _ = self.model.transcribe(tmp_file.name, language=(config.WHISPER_LANGUAGE or None))
            transcript = " ".join(seg.text.strip() for seg in segments if getattr(seg, "text", None))
        except Exception as e:
            transcript = f"[Erro na transcrição do chunk: {e}]"
        finally:
            tmp_file.close()
        return transcript

    def _callback(self, indata, frames, time, status):
        if status:
            print(status)

        # Guarda o chunk
        self.audio_chunks.append(indata.copy())

        # --- Transcreve o chunk em tempo real ---
        transcript = self._transcribe_chunk(np.array(indata))
        if transcript.strip():
            out_msg = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {transcript}"
            if self.out_queue:
                self.out_queue.put(out_msg)
            else:
                print(out_msg)

    def start(self):
        if self.running:
            return
        self.running = True
        self.audio_chunks = []

        # Configura índice do dispositivo
        try:
            device_index = int(config.AUDIO_DEVICE_INDEX) if config.AUDIO_DEVICE_INDEX else None
        except ValueError:
            device_index = None

        # Obtém informações do dispositivo de áudio
        try:
            device_info = sd.query_devices(device_index, 'input') if device_index is not None else "Default"
        except Exception as e:
            device_info = f"Erro ao detectar dispositivo ({e})"

        # Mensagem inicial imediata
        start_msg = (
            "[desktop_app] Gravação iniciada\n"
            f"Modelo Whisper: {self.model_path}\n"
            f"Dispositivo de áudio: {device_info}\n"
            f"CHUNK_SECONDS: {config.CHUNK_SECONDS}\n"
            f"WHISPER_LANGUAGE: {config.WHISPER_LANGUAGE}"
        )
        if self.out_queue:
            self.out_queue.put(start_msg)
        else:
            print(start_msg)

        # Cria o stream de áudio
        self.stream = sd.InputStream(
            channels=1,
            samplerate=config.SAMPLERATE,
            callback=self._callback,
            blocksize=int(config.SAMPLERATE * config.CHUNK_SECONDS),
            device=device_index
        )
        self.stream.start()

        # Thread para manter a gravação viva
        self.thread = threading.Thread(target=self._process_audio)
        self.thread.start()

    def stop(self):
        if not self.running:
            return
        self.running = False

        # Mensagem imediata
        stop_msg = "[desktop_app] Gravação encerrada"
        if self.out_queue:
            self.out_queue.put(stop_msg)
        else:
            print(stop_msg)

        if self.stream:
            self.stream.stop()
            self.stream.close()
        if self.thread:
            self.thread.join()

        # --- Salva todo o áudio e a transcrição final ---
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs("out", exist_ok=True)
        tmp_wav = os.path.join("out", f"transcricao_{ts}.wav")
        audio_data = np.concatenate(self.audio_chunks, axis=0)
        sf.write(tmp_wav, audio_data, config.SAMPLERATE)

        # Transcrição final acumulada
        final_transcript = ""
        try:
            segments, _ = self.model.transcribe(tmp_wav, language=(config.WHISPER_LANGUAGE or None))
            final_transcript = " ".join(seg.text.strip() for seg in segments if getattr(seg, "text", None))
        except Exception as e:
            final_transcript = f"[Erro na transcrição final: {e}]"

        txt_path = tmp_wav.rsplit(".", 1)[0] + ".txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(final_transcript + "\n")

        save_msg = f"Salvo como:\n- Áudio: {tmp_wav}\n- Transcrição: {txt_path}"
        if self.out_queue:
            self.out_queue.put(save_msg)
        else:
            print(save_msg)

    def _process_audio(self):
        # Mantém a thread viva durante a gravação
        while self.running:
            sd.sleep(100)


# =========================================================
# Funções globais para desktop_app.py
# =========================================================
transcriber_instance = None

def run_transcriber(out_queue=None):
    global transcriber_instance
    if not transcriber_instance:
        transcriber_instance = RealtimeTranscriber(out_queue=out_queue)
        transcriber_instance.start()
    return transcriber_instance

def stop_transcriber():
    global transcriber_instance
    if transcriber_instance:
        transcriber_instance.stop()
        transcriber_instance = None
