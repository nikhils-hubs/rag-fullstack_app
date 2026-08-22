import os 
import re
import json
from unstructured.partition.pdf import partition_pdf

# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# file_path = os.path.join(BASE_DIR,"assets","building-Muscle-Made-rag.pdf")
# output_path = os.path.join(BASE_DIR,"assets")

def cleaning_book(file_path,file_path_json):
    elements = partition_pdf(filename = file_path, strategy = "fast")
    
    KEEP = {"Title","NarrativeText","ListItem"}
    elements = [el for el in elements if el.category in KEEP and el.text.strip()]
    chapter_patterns = re.compile(r'^Chapter\s+\d+\s*:', re.IGNORECASE)
    chapters = []
    current_tittle = "chapter"
    current_text = []

    for el in elements:
        text = el.text.strip()
        if chapter_patterns.match(text):
            if current_text:
                chapters.append({
                    "chapter": current_tittle,
                    "text": " ".join(current_text)
                })
            current_tittle = text
            current_text = []
        else:
            current_text.append(text)
    if current_text:
        chapters.append({
            "chapter": text,
            "text": " ".join(current_text),
        })

    with open(file_path_json,"w",encoding="utf-8") as file:
        json.dump(chapters,file,indent=2,ensure_ascii=False)
    
    return f"Converted into json at {file_path_json}"