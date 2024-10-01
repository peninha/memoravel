import tiktoken
import json

class Memoravel:
    def __init__(self, limit=10, max_tokens=8000, preserve_initial_messages=0, preserve_system_messages=False):
        # Verifica se ambos os parâmetros são usados simultaneamente
        if preserve_initial_messages > 0 and preserve_system_messages:
            raise ValueError("Você não pode usar 'preserve_initial_messages' e 'preserve_system_messages' ao mesmo tempo.")

        self.limit = limit
        self.max_tokens = max_tokens
        self.preserve_initial_messages = preserve_initial_messages
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

        # Índice a partir do qual podemos remover mensagens
        removable_start_index = self.preserve_initial_messages

        while (self.max_tokens > 0 and total_tokens > self.max_tokens) or (self.limit > 0 and len(self.history) > self.limit):
            # Encontra o índice da primeira mensagem que pode ser removida
            for i in range(removable_start_index, len(self.history)):
                # Se preserve_system_messages estiver ativo, pular mensagens do sistema
                if self.preserve_system_messages and self.history[i]['role'] == 'system':
                    continue
                # Remova a mensagem encontrada que não seja do sistema
                self.history.pop(i)
                break
            total_tokens = self._count_tokens()

    def _count_tokens(self):
        # Otimização: Use try-except para evitar travamentos devido a entradas inesperadas
        try:
            return sum(len(self.encoder.encode(msg["content"])) for msg in self.history)
        except Exception as e:
            print(f"Erro ao contar tokens: {e}")
            return 0  # Retorna zero ou algum valor padrão em caso de erro

    def get_history(self):
        history_deserialized = []
        for msg in self.history:
            try:
                content = json.loads(msg["content"])
            except json.JSONDecodeError:
                content = msg["content"]
            history_deserialized.append({"role": msg["role"], "content": content})
        return history_deserialized
