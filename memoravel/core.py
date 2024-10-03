import tiktoken
import json

class Memoravel:
    def __init__(self, limit=10, max_tokens=8000, preserve_initial_memories=0, preserve_system_memories=True, preserve_last_memories=1):
        # Validações lógicas para evitar configurações inválidas
        if preserve_initial_memories > limit > 0:
            raise ValueError("O número de 'preserve_initial_memories' não pode ser maior que 'limit'.")
        if preserve_last_memories > limit > 0:
            raise ValueError("O número de 'preserve_last_memories' não pode ser maior que 'limit'.")
        
        self.limit = limit
        self.max_tokens = max_tokens
        self.preserve_initial_memories = preserve_initial_memories
        self.preserve_system_memories = preserve_system_memories
        self.preserve_last_memories = preserve_last_memories
        self.history = []
        self.encoder = tiktoken.get_encoding("cl100k_base")

    def add_memory(self, role, content):
        if isinstance(content, (dict, list)):
            content_serialized = json.dumps(content)
        else:
            content_serialized = content
        self.history.append({"role": role, "content": content_serialized})
        self._trim_history()

    def _trim_history(self):
        total_tokens = self._count_tokens()

        # Índice a partir do qual podemos remover mensagens
        removable_start_index = self.preserve_initial_memories

        # Calcula o índice até onde podemos remover (antes das últimas memórias que devem ser preservadas)
        removable_end_index = len(self.history) - self.preserve_last_memories

        # Verifica se o histórico pode ser ajustado (há mensagens que podem ser removidas)
        while (
            (self.max_tokens > 0 and total_tokens > self.max_tokens) or
            (self.limit > 0 and len(self.history) > self.limit)
        ) and self._has_removable_memory(removable_start_index, removable_end_index):
            # Encontra o índice da primeira mensagem que pode ser removida
            for i in range(removable_start_index, removable_end_index):
                # Se preserve_system_memories estiver ativo, pular mensagens do sistema
                if self.preserve_system_memories and self.history[i]["role"] == "system":
                    continue
                # Remove a primeira mensagem removível
                self.history.pop(i)
                break
            total_tokens = self._count_tokens()
            removable_end_index = len(self.history) - self.preserve_last_memories

    def _has_removable_memory(self, start_index, end_index):
        """Verifica se há mensagens removíveis entre um índice inicial e final."""
        return any(
            (msg["role"] != "system" or not self.preserve_system_memories)
            for msg in self.history[start_index:end_index]
        )

    def _count_tokens(self):
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
