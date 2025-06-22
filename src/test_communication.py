#!/usr/bin/env python3
"""
Teste de comunicação entre cliente e servidor 4D-PAM5
"""

import threading
import time

from src.client import PAM5Client
from src.crypto import decrypt_data, encrypt_data
from src.decoder import decoder_4d_pam5
from src.encoder import encoder_4d_pam5
from src.logger import logger
from src.server import PAM5Server


def test_server_callback(data):
    """Callback para processar mensagens recebidas pelo servidor"""
    logger.debug("Server callback")

    symbols = data["symbols"]
    key = data["key"]
    original_length = data.get("original_length", len(symbols) * 8)

    # Host B (recepção): aplicar algoritmo inverso
    ("\nAplicando algoritmo de decodificação...")
    recovered_bin = decoder_4d_pam5(symbols)

    # Transformação de binário para texto
    decrypted_msg = decrypt_data(recovered_bin[:original_length], key)
    logger.debug(f'Decrypted message: "{decrypted_msg}"')


def test_communication():
    # Iniciar servidor em thread separada
    server = PAM5Server()
    server_thread = threading.Thread(
        target=lambda: server.start(
            host="127.0.0.1", port=12345, message_callback=test_server_callback
        ),
        daemon=True,
    )
    server_thread.start()

    # Aguardar servidor iniciar
    time.sleep(1)

    try:
        client = PAM5Client()
        client.connect("127.0.0.1", 12345)

        logger.debug("Client sending message")

        # Host A (envio): processar dados
        message = "Teste"
        key = "10"

        encrypted_bin = encrypt_data(message, key)

        logger.debug(f"Encrypted binary: {encrypted_bin}")

        symbols = encoder_4d_pam5(encrypted_bin)

        data = {"symbols": symbols, "key": key, "original_length": len(encrypted_bin)}

        client.send_data(data)

        time.sleep(2)

        client.disconnect()

    except Exception as e:
        print(f"Erro no teste: {e}")
    finally:
        server.stop()


if __name__ == "__main__":
    test_communication()
