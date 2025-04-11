class SharedState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SharedState, cls).__new__(cls)
            cls._instance.clients_connected = set()
            cls._instance.selected_file_path = None
        return cls._instance

    def set_selected_file_path(self, path: str):
        self.selected_file_path = path

    def get_selected_file_path(self) -> str:
        return self.selected_file_path

    def add_client(self, client):
        self.clients_connected.add(client)

    def remove_client(self, client):
        self.clients_connected.discard(client)

    def get_clients(self):
        return self.clients_connected
