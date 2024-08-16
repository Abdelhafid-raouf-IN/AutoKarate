import os

def create_directory(directory):
    os.makedirs(directory, exist_ok=True)

def write_to_file(filename, content):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        f.write(content)
