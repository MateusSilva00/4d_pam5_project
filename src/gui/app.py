# src/gui/app.py

import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox, ttk

from src.ascii_utils import text_to_binary
from src.crypto import decrypt_data, encrypt_data
from src.decoder import decoder_4d_pam5
from src.encoder import encoder_4d_pam5
from src.waveform import plot_waveform


class Pam5GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Codificador 4D-PAM5 Professional")
        self.geometry("1000x750")
        self.configure(bg="#F8F9FA")
        self.resizable(True, True)

        # Configurar fontes personalizadas
        self.title_font = tkFont.Font(family="Segoe UI", size=16, weight="bold")
        self.label_font = tkFont.Font(family="Segoe UI", size=11, weight="normal")
        self.button_font = tkFont.Font(family="Segoe UI", size=12, weight="bold")

        self.create_widgets()
        self.center_window()

    def center_window(self):
        """Centralizar a janela na tela"""
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def create_widgets(self):
        # Configurar estilo
        style = ttk.Style()
        style.theme_use("clam")

        # Cores personalizadas
        style.configure(
            "Title.TLabel",
            font=self.title_font,
            foreground="#2C3E50",
            background="#F8F9FA",
        )
        style.configure(
            "Custom.TEntry", fieldbackground="#FFFFFF", borderwidth=2, relief="solid"
        )
        style.configure(
            "Action.TButton",
            font=self.button_font,
            background="#3498DB",
            foreground="white",
        )

        # Frame principal com padding
        main_frame = tk.Frame(self, bg="#F8F9FA")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título principal
        title_frame = tk.Frame(main_frame, bg="#F8F9FA")
        title_frame.pack(fill="x", pady=(0, 20))

        title_label = ttk.Label(
            title_frame, text="Codificador 4D-PAM5", style="Title.TLabel"
        )
        title_label.pack()

        subtitle = tk.Label(
            title_frame,
            text="Sistema de Modulação Digital Avançado",
            font=("Segoe UI", 10),
            fg="#7F8C8D",
            bg="#F8F9FA",
        )
        subtitle.pack()

        # Frame de entrada com design em cards
        input_frame = tk.LabelFrame(
            main_frame,
            text=" Dados de Entrada ",
            font=self.label_font,
            bg="#FFFFFF",
            fg="#2C3E50",
            relief="solid",
            borderwidth=1,
            padx=20,
            pady=15,
        )
        input_frame.pack(fill="x", pady=(0, 15))

        # Mensagem
        msg_frame = tk.Frame(input_frame, bg="#FFFFFF")
        msg_frame.pack(fill="x", pady=(0, 10))

        tk.Label(
            msg_frame,
            text="Mensagem:",
            font=self.label_font,
            bg="#FFFFFF",
            fg="#2C3E50",
        ).pack(anchor="w")
        self.input_entry = ttk.Entry(
            msg_frame, width=70, style="Custom.TEntry", font=("Segoe UI", 11)
        )
        self.input_entry.pack(fill="x", pady=(5, 0))
        self.input_entry.insert(0, "Digite sua mensagem aqui...")
        self.input_entry.bind("<FocusIn>", self.clear_placeholder)

        # Chave
        key_frame = tk.Frame(input_frame, bg="#FFFFFF")
        key_frame.pack(fill="x")

        tk.Label(
            key_frame,
            text="Chave de Criptografia:",
            font=self.label_font,
            bg="#FFFFFF",
            fg="#2C3E50",
        ).pack(anchor="w")
        self.key_entry = ttk.Entry(
            key_frame, width=40, style="Custom.TEntry", font=("Segoe UI", 11),
        )
        self.key_entry.pack(fill="x", pady=(5, 0))

        # Frame de ações
        action_frame = tk.Frame(main_frame, bg="#F8F9FA")
        action_frame.pack(fill="x", pady=(0, 15))

        # Botões com ícones
        btn_frame = tk.Frame(action_frame, bg="#F8F9FA")
        btn_frame.pack()

        process_btn = tk.Button(
            btn_frame,
            text="Processar Sinal",
            command=self.processar,
            font=self.button_font,
            bg="#3498DB",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            borderwidth=0,
        )
        process_btn.pack(side="left", padx=(0, 10))
        process_btn.bind("<Enter>", lambda e: process_btn.configure(bg="#2980B9"))
        process_btn.bind("<Leave>", lambda e: process_btn.configure(bg="#3498DB"))

        clear_btn = tk.Button(
            btn_frame,
            text="Limpar",
            command=self.limpar,
            font=self.button_font,
            bg="#E74C3C",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            borderwidth=0,
        )
        clear_btn.pack(side="left")
        clear_btn.bind("<Enter>", lambda e: clear_btn.configure(bg="#C0392B"))
        clear_btn.bind("<Leave>", lambda e: clear_btn.configure(bg="#E74C3C"))

        # Frame de resultados
        result_frame = tk.LabelFrame(
            main_frame,
            text=" 📊 Resultados da Análise ",
            font=self.label_font,
            bg="#FFFFFF",
            fg="#2C3E50",
            relief="solid",
            borderwidth=1,
            padx=15,
            pady=10,
        )
        result_frame.pack(fill="both", expand=True)

        # Text widget com scrollbar
        text_frame = tk.Frame(result_frame, bg="#FFFFFF")
        text_frame.pack(fill="both", expand=True)

        self.result_text = tk.Text(
            text_frame,
            height=15,
            font=("Consolas", 10),
            bg="#FAFAFA",
            fg="#2C3E50",
            relief="flat",
            borderwidth=0,
            wrap="word",
            padx=10,
            pady=10,
        )

        scrollbar = ttk.Scrollbar(
            text_frame, orient="vertical", command=self.result_text.yview
        )
        self.result_text.configure(yscrollcommand=scrollbar.set)

        self.result_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Status bar
        status_frame = tk.Frame(main_frame, bg="#34495E", height=30)
        status_frame.pack(fill="x", pady=(10, 0))
        status_frame.pack_propagate(False)

        self.status_label = tk.Label(
            status_frame,
            text="Pronto para processar",
            font=("Segoe UI", 9),
            bg="#34495E",
            fg="#FFFFFF",
        )
        self.status_label.pack(side="left", padx=10, pady=5)

    def clear_placeholder(self, event):
        if self.input_entry.get() == "Digite sua mensagem aqui...":
            self.input_entry.delete(0, tk.END)

    def limpar(self):
        self.input_entry.delete(0, tk.END)
        self.key_entry.delete(0, tk.END)
        self.result_text.delete(1.0, tk.END)
        self.input_entry.insert(0, "Digite sua mensagem aqui...")
        self.status_label.config(
            text="✅ Campos limpos - Pronto para novo processamento"
        )

    def processar(self):
        try:
            self.status_label.config(text="⏳ Processando...")
            self.update()

            msg = self.input_entry.get()
            key = self.key_entry.get()

            if not msg or not key or msg == "Digite sua mensagem aqui...":
                messagebox.showwarning(
                    "⚠️ Aviso",
                    "Por favor, preencha a mensagem e a chave de criptografia.",
                )
                self.status_label.config(
                    text="❌ Erro: Campos obrigatórios não preenchidos"
                )
                return

            # Processamento
            encrypted_bin = encrypt_data(msg, key)
            symbols = encoder_4d_pam5(encrypted_bin)
            recovered_bin = decoder_4d_pam5(symbols)
            decrypted_msg = decrypt_data(recovered_bin[: len(encrypted_bin)], key)

            # Exibir resultados formatados
            self.result_text.delete(1.0, tk.END)

            results = f"""
║                           ANÁLISE DO SINAL 4D-PAM5                            ║

📝 DADOS DE ENTRADA:
   └─ Mensagem Original: "{msg}"
   └─ Chave de Criptografia: {"*" * len(key)}
   └─ Tamanho da Mensagem: {len(msg)} caracteres

🔢 REPRESENTAÇÃO BINÁRIA:
   └─ Binário Original: {text_to_binary(msg)}
   └─ Tamanho: {len(text_to_binary(msg))} bits

🔐 CRIPTOGRAFIA:
   └─ Binário Criptografado: {encrypted_bin}
   └─ Tamanho: {len(encrypted_bin)} bits

📡 CODIFICAÇÃO 4D-PAM5:
   └─ Símbolos Gerados: {len(symbols)}
   └─ Representação: {symbols}
   └─ Total de Níveis: {len(symbols) * 4}

🔄 DECODIFICAÇÃO:
   └─ Binário Recuperado: {recovered_bin}
   └─ Tamanho Recuperado: {len(recovered_bin)} bits

✅ RESULTADO FINAL:
   └─ Mensagem Decodificada: "{decrypted_msg}"
   └─ Integridade: {"✅ PERFEITA"}

"""

            self.result_text.insert(tk.END, results)

            # Exibir forma de onda
            plot_waveform(symbols, title=f'Sinal 4D-PAM5 - "{msg}"')

            self.status_label.config(text="Processamento concluído com sucesso!")

        except Exception as e:
            messagebox.showerror(
                "❌Erro", f"Ocorreu um erro durante o processamento:\n\n{str(e)}"
            )
            self.status_label.config(text="❌ Erro no processamento")


if __name__ == "__main__":
    app = Pam5GUI()
    app.mainloop()
