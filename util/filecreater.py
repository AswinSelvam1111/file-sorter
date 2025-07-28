import os

file_name = ["Pictures", "Videos", "Documents", "Music", "Others"]
file_types = [".txt", ".jpg", ".png", ".mp4", ".avi", ".docx", ".pdf", ".mp3"]

def create_directory(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)
        print(f"Created directory: {file_path}")
    else:
        print(f"{file_path} successfully found.")

file_path = "C:/Users/aswin/OneDrive/Desktop/Projects/FileSorter/rawfolder"
create_directory(file_path)

for filetype in file_types:
    file = os.path.join(file_path, "test2" + filetype)
    with open(file, 'w') as f:
        f.write("This is a test file.")
