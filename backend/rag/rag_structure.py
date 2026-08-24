import uuid
from backend.utils.handling_json import json_dumps,json_loader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_chroma import Chroma

file_data = json_loader(directory_name="knowlegde_base",file_name="building-muscle.json")

def chunking(file_data):
    text_spliter = RecursiveCharacterTextSplitter(
    chunk_size = 800,
    chunk_overlap = 100,
    separators =[
        "\n\n", 
        "\n", 
        ". ",
        " ",
        ""
    ],
    length_function = len,
    is_separator_regex = False,
    )
    
    chapter_docs = []
    for chapter_index,entry in enumerate(file_data, start = 1):
        chapter_name = entry["chapter"]
        chapter_text = entry["text"]
        chapter_docs.append(
            Document(
                page_content = chapter_text,
                metadata = {
                    "chunk_id": f"chunk_{uuid.uuid4()}",
                    "chapter": chapter_name,
                    "chapter_index": chapter_index
                }
            )
        )
    chunks = text_spliter.split_documents(chapter_docs)
    chunks_count = {}
    for chunk in chunks:
        chapter_index = chunk.metadata["chapter_index"]
        chunk_index = chunks_count.get(chapter_index, 0)
        chunk.metadata["chunk_id"] = (
            f" chapter_{chapter_index}_chunk_{chunk_index}"
        )
        chunks_count[chapter_index] = chunk_index + 1
    return chunks
    
chunk = chunking(file_data = file_data)

embedding = HuggingFaceEmbeddings(
    model_name = "BAAI/bge-small-en-v1.5",
    encode_kwargs = {"normalize_embeddings": True}
)

vector_store = Chroma.from_documents(
    documents = chunk,
    embedding = embedding,
    persist_directory="./vector_DB",
    collection_name= "muscle_growth" 
)