import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

from src.ascii_utils import binary_to_text, text_to_binary
from src.client import PAM5Client
from src.crypto import decrypt_data, encrypt_data
from src.decoder import decoder_4d_pam5
from src.encoder import encoder_4d_pam5
from src.server import PAM5Server
from src.waveform import plot_waveform


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("4D-PAM5 Comunicação - Host A e Host B")
        self.geometry("1200x800")
        self.resizable(True, True)
        self.client = None
        self.server = None
        self.server_thread = None

        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Título principal
        title_label = ttk.Label(main_frame, text="Sistema de Comunicação 4D-PAM5", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))

        # Frame para botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)

        self.btn_cliente = ttk.Button(button_frame, text="HOST A (Cliente)", 
                                    command=self.start_cliente, width=20)
        self.btn_cliente.grid(row=0, column=0, padx=10)

        self.btn_servidor = ttk.Button(button_frame, text="HOST B (Servidor)", 
                                     command=self.start_servidor, width=20)
        self.btn_servidor.grid(row=0, column=1, padx=10)

        # Frame para área de exibição
        display_frame = ttk.Frame(main_frame)
        display_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Área de exibição com scrollbar
        self.txt_area = scrolledtext.ScrolledText(display_frame, width=140, height=35, 
                                                font=("Consolas", 10), wrap=tk.WORD)
        self.txt_area.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto para iniciar comunicação")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                             relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

    def start_cliente(self):
        self.clear_area()
        self.status_var.set("Modo HOST A (Cliente) iniciado")
        self.add_separator("HOST A - PROCESSO DE ENVIO")
        self.txt_area.insert(tk.END, "HOST A iniciado - Preparando para enviar mensagem...\n\n")
        self.cliente_window()

    def start_servidor(self):
        self.clear_area()
        self.status_var.set("Modo HOST B (Servidor) iniciado - Aguardando conexão...")
        self.add_separator("HOST B - PROCESSO DE RECEPÇÃO")
        self.txt_area.insert(tk.END, "HOST B iniciado - Aguardando mensagem do HOST A...\n\n")
        
        try:
            self.server = PAM5Server()
            self.server_thread = threading.Thread(
                target=lambda: self.server.start(
                    host="0.0.0.0", port=5225, message_callback=self.server_callback
                ),
                daemon=True,
            )
            self.server_thread.start()
            self.txt_area.insert(tk.END, "✓ Servidor ativo na porta 5225\n")
            self.txt_area.insert(tk.END, "✓ Aguardando conexão do HOST A...\n\n")
        except Exception as e:
            self.txt_area.insert(tk.END, f"✗ Erro ao iniciar servidor: {e}\n")

    def cliente_window(self):
        win = tk.Toplevel(self)
        win.title("HOST A - Enviar Mensagem")
        win.geometry("500x300")
        win.resizable(False, False)
        win.grab_set()  # Modal window

        # Frame principal
        main_frame = ttk.Frame(win)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Mensagem
        ttk.Label(main_frame, text="Digite a mensagem:", font=("Arial", 11)).pack(anchor="w", pady=(0,5))
        entry_msg = tk.Entry(main_frame, width=60, font=("Arial", 11))
        entry_msg.pack(pady=(0,15))
        entry_msg.focus()

        # Chave
        ttk.Label(main_frame, text="Digite a chave de criptografia:", font=("Arial", 11)).pack(anchor="w", pady=(0,5))
        entry_key = tk.Entry(main_frame, width=40, font=("Arial", 11), show="*")
        entry_key.pack(pady=(0,20))

        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack()

        def enviar():
            msg = entry_msg.get().strip()
            key = entry_key.get().strip()
            if not msg or not key:
                messagebox.showerror("Erro", "Preencha a mensagem e a chave de criptografia.")
                return
            self.processar_cliente(msg, key)
            win.destroy()

        def cancelar():
            win.destroy()

        ttk.Button(button_frame, text="Enviar", command=enviar, width=15).pack(side=tk.LEFT, padx=(0,10))
        ttk.Button(button_frame, text="Cancelar", command=cancelar, width=15).pack(side=tk.LEFT)

        # Bind Enter key
        win.bind('<Return>', lambda e: enviar())

    def processar_cliente(self, msg, key):
        self.txt_area.insert(tk.END, "ETAPA 1: Digitação do texto\n")
        self.txt_area.insert(tk.END, f"→ Mensagem original: '{msg}'\n")
        self.txt_area.insert(tk.END, f"→ Tamanho: {len(msg)} caracteres\n\n")

        # Transformação em binário (antes da criptografia)
        self.txt_area.insert(tk.END, "ETAPA 2: Transformação em binário\n")
        binario_original = text_to_binary(msg)
        self.txt_area.insert(tk.END, f"→ Binário original: {binario_original}\n")
        self.txt_area.insert(tk.END, f"→ Tamanho: {len(binario_original)} bits\n\n")

        # Criptografia
        self.txt_area.insert(tk.END, "ETAPA 3: Aplicação do algoritmo de criptografia\n")
        self.txt_area.insert(tk.END, f"→ Chave utilizada: '{key}'\n")
        encrypted_bin = encrypt_data(msg, key)
        self.txt_area.insert(tk.END, f"→ Mensagem criptografada (binário): {encrypted_bin}\n")
        self.txt_area.insert(tk.END, f"→ Tamanho após criptografia: {len(encrypted_bin)} bits\n\n")

        # Codificação 4D-PAM5
        self.txt_area.insert(tk.END, "ETAPA 4: Aplicação do algoritmo de codificação de linha (4D-PAM5)\n")
        symbols = encoder_4d_pam5(encrypted_bin)
        self.txt_area.insert(tk.END, f"→ Símbolos 4D-PAM5 gerados: {symbols}\n")
        self.txt_area.insert(tk.END, f"→ Número de símbolos: {len(symbols)}\n")
        self.txt_area.insert(tk.END, f"→ Cada símbolo: (nível1, nível2, nível3, nível4)\n")
        self.txt_area.insert(tk.END, f"→ Níveis possíveis: -2, -1, +1, +2\n\n")

        # Gráfico
        self.txt_area.insert(tk.END, "ETAPA 5: Apresentação do gráfico da forma de onda\n")
        self.txt_area.insert(tk.END, "→ Gerando gráfico da forma de onda 4D-PAM5...\n")
        plot_waveform(symbols, title="HOST A - Sinal 4D-PAM5 (Processo de Montagem)")
        self.txt_area.insert(tk.END, "✓ Gráfico exibido com sucesso!\n\n")

        # Envio
        self.txt_area.insert(tk.END, "ETAPA 6: Envio para o HOST B\n")
        try:
            self.client = PAM5Client()
            self.client.connect("127.0.0.1", 5225)
            data = {
                "symbols": symbols, 
                "key": key, 
                "original_length": len(encrypted_bin),
                "original_message": msg
            }
            self.client.send_data(data)
            self.txt_area.insert(tk.END, "✓ Mensagem enviada ao HOST B com sucesso!\n")
            self.txt_area.insert(tk.END, "→ Aguardando processamento no HOST B...\n\n")
            self.client.disconnect()
            self.status_var.set("Mensagem enviada com sucesso - Aguardando HOST B processar")
        except Exception as e:
            self.txt_area.insert(tk.END, f"✗ Erro ao enviar para HOST B: {e}\n")
            self.txt_area.insert(tk.END, "→ Verifique se o HOST B está ativo\n\n")
            self.status_var.set("Erro no envio - Verifique conexão")

    def server_callback(self, data):
        try:
            # Recepção
            symbols = data["symbols"]
            key = data["key"]
            original_length = data.get("original_length", len(symbols) * 8)
            
            self.txt_area.insert(tk.END, "="*80 + "\n")
            self.txt_area.insert(tk.END, "RECEPÇÃO NO HOST B - PROCESSAMENTO INICIADO\n")
            self.txt_area.insert(tk.END, "="*80 + "\n\n")

            # Etapa 1: Recepção
            self.txt_area.insert(tk.END, "ETAPA 1: Recepção dos dados\n")
            self.txt_area.insert(tk.END, f"✓ Símbolos recebidos do HOST A: {symbols}\n")
            self.txt_area.insert(tk.END, f"→ Número de símbolos: {len(symbols)}\n")
            self.txt_area.insert(tk.END, f"→ Chave recebida: '{key}'\n\n")

            # Etapa 2: Apresentar gráfico
            self.txt_area.insert(tk.END, "ETAPA 2: Apresentação do gráfico da forma de onda recebida\n")
            self.txt_area.insert(tk.END, "→ Gerando gráfico da forma de onda recebida...\n")
            plot_waveform(symbols, title="HOST B - Sinal 4D-PAM5 (Processo Inverso)")
            self.txt_area.insert(tk.END, "✓ Gráfico da recepção exibido com sucesso!\n\n")

            # Etapa 3: Decodificação 4D-PAM5
            self.txt_area.insert(tk.END, "ETAPA 3: Aplicação do algoritmo de codificação de linha (modo inverso)\n")
            recovered_bin = decoder_4d_pam5(symbols)
            self.txt_area.insert(tk.END, f"→ Binário decodificado: {recovered_bin[:original_length]}\n")
            self.txt_area.insert(tk.END, f"→ Tamanho: {len(recovered_bin[:original_length])} bits\n\n")

            # Etapa 4: Descriptografia
            self.txt_area.insert(tk.END, "ETAPA 4: Aplicação do algoritmo de criptografia (modo inverso)\n")
            decrypted_msg = decrypt_data(recovered_bin[:original_length], key)
            self.txt_area.insert(tk.END, f"→ Mensagem descriptografada: '{decrypted_msg}'\n\n")

            # Etapa 5: Transformação para ASCII
            self.txt_area.insert(tk.END, "ETAPA 5: Transformação de binário para ASCII\n")
            self.txt_area.insert(tk.END, f"→ Texto final em ASCII: '{decrypted_msg}'\n\n")

            # Etapa 6: Resultado final
            self.txt_area.insert(tk.END, "ETAPA 6: Mensagem final\n")
            self.txt_area.insert(tk.END, f"✓ MENSAGEM RECEBIDA COM SUCESSO: '{decrypted_msg}'\n\n")
            
            self.add_separator("COMUNICAÇÃO FINALIZADA COM SUCESSO")
            self.status_var.set("Comunicação HOST A → HOST B finalizada com sucesso")

        except Exception as e:
            self.txt_area.insert(tk.END, f"✗ Erro no processamento HOST B: {e}\n")
            self.status_var.set("Erro no processamento HOST B")

    def add_separator(self, title=""):
        self.txt_area.insert(tk.END, "="*80 + "\n")
        if title:
            self.txt_area.insert(tk.END, f"{title:^80}\n")
            self.txt_area.insert(tk.END, "="*80 + "\n")

    def clear_area(self):
        self.txt_area.delete("1.0", tk.END)

    def on_closing(self):
        if self.server:
            self.server.stop()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
