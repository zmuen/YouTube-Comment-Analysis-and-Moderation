import subprocess
import sys

# install dependencies from a requirements.txt file
def install_requirements(requirements_path):
   subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])

# Example usage
requirements_path = './requirements.txt'
install_requirements(requirements_path)