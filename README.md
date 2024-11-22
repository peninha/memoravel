# memoravel

A Python library to manage message history, for implementing memory in Language Models.

[portuguese] Uma biblioteca para gerenciar histórico de mensagens, para implementar memória nos Modelos de Linguagem.

## Features

- **Message History Management**: Store and manage message history to simulate memory in LLMs.
- **Token Counting**: Manage the number of tokens effectively to keep conversation context under a desired limit.
- **Flexible Memory Preservation**: Allows preserving initial or last messages, including system messages, ensuring critical information remains.

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
memory.add(role="system", content="You are a helpful assistant.")
memory.add(role="user", content="Write a haiku about recursion in programming.")
memory.add(role="assistant", content="A function returns,\nIt calls itself once again,\nInfinite beauty.")

# Add a new user message
memory.add(role="user", content="Can you explain what recursion is in two sentences?")

# Make the first API request
response = make_request(memory, model)
if response:
    print("Response from model:")
    print(response)
    # Add the response to memory
    memory.add(role="assistant", content=response)

# Add another user message
memory.add(role="user", content="What is the most common application of recursion? Summarize it in two sentences.")

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



