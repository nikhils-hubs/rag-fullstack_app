import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FILE_PATH = os.path.join(BASE_DIR,"documents","building-Muscle-Made-rag.pdf")

loader = PyMuPDFLoader(FILE_PATH)
document = loader.load()
document = document[:20]

text_spliters = RecursiveCharacterTextSplitter(
    separators= ["\n\n", "\n", " ", ""],
    chunk_size = 500,
    chunk_overlap = 50,
    length_function = len,
    is_separator_regex= False
)

chunks = text_spliters.split_documents(document)

embedding = HuggingFaceEmbeddings(
    model_name = "BAAI/bge-small-en-v1.5",
    encode_kwargs = {"normalize_embeddings": True}
)

vector_store = Chroma.from_documents(
    documents = chunks,
    embedding = embedding,
    persist_directory="./chroma_vector_DB",
    collection_name= "muscle_growth"
    
)