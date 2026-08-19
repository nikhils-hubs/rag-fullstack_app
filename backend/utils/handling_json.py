import json
from backend.utils.DIR import DIR

def json_loader(directory_name,file_name):
    final_file_path = DIR(directory_name,file_name)
    with open(final_file_path,"r",encoding="utf-8") as file:
        file_data = json.load(file)
    return file_data

def json_dumps(directory_name,file_name,data):
    final_file_path = DIR(directory_name,file_name)
    with open(final_file_path,"w",encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    
    