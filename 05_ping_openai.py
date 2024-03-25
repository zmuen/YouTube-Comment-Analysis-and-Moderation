from dotenv import load_dotenv
import openai
import requests
import os

# Load API key from environment variables
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

# print(os.getenv('OPENAI_API_KEY')) ## Debugging information

# Assign the API key to openai
openai.api_key = api_key

# Setup the API URL
url = "https://api.openai.com/v1/completions"

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