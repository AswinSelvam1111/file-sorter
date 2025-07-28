import os
import tkinter as tk
import file_organizer
from dotenv import load_dotenv

def on_click_sort_by_file_type(root, entry1, entry2):
    raw_file_path = entry1.get()

    #include a check to ensure the raw_file_path is a folder
    destination_path = entry2.get()
    file_organizer.sort_all_by_file_type(raw_file_path, destination_path)
    email_gui(root)
    
def on_click_sort_by_date_created(root, entry1, entry2):
    raw_file_path = entry1.get()

    #include a check to ensure the raw_file_path is a folder
    destination_path = entry2.get()
    file_organizer.sort_all_by_datetime(raw_file_path, destination_path)
    email_gui(root)


def main_gui():
    root = tk.Tk()
    root.geometry("400x200")
    root.resizable(True, False)
    root.title("File Sorter")


    w = tk.Label(root, text='Welcome to File Sorter! \n\n Do you want it to be organised by file type or date created?')
    w.pack()

    tk.Label(root, text="Where do you want to get files from?").pack()
    entry1 = tk.Entry(root)
    entry1.pack()

    # Label and Entry for second input
    tk.Label(root, text="Where do you want the sorted files to go? (Make sure this location is a folder)").pack()
    entry2 = tk.Entry(root)
    entry2.pack()

    # Create buttons for sorting options
    clickbutton1 = tk.Button(root, text="By File Type", command=lambda: on_click_sort_by_file_type(root, entry1, entry2))
    clickbutton2 = tk.Button(root, text="Date Created", command=lambda: on_click_sort_by_date_created(root, entry1, entry2))
    clickbutton1.pack(side="left", padx=80), clickbutton2.pack(side="left")

    root.mainloop()

def email_gui(prev_root):
    prev_root.destroy()  # Close the main window if it exists

    load_dotenv()  # Load environment variables from .env file
    email_address = os.getenv("EMAIL_ADDRESS")

    root = tk.Tk()
    root.geometry("450x100")
    root.resizable(True, False)
    root.title("File Sorter")

    w = tk.Label(root, text=f'Do you want to email the most recent log file? \n\n Take note that the email address on the recieving end is: {email_address}')
    w.pack()

    button1 = tk.Button(root, text="Email Log File", command=lambda: [file_organizer.email_recent_file(), root.destroy()])
    button2 = tk.Button(root, text="Cancel", command=root.destroy)
    button1.pack(side="left", padx=80), button2.pack(side="left")

    root.mainloop()


if __name__ == "__main__":
    main_gui()