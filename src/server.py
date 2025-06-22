import pickle
import socket
import threading

from src.logger import logger


class PAM5Server:
    def __init__(self):
        self.socket = None
        self.running = False
        self.clients = []

    def start(self, host="127.0.0.1", port=12345, message_callback=None):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((host, port))
            self.socket.listen(5)
            self.running = True

            logger.info(f"Server running on {host}:{port}")

            while self.running:
                try:
                    client_socket, client_address = self.socket.accept()
                    logger.info(f"Client connection established: {client_address}")

                    # Criar thread para cada cliente
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address, message_callback),
                        daemon=True,
                    )
                    client_thread.start()

                except socket.error as e:
                    if self.running:
                        logger.error(f"Socket error: {e}")

        except Exception as e:
            logger.error(f"Failed to start server: {e}")
            raise e

    def handle_client(self, client_socket, client_address, message_callback):
        try:
            self.clients.append(client_socket)

            while self.running:
                try:
                    size_data = client_socket.recv(4)
                    if not size_data:
                        break

                    data_size = int.from_bytes(size_data, byteorder="big")

                    received_data = b""
                    while len(received_data) < data_size:
                        chunk = client_socket.recv(
                            min(data_size - len(received_data), 4096)
                        )
                        if not chunk:
                            break
                        received_data += chunk

                    # Deserializar os dados
                    data = pickle.loads(received_data)

                    logger.info(f"Received data from {client_address}: {data}")

                    # Chamar callback se fornecido
                    if message_callback:
                        message_callback(data)

                except socket.error as e:
                    logger.error(
                        f"Socket error while handling client {client_address}: {e}"
                    )
                    break

        except Exception as e:
            logger.error(f"Error handling client {client_address}: {e}")
        finally:
            client_socket.close()
            logger.info(f"Client {client_address} disconnected.")

    def stop(self):
        self.running = False

        for client in self.clients[:]:
            try:
                client.close()
            except Exception as e:
                logger.error(f"Error closing client connection: {e}")

        self.clients.clear()

        if self.socket:
            try:
                self.socket.close()
                logger.info("Server stopped successfully.")
            except Exception as e:
                logger.error(f"Error while stopping server: {e}")
            finally:
                self.socket = None

    def broadcast_message(self, data):
        disconnected_clients = []

        for client in self.clients:
            try:
                serialized_data = pickle.dumps(data)
                data_size = len(serialized_data)
                client.sendall(data_size.to_bytes(4, byteorder="big"))
                client.sendall(serialized_data)
            except Exception as e:
                logger.error(f"Error in broadcasting to client: {e}")
                disconnected_clients.append(client)

        for client in disconnected_clients:
            if client in self.clients:
                self.clients.remove(client)
                try:
                    client.close()
                except Exception as e:
                    logger.error(f"Error closing disconnected client: {e}")
