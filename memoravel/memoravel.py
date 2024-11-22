import tiktoken
import json

# NOTE: This class currently only works with the OpenAI API format.
# TODO: Implement compatibility with other model APIs.
# TODO: Melhorar o exemplo do Quick Start
# TODO: Fazer exemplos para a pasta examples

class Memoravel:
    def __init__(self, limit=10, max_tokens=8000, preserve_initial_memories=0, preserve_system_memories=True, preserve_last_memories=1, model="gpt-4o"):
        """
        A class to manage conversation memory for Language Models, maintaining message history
        and managing tokens to simulate persistent memory.
    
        NOTE:
            This class currently only works with the OpenAI API format.
        
        .. todo::
            Implement compatibility with other model APIs.

        Args:
            limit (int, optional): The maximum number of messages allowed in the history. Default is 10. Set to 0 for unlimited.
            max_tokens (int, optional): The maximum number of tokens allowed in the history. Default is 8000.
            preserve_initial_memories (int, optional): Number of initial memories to preserve. These messages will not be removed during trimming. Default is 0.
            preserve_system_memories (bool, optional): If True, system messages will be preserved during trimming. Default is True.
            preserve_last_memories (int, optional): Number of recent messages to preserve during trimming. Default is 1.
            model (str, optional): The model for which the encoding will be used, for token counting purposes. Default is "gpt-4o".
        
        Example:
            .. code-block:: python
                
                from memoravel import Memoravel
                memory = Memoravel(limit=5, max_tokens=1000, preserve_initial_memories=2, model="gpt-4")
        
        """
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

    def _trim_history(self):
        
        total_tokens = self.count_tokens()

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
            total_tokens = self.count_tokens()
            removable_end_index = len(self.history) - self.preserve_last_memories

    def _has_removable_memory(self, start_index, end_index):
        
        return any(
            (msg["role"] != "system" or not self.preserve_system_memories)
            for msg in self.history[start_index:end_index]
        )

    def add(self, role, content=None, **kwargs):
        """
        Adds a new message to the history and trims the history if necessary.
        
        Args:
            role (str): The role of the message (e.g., 'user', 'assistant', 'system').
            content (str, dict, list, optional): The content of the message, can be a string, dict, or list.
            kwargs: Additional fields that should be added to the message.
        
        Example:
            .. code-block:: python
            
                from memoravel import Memoravel
                memory = Memoravel()
                memory.add("system", "You talk like a pirate, always")
                memory.add("user", "Hello!")
                memory.add("assistant", "Arrr! Greetings, landlubber!")
                memory.add("tool", "content", custom_field="this is a custom field content")
        
        """
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
        self._trim_history()  # Trim the history after adding a new message

    def count_tokens(self):
        """
        Counts the total number of tokens in the current history.
        
        Returns:
            int: The total token count.
        
        Example:
            .. code-block:: python
            
                from memoravel import Memoravel
                memory = Memoravel()
                memory.add(role="user", content="Hello!")
                memory.add(role="assistant", content="How can I help you?")
                total_tokens = memory.count_tokens()
        
        """
        try:
            return sum(len(self.encoder.encode(json.dumps(msg))) for msg in self.history)
        except Exception as e:
            print(f"Error counting tokens: {e}")
            return False

    def recall(self, last_n=None, first_n=None, index_or_slice=None):
        """
        Returns the last `last_n` memories, the first `first_n` memories, or a specific range of the history using slice.
        
        Args:
            last_n (int, optional): Number of last memories to be retrieved.
            first_n (int, optional): Number of first memories to be retrieved.
            slice_range (slice, optional): A slice object to define the range (start, stop, step).
        
        Returns:
            list: A list of retrieved memories.
        
        Note:
            Only one of the parameters 'last_n', 'first_n', or 'slice_range' can be used at a time.
        
        Example:
            .. code-block:: python
            
                from memoravel import Memoravel
                memory = Memoravel(limit=5)
                memory.add(role="user", content="Hello!")
                memory.add(role="assistant", content="Hi! How can I help?")
                
                # Get the last message
                last_message = memory.recall(last_n=1)
    
                # Get the first message
                first_message = memory.recall(first_n=1)
    
                # Get a slice of messages
                messages_slice = memory.recall(slice_range=slice(0, 2))
        
        """
        if sum(param is not None for param in [last_n, first_n, index_or_slice]) > 1:
            raise ValueError("Only one of the parameters 'last_n', 'first_n', or 'slice_range' can be used at a time.")
        
        if last_n is not None:
            result = self.history[-last_n:] if last_n <= len(self.history) else self.history
        elif first_n is not None:
            result = self.history[:first_n] if first_n <= len(self.history) else self.history
        elif index_or_slice is not None:
            if not isinstance(index_or_slice, (slice, int)):
                raise ValueError("The 'index_or_slice' parameter must be a slice or an integer.")
            result = self.history[index_or_slice]
            if isinstance(index_or_slice, int):
                result = [result]  # Ensure the result is always a list
        else:
            result = self.history
        
        return result
    
    def save(self, file_path):
       """
       Saves the memory content to a JSON file.

       Args:
           file_path (str): The path where the JSON file should be saved.
       
       Example:
           .. code-block:: python
           
               from memoravel import Memoravel
               memory = Memoravel()
               memory.add(role="user", content="Hello!")
               memory.save("memory.json")
               
       """
       try:
           with open(file_path, 'w', encoding='utf-8') as file:
               json.dump(self.history, file, ensure_ascii=False, indent=2)
       except Exception as e:
           print(f"Error saving file: {e}")

    def load(self, file_path):
       """
       Loads the memory content from a JSON file.

       Args:
           file_path (str): The path to the JSON file to load.
       
       Example:
           .. code-block:: python
           
               from memoravel import Memoravel
               memory = Memoravel()
               memory.load("memory.json")
               
       """
       try:
           with open(file_path, 'r', encoding='utf-8') as file:
               self.history = json.load(file)
       except Exception as e:
           print(f"Error loading file: {e}")

    def delete(self, index_or_slice):
        """
        Deletes one or more memories from the history using a slice or an index.

        Args:
            index_or_slice (slice or int): A slice object or an index to define the range or specific memory to delete.
        
        Example:
            .. code-block:: python
            
                from memoravel import Memoravel
                memory = Memoravel()
                memory.add("user", "Message 1")
                memory.add("user", "Message 2")
                memory.add("user", "Message 3")
                memory.add("user", "Message 4")
                
                # Delete the first two messages
                memory.delete(index_or_slice=slice(0, 2))
                
                # Delete a specific message by index
                memory.delete(index_or_slice=1)
                
        """
        
        if isinstance(index_or_slice, (slice, int)):
            del self.history[index_or_slice]
        else:
            raise ValueError("The 'slice_range' parameter must be a slice object or int.")

    def insert(self, index, messages):
        """
        Inserts one or more messages into a specific position in the history and trims if necessary.
        
        Args:
            index (int): The index at which to insert the new messages.
            messages (list or dict): A single message (as a dict) or a list of messages to insert.
        
        Example:
            .. code-block:: python
                
                from memoravel import Memoravel
                memory = Memoravel()
                memory.add("user", "Message 1")
                memory.add("user", "Message 3")
                
                # Insert a new message at index 1
                memory.insert(1, {"role": "assistant", "content": "Inserted message"})
                
                # Insert multiple messages at index 2
                memory.insert(2, [{"role": "user", "content": "Another message"}, {"role": "system", "content": "System message"}])
                
        """
        if isinstance(messages, dict):
            self.history.insert(index, messages)
        elif isinstance(messages, list):
            for i, message in enumerate(messages):
                self.history.insert(index + i, message)
        else:
            raise ValueError("The 'messages' parameter must be either a dict or a list of dicts.")
        
        # Trim the history after insertion
        self._trim_history()
