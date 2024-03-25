from dotenv import load_dotenv
import openai

import os

api_key = os.getenv('API_KEY')

# Load environment variables from .env file
load_dotenv("openai.env")

# Get API key from environment variables
api_key = os.getenv('API_KEY')

# Set the API key
openai.api_key = api_key

# Define the prompt
message = [
    {
        'role': 'system',
        'content': 'You are a helpful assistant.'
    }, 
    {
        'role': 'user',
        'content': "How many states are there in the United States of America?"
    }
]

# Make a request to the OpenAI API
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=message
)

# Print the response
data = response['choices'][0].message.content.strip()

# Response as a JSON object
json_response = {
    "answer": data
}
# Print the JSON response
print(json_response)