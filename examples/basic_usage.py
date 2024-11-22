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