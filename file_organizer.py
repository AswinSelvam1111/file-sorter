import os
import ctypes
import shutil
import calendar
import datetime
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


from win32com.client import Dispatch


file_name = ["Pictures", "Videos", "Documents", "Music", "Others"]
duplicate_path: int = 0

def create_directory(file_path, log_file):
    if not os.path.exists(file_path):
        os.makedirs(file_path)
        log_message(log_file, f"Created directory: {file_path} \n")
    else:
        log_message(log_file, f"{file_path} successfully found. \n")


def show_poup(message, title):
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x00000000 | 0x00003000 | 0x00001000)

def log_create(base_path):
    global log_file_path

    log_file_path = os.path.join(base_path, "logs")
    log_name = "logs_"+datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+".txt"
    log_file = os.path.join(log_file_path, log_name)
    if not os.path.exists(log_file_path):
        os.makedirs(log_file_path)
    return log_file

def log_message(log_file, message):
    with open(log_file, 'a') as f:
        f.write(message)


# Sort files by file type

def sort_file_by_file_type (file_path, filetype_destination_path, log_file):
    global duplicate_path
    file = os.path.basename(file_path)

    if os.path.isfile(file_path):
        #seperate file to get file type
        name, ext = os.path.splitext(file)
        ext = ext[1:].lower()  # Remove the dot and convert to lowercase
        log_message(log_file, f"Processing file: {file}\n")

        #each case of file type means a different folder
        match ext:
            case "jpg" | "png":
                destination_path = "Pictures"
            case "mp4" | "avi":
                destination_path = "Videos"    
            case "docx" | "pdf" | "txt":
                destination_path = "Documents"
            case "mp3":
                destination_path = "Music"
            case _:
                destination_path = "Others"
                log_message(log_file, f"File type .{ext} not recognised, moving to Others folder.\n")
        
        #create destination folder if it doesn't exist
        shortcut_path = os.path.join(filetype_destination_path, destination_path, f"{name}_{ext}.lnk")
        #os.makedirs(shortcut_path, exist_ok=True)
        if not os.path.exists(shortcut_path):     
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = file_path
            shortcut.WorkingDirectory = file_path.rsplit("\\", 1)[0]
            shortcut.IconLocation = file_path  # Optional: You can set a .ico file path instead
            os.makedirs(os.path.dirname(shortcut_path), exist_ok=True)
            shortcut.save()
            log_message(log_file, f"Created shortcut {file} in {destination_path}\n")
        else:
            log_message(log_file, f"Shortut file {file} already exists in {destination_path}.")
            duplicate_path += 1

def sort_all_by_file_type(raw_file_path, base_destination_path):
    global duplicate_path
    duplicate_path = 0 #just in case it was not reset
    filetype_destination_path = os.path.join(base_destination_path, "By File Type")
    file_name = ["Pictures", "Videos", "Documents", "Music", "Others"]

    log_file = log_create(base_destination_path)
    log_message(log_file, f"Log started at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    create_directory(filetype_destination_path, log_file)

    for file in file_name:
        destination_path = os.path.join(filetype_destination_path, file)
        log_message(log_file, f"Checking/Creating directory: {destination_path} \n")
        create_directory(destination_path, log_file)
        destination_path = os.path.dirname(destination_path)
    log_message(log_file, "All directories checked/created successfully. \n")

    try:
        sort_folders_by_file_type(raw_file_path, filetype_destination_path, log_file)
        log_message(log_file, "File sorting by type completed successfully.\n")
    except FileNotFoundError as e:
        show_poup(f"Error: {e}", "File Not Found")
    if duplicate_path > 0:
        show_poup(f"File sorting completed. {duplicate_path} duplicate files found.", "File Sorting Completed")

def sort_folders_by_file_type(file_path, filetype_destination_path, log_file):
    for file in os.listdir(file_path):
        extended_path = os.path.join(file_path, file)

        if os.path.isdir(extended_path) and not os.path.islink(extended_path):
            sort_folders_by_file_type(extended_path, filetype_destination_path, log_file)

        elif os.path.isfile(extended_path):
            sort_file_by_file_type(extended_path, filetype_destination_path, log_file)

        else:
            log_message(log_file, f"Skipping {extended_path}, not a file or directory.\n")


# Sort files by date created

def sort_file_by_datetime(file_path, datetime_destination_path, log_file):
    global duplicate_path
    file = os.path.basename(file_path)

    if os.path.isfile(file_path):
        #seperate file to get file type
        name, ext = os.path.splitext(file)
        ext = ext[1:].lower()  # Remove the dot and convert to lowercase
        log_message(log_file, f"Processing file: {file_path}\n")

        # Get creation timestamp
        time_created = os.path.getctime(file_path)
        time_created = datetime.datetime.fromtimestamp(time_created)

        time_created = time_created.strftime('%Y-%m')
        year_created, month_created = time_created.split('-')
        log_message(log_file, f"File was created in {year_created} and month {month_created} \n")

        if str(year_created) in os.listdir(datetime_destination_path):
            for month in os.listdir(os.path.join(datetime_destination_path, str(year_created))):
                log_message(log_file, f"Checking month: {month} \n")
                if str(month_created) in month:
                    shortcut_path = os.path.join(datetime_destination_path, str(year_created), str(month), f"{name}_{ext}.lnk")
                    log_message(log_file, f"Creating shortcut at {shortcut_path} \n")
                    if not os.path.exists(shortcut_path):
                        # Create the shortcut
                        shell = Dispatch('WScript.Shell')
                        shortcut = shell.CreateShortCut(shortcut_path)
                        shortcut.Targetpath = file_path
                        shortcut.WorkingDirectory = file_path.rsplit("\\", 1)[0]
                        shortcut.IconLocation = file_path 
                        os.makedirs(os.path.dirname(shortcut_path), exist_ok=True)
                        shortcut.save()
                        log_message(log_file, f"Shortcut created for {file} in {year_created}/{month} \n")
                        break
                    else:
                        log_message(log_file, f"Shortcut file {file} already exists in {year_created}/{month_created}.")
                        duplicate_path += 1


def sort_all_by_datetime(raw_file_path, base_destination_path):
    global duplicate_path

    duplicate_path = 0 #just in case it was not reset
    datetime_destination_path = os.path.join(base_destination_path, "By Date")

    log_file = log_create(base_destination_path)
    log_message(log_file, f"Log started at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    create_directory(datetime_destination_path, log_file)

    months = list(calendar.month_name)[1:]  # Exclude the empty string at index 0
    years = list(range(2020, 2026))  # years from 2020 to 2025'

    create_directory(os.path.join(datetime_destination_path, "Older"), log_file)

    for year in years:
        datetime_destination_path = os.path.join(rf"{datetime_destination_path}", f"{year}")
        create_directory(datetime_destination_path, log_file)
        month_counter: int = 0
        for month in months:
            month_counter += 1
            datetime_destination_path = os.path.join(rf"{datetime_destination_path}", f"{month_counter:02d}_{month}")
            create_directory(datetime_destination_path, log_file)
            datetime_destination_path = os.path.dirname(datetime_destination_path) #  to go back to the year directory
        datetime_destination_path = os.path.dirname(datetime_destination_path) # to go back to the main datetime directory
    log_message(log_file, "All directories checked/created successfully.")

    try:
        sort_folders_by_datetime(raw_file_path, datetime_destination_path, log_file)
        log_message(log_file, "File sorting by datetime completed successfully.\n")
    except FileNotFoundError as e:
        show_poup(f"Error: {e}", "File Not Found")
    if duplicate_path > 0:
        show_poup(f"File sorting completed. {duplicate_path} duplicate files found.", "File Sorting Completed")

def sort_folders_by_datetime(file_path, datetime_destination_path, log_file):
    log_message(log_file, f"Sorting folders in: {file_path}\n")
    for file in os.listdir(file_path):
        extended_path = os.path.join(file_path, file)

        if os.path.isdir(extended_path) and not os.path.islink(extended_path):
            sort_folders_by_datetime(extended_path, datetime_destination_path, log_file)

        elif os.path.isfile(extended_path):
            log_message(log_file, f"Sorting file: {extended_path}\n")
            sort_file_by_datetime(extended_path, datetime_destination_path, log_file)

        else:
            log_message(log_file, f"Skipping {extended_path}, not a file or directory.\n")

def recent_file(folder_path):
    files = sorted([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
    if not files:
        return None
    return os.path.join(folder_path, files[-1])


# Email the most recent log file

def email_recent_file():
    logFile = recent_file(log_file_path)  
    if not logFile:
        show_poup("No files found in the directory.", "No files found")  # Make sure showPopup is defined
        return

    load_dotenv()  # Load environment variables from .env file

    senderEmail = os.getenv("EMAIL_ADDRESS")
    receiverEmail = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")  # Use environment variable in production

    msg = MIMEMultipart()
    msg['From'] = senderEmail
    msg['To'] = receiverEmail
    msg['Subject'] = "Recent Log File"
    msg.attach(MIMEText(f"Please find the attached log file: {logFile}", 'plain'))

    with open(logFile, 'rb') as f:
        part = MIMEApplication(f.read(), Name=os.path.basename(logFile))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(logFile)}"'
        msg.attach(part)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(senderEmail, password)
            server.send_message(msg)
        show_poup("Email sent successfully!", "Email Sent")
    except Exception as e:
        show_poup(f"Failed to send email: {str(e)}", "Email Error")

#Duplicate file handlers - done
#Logging each relocation and storing in log file - done
#Create shortcuts for each file in the destination folder - done
#Do the same for the folder sorted by dates - done
#add GUI functionality - done
#solve for testcases where file inside a subfolder - done
#If cannot find the directory corresponding the date, add to Older folder - done
#Add email functionality to send the log file - done


# fix the issues with datetime sorting (mainly the parameters in the functions) - ongoing


# allow the script to save the last entered base path and use it as the default next time - pending