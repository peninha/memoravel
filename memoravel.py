import tiktoken
import json

class Memoravel:
    def __init__(self, limit=10, max_tokens=8000, preserve_system_messages=1):
        self.limit = limit
        self.max_tokens = max_tokens
        self.preserve_system_messages = preserve_system_messages
        self.history = []
        self.encoder = tiktoken.get_encoding("cl100k_base")

    def add_message(self, role, content):
        if isinstance(content, (dict, list)):
            content_serialized = json.dumps(content)
        else:
            content_serialized = content
        self.history.append({"role": role, "content": content_serialized})
        self._trim_history()

    def _trim_history(self):
        total_tokens = self._count_tokens()
        removable_start_index = self.preserve_system_messages

        while (total_tokens > self.max_tokens or len(self.history) > self.limit) and len(self.history) > self.preserve_system_messages:
            self.history.pop(removable_start_index)
            total_tokens = self._count_tokens()

    def _count_tokens(self):
        return sum(len(self.encoder.encode(msg["content"])) for msg in self.history)

    def get_history(self):
        history_deserialized = []
        for msg in self.history:
            try:
                content = json.loads(msg["content"])
            except json.JSONDecodeError:
                content = msg["content"]
            history_deserialized.append({"role": msg["role"], "content": content})
        return history_deserialized