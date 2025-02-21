import json
from bottle import request, abort
from geventwebsocket.exceptions import WebSocketError

class WebSocketController:
    def __init__(self):
        self.clients = []

    def add_client(self, client):
        self.clients.append(client)

    def remove_client(self, client):
        self.clients.remove(client)

    def add_connection(self, ws):
        """Adiciona uma nova conexão WebSocket."""
        self.connections.append(ws)

    def remove_connection(self, ws):
        """Remove uma conexão WebSocket."""
        if ws in self.connections:
            self.connections.remove(ws)

    def broadcast(self, message):
        """Envia uma mensagem para todas as conexões WebSocket ativas."""
        for ws in self.connections:
            try:
                ws.send(json.dumps(message))
            except Exception as e:
                print(f"Erro ao enviar mensagem via WebSocket: {e}")
                self.remove_connection(ws)

websocket_controller = WebSocketController()
