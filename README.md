# memoravel

A Python library designed to manage and manipulate conversational history, enabling persistent memory capabilities in Language Models.

[![Documentation Status](https://readthedocs.org/projects/memoravel/badge/?version=latest)](https://memoravel.readthedocs.io/en/latest/?badge=latest)

[portuguese] Uma biblioteca Python projetada para gerenciar e manipular o histórico de conversas, habilitando capacidades de memória persistente em Modelos de Linguagem.

## Features

- **Advanced Message History Management**: Easily store, retrieve, and manage conversational history, enabling your Language Model to simulate memory and maintain context across multiple interactions.

- **Adaptive Token Counting and Management**: Automatically tracks the number of tokens in the message history, ensuring that conversations stay within the token limit of the language model.

- **Customizable Trimming Rules**: Define detailed trimming rules to manage which messages should be retained and which can be discarded as new messages are added. Set rules such as preserving system prompts, the initial prompts or keeping recent exchanges, allowing you to maintain a balance between keeping the most relevant context and staying within token limits.

- **Granular Memory Editing**: Insert or delete specific messages at any position in the memory. This feature allows for precise control over the conversation history, enabling you to modify, expand, or refine the context as needed, without affecting the overall flow of the memory.

- **Selective Recall of Messages**: Retrieve messages flexibly using various criteria: request the last `n` messages, the first `n` messages, or a specific range using Python-style slicing. This makes it easy to programmatically adjust the context you provide to the language model based on the current need.

- **Persistent Memory Capabilities**: Save and load memory to and from disk in JSON format, allowing for persistent conversation states across different sessions. This is particularly useful for long-running applications, where the conversation context needs to be preserved between interactions.

- **Easy Extensibility**: Built with flexibility in mind, making it easy to adapt for other language models, future extensions, or use as a memory manager for other modules.

## Installation

To install memoravel, you can use pip:

```sh
pip install memoravel
```

## Quick Start

Here is a quick example to help you get started with `memoravel`, including integration with OpenAI's API. We'll use a helper function to make requests and manage memory:

```python
from memoravel import Memoravel
from dotenv import load_dotenv
from openai import OpenAI

# Initialize OpenAI client
# Make sure there is a .env file with your API Token in it: OPENAI_API_KEY="..."
load_dotenv() 
client = OpenAI()

model = "gpt-4o"

# Initialize memory with a message limit of 5
memory = Memoravel(limit=5, max_tokens=8000, model=model)

def make_request(memory, model):
    try:
        # Make an API request using the current memory
        completion = client.chat.completions.create(
            model=model,
            messages=memory.recall()
        )
        # Get the response from the assistant
        response = completion.choices[0].message.content
        return response
    except Exception as e:
        print(f"Error during API request: {e}")
        return None

# Add a system message and some user interactions
memory.add(role="system", content="You are Gollum.")
memory.add(role="user", content="Hello.")
memory.add(role="assistant", content="Yesss, precious, hello... What does it wants, hmm?")

# Add a new user message
memory.add(role="user", content="Did you see Frodo?")

# Make the first API request
response = make_request(memory, model)
if response:
    print("Response from model:")
    print(response)
    # Add the response to memory
    memory.add(role="assistant", content=response)

# Add another user message
memory.add(role="user", content="Goodbye!")

# Make a second API request
response = make_request(memory, model)
if response:
    print("\nResponse from model:")
    print(response)
    # Add the response to memory
    memory.add(role="assistant", content=response)

# Recall the last two messages
last_two_messages = memory.recall(last_n=2)
print(f"\nLast two messages from the conversation:\n{last_two_messages}")

# Now, let's check the whole memory
print(f"\nFull memory after all interactions:\n{memory.recall()}")
# Because we limit the memory length to 5, there are only 5 messages stored, and the system prompt is preserved among them.

# Check the total number of tokens stored in memory
total_tokens = memory.count_tokens()
print(f"\nTokens in memory:\n{total_tokens}")
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

Full documentation for all methods and classes can be found at the [official documentation site](https://memoravel.readthedocs.io/en/latest/memoravel.html#memoravel.Memoravel). You can also refer to the docstrings in the code for quick explanations.

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



