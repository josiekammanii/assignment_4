import os

relative_path = '../notes.jpg'

# Absolute path
absolute_path = os.path.abspath(relative_path)

print(f"Absolute Path: {absolute_path}")