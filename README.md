# FileSorter

**FileSorter** is a Python-based application that makes use of modules like os and tkinter to sort files from a specific folder you select, and segregate them based on either the date they were created, or the type of file. For myself as a developer, it is meant to be a quick and easy way to introduce myself to using tkinter as a frontend framework rather than Flask or Django. Working with os and smtplib means an understanding of file handling, which I believe is a core concept for bigger and more complex code dealt with in an industrial setting. 

## Features:

- Fetches the path of the folder with files to be sorted, as well as the destination path.
- A folder will be created in the destination path, depending on whether the user selected "By File Type" or "By Date"
- The user will also have an option to see the logs for each file by having it sent to their email address.

## Installation:

Take note that this project was developed and tested on **Python 3.13.3**.

Generally most libraries are built-in, such as os and tkinter. Run the below command in cmd/terminal:

```bash
pip install python-dotenv
```
