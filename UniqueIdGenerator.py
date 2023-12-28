import threading


class CommandIdGenerator:
    _lock = threading.Lock()
    current_id = 0

    @classmethod
    def generate_unique_command_id(cls):
        with cls._lock:
            cls.current_id += 1
            return cls.current_id

    @classmethod
    def reset(cls):
        with cls._lock:
            cls.current_id = 0
