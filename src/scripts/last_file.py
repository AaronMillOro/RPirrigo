import glob
import os
from dotenv import dotenv_values


config = dotenv_values(".env")

REPOSITORY = config["IMG_DIR"] + "*.jpg"
files_directory = glob.glob(REPOSITORY) 
latest_file = max(files_directory, key=os.path.getctime)
print(latest_file, type(latest_file))