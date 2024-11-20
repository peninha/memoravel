import tiktoken
import json

class Memoravel:
    def __init__(self, limit=10, max_tokens=8000, preserve_initial_memories=0, preserve_system_memories=True, preserve_last_memories=1, model="gpt-4o"):
        # Logical validations to avoid invalid configurations
        if preserve_initial_memories > limit > 0:
            raise ValueError("The number of 'preserve_initial_memories' cannot be greater than 'limit'.")
        if preserve_last_memories > limit > 0:
            raise ValueError("The number of 'preserve_last_memories' cannot be greater than 'limit'.")
        
        self.limit = limit
        self.max_tokens = max_tokens
        self.preserve_initial_memories = preserve_initial_memories
        self.preserve_system_memories = preserve_system_memories
        self.preserve_last_memories = preserve_last_memories
        self.history = []
        self.encoder = tiktoken.encoding_for_model(model)

    def add(self, role, content=None, **kwargs):
        # Building the message structure
        message = {"role": role}
        
        # Adding content if available
        if content is not None:
            if isinstance(content, (dict, list)):
                message["content"] = json.dumps(content)
            else:
                message["content"] = content
        
        # Adding additional fields, such as tool_calls or tool_call_id
        for key, value in kwargs.items():
            message[key] = value
        
        self.history.append(message)
        self._trim_history()

    def _trim_history(self):
        total_tokens = self._count_tokens()

        # Index from which we can remove messages
        removable_start_index = self.preserve_initial_memories

        # Calculate the index up to which we can remove (before the last memories that must be preserved)
        removable_end_index = len(self.history) - self.preserve_last_memories

        # Check if the history can be adjusted (if there are messages that can be removed)
        while (
            (self.max_tokens > 0 and total_tokens > self.max_tokens) or
            (self.limit > 0 and len(self.history) > self.limit)
        ) and self._has_removable_memory(removable_start_index, removable_end_index):
            # Find the index of the first removable message
            for i in range(removable_start_index, removable_end_index):
                # If preserve_system_memories is active, skip system messages
                if self.preserve_system_memories and self.history[i]["role"] == "system":
                    continue
                # Remove the first removable message
                self.history.pop(i)
                break
            total_tokens = self._count_tokens()
            removable_end_index = len(self.history) - self.preserve_last_memories

    def _has_removable_memory(self, start_index, end_index):
        """Checks if there are removable messages between a start and end index."""
        return any(
            (msg["role"] != "system" or not self.preserve_system_memories)
            for msg in self.history[start_index:end_index]
        )

    def _count_tokens(self):
        try:
            return sum(len(self.encoder.encode(json.dumps(msg))) for msg in self.history)
        except Exception as e:
            print(f"Error counting tokens: {e}")
            return 0  # Return zero or some default value in case of an error

    def recall(self, last_n=None, first_n=None, slice_range=None):
        """
        Returns the last 'last_n' memories, the first 'first_n' memories, or a specific range of the history using slice.
        
        :param last_n: number of last memories to be retrieved.
        :param first_n: number of first memories to be retrieved.
        :param slice_range: a slice object to define the range (start, stop, step).
        :return: A list of retrieved memories.
        """
        if sum(param is not None for param in [last_n, first_n, slice_range]) > 1:
            raise ValueError("Only one of the parameters 'last_n', 'first_n', or 'slice_range' can be used at a time.")
        
        if last_n is not None:
            result = self.history[-last_n:] if last_n <= len(self.history) else self.history
        elif first_n is not None:
            result = self.history[:first_n] if first_n <= len(self.history) else self.history
        elif slice_range is not None:
            if not isinstance(slice_range, slice):
                raise ValueError("The 'slice_range' parameter must be a slice object.")
            result = self.history[slice_range]
        else:
            result = self.history
        
        return result
    
    def save(self, file_path):
       """Saves the memory content to a JSON file."""
       try:
           with open(file_path, 'w', encoding='utf-8') as file:
               json.dump(self.history, file, ensure_ascii=False, indent=2)
       except Exception as e:
           print(f"Error saving file: {e}")

    def load(self, file_path):
       """Loads the memory content from a JSON file."""
       try:
           with open(file_path, 'r', encoding='utf-8') as file:
               self.history = json.load(file)
       except Exception as e:
           print(f"Error loading file: {e}")
