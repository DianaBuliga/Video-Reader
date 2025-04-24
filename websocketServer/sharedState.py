class SharedState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SharedState, cls).__new__(cls)
            cls._instance.clients_connected = set()
            cls._instance.selected_file_path = None
            cls._instance.video_processing_active = False
            cls._instance.video_position = 0
        return cls._instance

    def set_selected_file_path(self, path):
        self.selected_file_path = path

    def get_selected_file_path(self):
        return self.selected_file_path

    def add_client(self, client):
        self.clients_connected.add(client)

    def remove_client(self, client):
        self.clients_connected.discard(client)

    def get_clients(self):
        return self.clients_connected

    def set_video_processing_active(self, value):
        print('video_active_changed', value)
        self.video_processing_active = value

    def get_video_processing_active(self):
        return self.video_processing_active

    def set_video_position(self, pos):
        self.video_position = pos

    def get_video_position(self):
        return self.video_position
