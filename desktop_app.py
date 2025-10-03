import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import time
import threading
import queue

from app.real_time_prototype import prototype
from app.real_time_prototype.content_creator import generate_article
from app.real_time_prototype.edit_config import EditConfig  # Import da classe EditConfig

# Fila para comunicação com a thread do transcriber
output_queue = queue.Queue()

# Controle de thread
transcriber_thread = None

def start_transcriber():
    global transcriber_thread
    if transcriber_thread is None or not transcriber_thread.is_alive():
        transcriber_thread = threading.Thread(target=prototype.run_transcriber, args=(output_queue,))
        transcriber_thread.start()
        log_message("[desktop_app] Gravação iniciada...")
    else:
        log_message("O transcritor já está em execução.")

def stop_transcriber():
    prototype.stop_transcriber()
    log_message("[desktop_app] Gravação encerrada")

def check_queue():
    try:
        while True:
            msg = output_queue.get_nowait()
            log_message(msg)
    except queue.Empty:
        pass
    root.after(200, check_queue)

def log_message(message):
    text_output.config(state=tk.NORMAL)
    text_output.insert(tk.END, message + "\n")
    text_output.see(tk.END)
    text_output.config(state=tk.DISABLED)

def gerar_conteudo():
    file_path = filedialog.askopenfilename(
        initialdir="out",
        title="Selecione o arquivo de transcrição",
        filetypes=[("Arquivos de texto", "*.txt")]
    )

    if not file_path:
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            texto = f.read()

        if not texto.strip():
            messagebox.showwarning("Aviso", "O arquivo de transcrição está vazio.")
            return

        conteudo = generate_article(texto)

        ts = time.strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join("out", f"conteudo_{ts}.txt")

        # Se conteudo for lista de artigos, transforma em string concatenada
        if isinstance(conteudo, list):
            conteudo_text = "\n\n".join([f"{title}\n{body}" for title, body in conteudo])
        else:
            conteudo_text = str(conteudo)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(conteudo_text)

        # Exibe na tela o conteúdo gerado
        log_message(f"Conteúdo gerado:\n{conteudo_text}")
        messagebox.showinfo("Sucesso", f"Conteúdo gerado e salvo em:\n{output_file}")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar conteúdo: {e}")

def clear_screen():
    text_output.config(state=tk.NORMAL)
    text_output.delete(1.0, tk.END)
    text_output.config(state=tk.DISABLED)

def open_settings():
    EditConfig(root)  # Chama a classe EditConfig

# ========================
# Interface Tkinter
# ========================
root = tk.Tk()
root.title("Aplicativo de Transcrição")
root.geometry("700x500")
root.configure(bg="#160028")

# ========================
# Configuração de estilos ttk
# ========================
style = ttk.Style()
style.theme_use('clam')
style.configure("TButton",
                background="#2C004F",
                foreground="white",
                font=("Arial", 12),
                borderwidth=0,
                focusthickness=3,
                focuscolor='none')
style.map("TButton",
          background=[('active', '#3D005F')],
          foreground=[('active', 'white')])

# Título
try:
    inter_font = ("Inter", 20, "bold")
except:
    inter_font = ("Arial", 20, "bold")

label_title = tk.Label(root, text="TribeMD", font=inter_font, bg="#160028", fg="white")
label_title.pack(pady=10)

# Frame para botões de gravação
frame_buttons = tk.Frame(root, bg="#160028")
frame_buttons.pack(pady=10)

btn_start = ttk.Button(frame_buttons, text="Iniciar Transcrição", command=start_transcriber, style="TButton")
btn_start.grid(row=0, column=0, padx=10)
btn_stop = ttk.Button(frame_buttons, text="Parar Transcrição", command=stop_transcriber, style="TButton")
btn_stop.grid(row=0, column=1, padx=10)
btn_generate = ttk.Button(frame_buttons, text="Gerar Conteúdo", command=gerar_conteudo, style="TButton")
btn_generate.grid(row=0, column=2, padx=10)

text_output = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED,
                      bg="#160028", fg="white", insertbackground="white")
text_output.pack(expand=True, fill="both", padx=10, pady=10)

frame_bottom = tk.Frame(root, bg="#160028")
frame_bottom.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5, anchor="e")

btn_clear = ttk.Button(frame_bottom, text="Clear", command=clear_screen, style="TButton")
btn_clear.pack(side=tk.RIGHT, padx=5)
btn_settings = ttk.Button(frame_bottom, text="Configuração", command=open_settings, style="TButton")
btn_settings.pack(side=tk.RIGHT, padx=5)


root.after(200, check_queue)
root.mainloop()
