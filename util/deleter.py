import shutil

try:
    shutil.rmtree("C:/Users/aswin/OneDrive/Desktop/Projects/FileSorter/rawfolder")
    print("Test folder deleted successfully.")
except:
    print("Failed to delete the test folder. It may not exist or is currently in use.")
    