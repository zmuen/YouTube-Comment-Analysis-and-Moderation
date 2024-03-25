import sqlite3
import json

# Connect to the database
conn = sqlite3.connect('comments.db')
cursor = conn.cursor()

# Create the 'comments' table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY,
        comment_text TEXT,
        author TEXT,
        timestamp TEXT,
        positive BOOLEAN,
        negative BOOLEAN,
        angry BOOLEAN,
        spam BOOLEAN,
        response_required BOOLEAN
    )
''')

# Read the JSON file
with open('fixed_comments.json') as file:
    data = json.load(file)

# Insert each comment into the database
for comment in data:
    cursor.execute('''INSERT INTO comments (comment_text, author, timestamp, positive, negative, angry, spam, response_required)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                   (
                    comment['text'], 
                    comment['author'], 
                    comment['time'], 
                    0,
                    0, 
                    0, 
                    0, 
                    0
                    ))

# Commit the changes and close the connection
conn.commit()
conn.close()