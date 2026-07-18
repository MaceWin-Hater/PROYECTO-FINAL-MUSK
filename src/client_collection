from src.client import Client
class ClientCollection:
    def __init__(self, clients):
        self.clients = clients

    def get_client_by_id(self, client_id):
        for client in self.clients:
            if client.client_id == client_id:
                return client
        return None
