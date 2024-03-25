import sqlite3
import json

# Connect to the database
conn = sqlite3.connect('comments.db')
cursor = conn.cursor()

# Fetch the first 1000 comments
cursor.execute('SELECT * FROM comments LIMIT 1000')
comments = cursor.fetchall()

# Close the database connection
conn.close()

# Convert comments to JSON format
json_data = json.dumps(comments)

# Write JSON data to clean_dataset.json
with open('clean_dataset.json', 'w') as file:
    file.write(json_data)