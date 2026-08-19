import os 

def DIR(directory_name,file_name):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(BASE_DIR,directory_name,file_name)
    return file_path