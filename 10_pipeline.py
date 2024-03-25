import subprocess

# Function to execute a subprocess command and check for errors
def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing {' '.join(command)}: {e}")
        exit(1)

# Run setup_requirements.py
run_command(["python", "setup_requirements.py"])

# Run YouTube Comment Downloader
extract_command = [youtube-comment-downloader --youtubeid L_Guz73e6fw --output comments.json]

# Run the extract command
run_command(extract_command)

# List of other script files in the correct order
scripts_files = [
    "02_count.py",
    "03_database.py",
    "05_ping_openai.py",
    "06_prediction.py",
    "07_create_responses.py",
    "08_categories.py",
    "09_visualization.py",
    "11_report.py",
]

# Execute each of the other scripts in order
for script in scripts_files:
    if script.endswith(".py"):
        run_command(["python", script])
