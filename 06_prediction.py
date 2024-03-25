import os
import json
import sqlite3
import openai
from dotenv import load_dotenv
import time
import re

# Load environment variables
load_dotenv("openai.env")

# Get API key
api_key = os.getenv('API_KEY')
openai.api_key = api_key

# Connect to SQLite database
conn = sqlite3.connect('comments.db')
cursor = conn.cursor()

# Fetch the first 1000 comments
cursor.execute("SELECT * FROM comments LIMIT 1000")
comments = cursor.fetchall()

# Define the prompt for classification
prompt = """
Task: Classify YouTube comments from "Sam Altman: OpenAI CEO on GPT-4, ChatGPT, and the Future of AI | Lex Fridman Podcast" into categories: positive, negative, angry, spam, and response_required. Use underlying sentiment or intent for classification, even if wording varies from examples.

Categories:
positive: Expressing satisfaction, appreciation or approval. Similar to "Thank you", "Excellent conversation!".
negative: Showing disappointment or disapproval, not anger. Example: "I'm disappointed with the conversation."
angry: Conveying frustration or anger. E.g., "This is unacceptable!" or "This guy is ruining people's lives."
spam: Promotional, irrelevant, or nonsensical. Like "Check out this link for amazing deals!"
response_Required: Comments that: 1. Directly ask a question (look for question marks and typical question words: Who, What, Where, When, Why, How). 2. Imply a question or request for information, even if not phrased as a direct question (like "could you please...?" or "I'm puzzled about...").

Output Format:
Classify each comment in the following JSON format:
{
  "positive": true/false,
  "negative": true/false,
  "angry": true/false,
  "spam": true/false,
  "response_required": true/false
}

Guidance: Prioritize sentiment recognition over exact phrasing. Comments similar in sentiment to provided examples, even if worded differently, should be categorized accordingly.
""" 

# Split comments into manageable chunks
chunks = [comments[i:i + 25] for i in range(0, len(comments), 25)]

try:
    for index, chunk in enumerate(chunks):
        messages = [{'role': 'system', 'content': prompt}]
        for comment in chunk:
            messages.append({'role': 'user', 'content': comment[1]})

        # Make the API call
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        time.sleep(10) 

        print(f"Processing chunk {index + 1}/{len(chunks)}")  # Debugging information

        # Extract the response content
        content = response.choices[0].message['content']
    
        # Parse JSON directly from the response content
        matches = re.findall(r'{[^{}]*}', content)
        # print(f"Content: {content}") # Debugging information
        # print(f"Matches: {matches}")
        for comment, match in zip(chunk, matches):
            try:
                result_dict = json.loads(match)
                # Extract the values and convert them to integers
                positive = int(result_dict.get('positive', False))
                negative = int(result_dict.get('negative', False))
                angry = int(result_dict.get('angry', False))
                spam = int(result_dict.get('spam', False))
                response_required = int(result_dict.get('response_required', False))

                # Update the database
                cursor.execute("""
                    UPDATE comments
                    SET positive = ?, negative = ?, angry = ?, spam = ?, response_required = ?
                    WHERE id = ?
                """, (positive, negative, angry, spam, response_required, comment[0]))
                conn.commit()  # Commit changes after updating each comment
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")

        print(f"Chunk {index + 1} processed and database updated accordingly.")

    # Commit changes after processing all chunks
    conn.commit()

except Exception as e:
    conn.rollback()
    print(f"An unexpected error occurred: {e}")
finally:
    conn.close()