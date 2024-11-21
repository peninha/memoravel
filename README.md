# memoravel

A Python library to manage message history, for implementing memory in Language Models.

Uma biblioteca para gerenciar histórico de mensagens, para implementar memória nos Modelos de Linguagem.

## Features

- **Message History Management**: Store and manage message history to simulate memory in LLMs.
- **Token Counting**: Manage the number of tokens effectively to keep conversation context under a desired limit.
- **Flexible Memory Preservation**: Allows preserving initial or last messages, including system messages, ensuring critical information remains.

## Installation

To install memoravel, you can use pip:

```sh
pip install git+https://github.com/peninha/memoravel.git#egg=memoravel
```

## Quick Start

Here is a quick example to help you get started with `memoravel`:

```python
from memoravel import Memoravel

# Initialize with a message limit of 5
memory = Memoravel(limit=5)

# Add some messages
memory.add(role="user", content="Hello, how are you?")
memory.add(role="assistant", content="I'm fine, thank you! How can I assist you today?")

# Recall all messages
history = memory.recall()
print(history)

# Add more messages and see how the history is trimmed
memory.add(role="user", content="Tell me a joke.")
memory.add(role="assistant", content="Why don't skeletons fight each other? They don't have the guts.")

# Recall last 3 messages
recent_history = memory.recall(last_n=3)
print(recent_history)
```

This example demonstrates basic usage, including adding messages and recalling them, as well as automatically trimming the history when necessary.

## Usage

`memoravel` can be used in a variety of ways to maintain conversational context for language models. Below are some of the key methods available:

### `add(role, content=None, **kwargs)`
Add a message to the history. This method will automatically trim the history if it exceeds the set limits.

- **Parameters**:
  - `role` (str): The role of the message (`user`, `assistant`, `system`).
  - `content` (str, dict, list, optional): The content of the message.
  - `kwargs`: Additional metadata.

### `recall(last_n=None, first_n=None, slice_range=None)`
Retrieve messages from the history.

- **Parameters**:
  - `last_n` (int, optional): Retrieve the last `n` messages.
  - `first_n` (int, optional): Retrieve the first `n` messages.
  - `slice_range` (slice, optional): Retrieve messages using a slice.

### `save(file_path)` / `load(file_path)`
Save or load the history from a file.

## Examples

You can find more comprehensive examples in the [`examples/`](examples/) directory of the repository. These examples cover various scenarios such as:

- Basic usage for conversational context.
- Advanced token management.
- Preserving system messages and custom metadata.

## Documentation

Full documentation for all methods and classes can be found at the [official documentation site](#) (placeholder link for now). You can also refer to the docstrings in the code for quick explanations.

## Contributing

We welcome contributions! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

Please make sure to add or update tests as appropriate, and ensure the code follows PEP8 guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Feedback and Support

If you have questions, suggestions, or feedback, feel free to open an issue on GitHub. Contributions, feedback, and improvements are always welcome.

![GitHub Repo stars](https://img.shields.io/github/stars/peninha/memoravel?style=social)
![GitHub forks](https://img.shields.io/github/forks/peninha/memoravel?style=social)

