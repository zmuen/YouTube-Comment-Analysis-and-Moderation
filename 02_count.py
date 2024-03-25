import json

data = []

# Open the file and read line by line
with open('comments.json', 'r') as file:
    content = file.read().strip().split('}\n{')

for line in content:
    if not line.endswith('}'):
        line += '}'
    if not line.startswith('{'):
        line = '{' + line

    try:
        # Load the JSON data from the line
        obj = json.loads(line)

        # Add the object to our data list
        data.append(obj)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON data from line: {line}. Error: {e}")

# Save the data to a new JSON file
with open('fixed_comments.json', 'w') as file:
    json.dump(data, file, indent=4)

with open("fixed_comments.json", "r") as file:
    # Read all the lines in the file
    lines = file.readlines()

# Count the number of lines
num_lines = len(lines)

# Print the result
print("Total number of comments:", num_lines)
