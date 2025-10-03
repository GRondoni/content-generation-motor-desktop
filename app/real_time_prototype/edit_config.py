# app/real_time_prototype/edit_config.py
import tkinter as tk
from tkinter import ttk
from app import config
import sounddevice as sd

class EditConfig:
    def __init__(self, master):
        self.master = master
        self.top = tk.Toplevel(master)
        self.top.title("Configurações")
        self.top.geometry("450x400")
        self.top.configure(bg="#160028")

        self.create_fields()

    def create_fields(self):
        # Labels e campos
        labels = [
            "Modelo de conteúdo", "Persona", "Tom", "Evento", "Publico",
            "Tamanho das chunks", "Dispositivo de áudio"
        ]
        self.entries = {}

        # Cria lista de dispositivos de áudio
        devices = sd.query_devices()
        input_devices = [f"{d['name']} (index {i})" for i, d in enumerate(devices) if d['max_input_channels'] > 0]

        for i, label in enumerate(labels):
            tk.Label(self.top, text=label, bg="#160028", fg="white").grid(row=i, column=0, sticky="w", padx=10, pady=5)
            if label == "Dispositivo de áudio":
                combo = ttk.Combobox(self.top, values=input_devices, state="readonly", width=35)
                # Seleciona o dispositivo atual
                if config.AUDIO_DEVICE_NAME:
                    combo.set(config.AUDIO_DEVICE_NAME)
                elif config.AUDIO_DEVICE_INDEX:
                    combo.set(f"{devices[int(config.AUDIO_DEVICE_INDEX)]['name']} (index {config.AUDIO_DEVICE_INDEX})")
                self.entries[label] = combo
                combo.grid(row=i, column=1, padx=10, pady=5)
            else:
                entry = tk.Entry(self.top, width=40)
                # Define valor atual
                if label == "Modelo de conteúdo":
                    entry.insert(0, config.WHISPER_MODEL)
                elif label == "Persona":
                    entry.insert(0, config.PERSONA)
                elif label == "Tom":
                    entry.insert(0, config.TOM)
                elif label == "Evento":
                    entry.insert(0, config.EVENTO)
                elif label == "Publico":
                    entry.insert(0, config.PUBLICO)
                elif label == "Tamanho das chunks":
                    entry.insert(0, str(config.CHUNK_SECONDS))
                self.entries[label] = entry
                entry.grid(row=i, column=1, padx=10, pady=5)

        # Botões Salvar / Cancelar
        tk.Button(self.top, text="Salvar", width=12, command=self.save_settings).grid(row=len(labels), column=0, padx=10, pady=15)
        tk.Button(self.top, text="Cancelar", width=12, command=self.top.destroy).grid(row=len(labels), column=1, padx=10, pady=15)

    def save_settings(self):
        # Atualiza config.py diretamente (pode ser modificado para salvar no .env)
        for k, widget in self.entries.items():
            value = widget.get()
            if k == "Modelo de conteúdo":
                config.WHISPER_MODEL = value
            elif k == "Persona":
                config.PERSONA = value
            elif k == "Tom":
                config.TOM = value
            elif k == "Evento":
                config.EVENTO = value
            elif k == "Publico":
                config.PUBLICO = value
            elif k == "Tamanho das chunks":
                config.CHUNK_SECONDS = int(value)
            elif k == "Dispositivo de áudio":
                # Extrai o index do combo selecionado
                idx = int(value.split("index ")[1].replace(")", ""))
                config.AUDIO_DEVICE_INDEX = str(idx)
                config.AUDIO_DEVICE_NAME = value.split(" (index")[0]

        self.top.destroy()
