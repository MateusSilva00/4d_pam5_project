import pickle
import socket

from src.logger import logger


class PAM5Client:
    def __init__(self):
        self.socket = None
        self.connected = False

    def connect(self, host: str = "0.0.0.0", port: int = 5225):
        """Connect to the PAM5 server."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            self.connected = True
            logger.info(f"Connected to server at {host}:{port}")
        except socket.error as e:
            logger.error(f"Failed to connect to server: {e}")
            self.connected = False

    def send_data(self, data: str):
        """Send data to the PAM5 server."""
        if not self.connected:
            raise ConnectionError("Client is not connected to the server.")

        try:
            serialized_data = pickle.dumps(data)
            data_size = len(serialized_data)
            self.socket.sendall(data_size.to_bytes(4, byteorder="big"))

            self.socket.sendall(serialized_data)
            logger.info(f"Sent data to server: {data}")
        except socket.error as e:
            logger.error(f"Failed to send data: {e}")
            raise e

    def disconnect(self):
        if self.socket:
            try:
                self.socket.close()
                logger.info("Disconnected from server.")
            except socket.error as e:
                logger.error(f"Error while disconnecting: {e}")
            finally:
                self.connected = False
                self.socket = None


if __name__ == "__main__":
    from src.crypto import encrypt_data
    from src.encoder import encoder_4d_pam5

    client = PAM5Client()

    try:
        client.connect()

        message = "Teste de comunicação!"
        key = "chave123"

        encrypted_bin = encrypt_data(message, key)
        symbols = encoder_4d_pam5(encrypted_bin)

        data = {"symbols": symbols, "key": key, "original_length": len(encrypted_bin)}

        client.send_data(data)
        print("Dados enviados com sucesso!")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        client.disconnect()
