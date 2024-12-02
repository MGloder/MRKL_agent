from typing import Optional


class Target:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.storage = []

    def add_storage(self, data):
        self.storage.append(data)

    def get_storage(self) -> Optional[str]:
        return self.storage[-1] if self.storage else None
