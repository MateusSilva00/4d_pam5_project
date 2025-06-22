# src/gui/app.py

import tkinter as tk
from tkinter import messagebox, ttk

from src.ascii_utils import text_to_binary
from src.crypto import decrypt_data, encrypt_data
from src.decoder import decoder_4d_pam5
from src.encoder import encoder_4d_pam5
from src.waveform import plot_waveform


class Pam5GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Codificador 4D-PAM5")
        self.geometry("800x600")

        # Mensagem
        ttk.Label(self, text="Mensagem:").pack()
        self.input_entry = ttk.Entry(self, width=80)
        self.input_entry.pack(pady=5)

        # Chave
        ttk.Label(self, text="Chave de criptografia:").pack()
        self.key_entry = ttk.Entry(self, width=40)
        self.key_entry.pack(pady=5)

        # Botão
        ttk.Button(self, text="Executar", command=self.processar).pack(pady=10)

        # Resultado
        self.result_text = tk.Text(self, height=20)
        self.result_text.pack(padx=10, pady=10, fill="both", expand=True)

    def processar(self):
        try:
            msg = self.input_entry.get()
            key = self.key_entry.get()

            if not msg or not key:
                messagebox.showwarning("Aviso", "Preencha a mensagem e a chave.")
                return

            # Criptografia
            encrypted_bin = encrypt_data(msg, key)

            # Codificação PAM5
            symbols = encoder_4d_pam5(encrypted_bin)

            # Decodificação reversa
            recovered_bin = decoder_4d_pam5(symbols)
            decrypted_msg = decrypt_data(recovered_bin[:len(encrypted_bin)], key)

            # Exibir resultados
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Mensagem original: {msg}\n")
            self.result_text.insert(tk.END, f"Chave: {key}\n\n")
            self.result_text.insert(tk.END, f"Binário da mensagem: {text_to_binary(msg)}\n\n")
            self.result_text.insert(tk.END, f"Binário criptografado: {encrypted_bin}\n\n")
            self.result_text.insert(tk.END, f"Símbolos codificados: {symbols}\n\n")
            self.result_text.insert(tk.END, f"Binário decodificado: {recovered_bin}\n\n")
            self.result_text.insert(tk.END, f"Mensagem final: {decrypted_msg}\n")

            # Exibir forma de onda
            plot_waveform(symbols, title="Forma de onda - 4D-PAM5")

        except Exception as e:
            messagebox.showerror("Erro", str(e))


if __name__ == "__main__":
    app = Pam5GUI()
    app.mainloop()
