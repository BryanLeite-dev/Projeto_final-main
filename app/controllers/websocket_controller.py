import json
from bottle import request, abort
from geventwebsocket.exceptions import WebSocketError

class WebSocketController:
    def __init__(self):
        self.clients = []

    def add_client(self, client):
        """Adiciona um novo cliente WebSocket."""
        self.clients.append(client)

    def remove_client(self, client):
        """Remove um cliente WebSocket."""
        if client in self.clients:
            self.clients.remove(client)

    def broadcast(self, message):
        """Envia uma mensagem para todos os clientes conectados."""
        for client in self.clients:
            try:
                client.send(json.dumps(message))
            except Exception as e:
                print(f"Erro ao enviar mensagem via WebSocket: {e}")
                self.remove_client(client)


# Instância global do WebSocketController
websocket_controller = WebSocketController()