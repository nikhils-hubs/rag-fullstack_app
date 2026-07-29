import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FILE_PATH_bulding_muscle = os.path.join(BASE_DIR,"documents","building-Muscle-Made-rag.pdf")
FILE_PATH_science_based_lifting = os.path.join(BASE_DIR,"documents","Science-based-lifting-rag.pdf")

loader_1 = PyMuPDFLoader(FILE_PATH_bulding_muscle)
loader_2 = PyMuPDFLoader(FILE_PATH_science_based_lifting)
document_bulding_muscle = loader_1.load()
document_science_based_lifting = loader_2.load()

text_spliters = RecursiveCharacterTextSplitter(
    separators= ["\n\n", "\n", " ", ""],
    chunk_size = 500,
    chunk_overlap = 50,
    length_function = len,
    is_separator_regex= False
)

for doc in document_bulding_muscle:
    doc.metadata["book"] = "Building Muscle"

for doc in document_science_based_lifting:
    doc.metadata["book"] = "Science and Development of Muscle Hypertrophy"
    

chunks = text_spliters.split_documents(document_bulding_muscle)
chunks_2 = text_spliters.split_documents(document_science_based_lifting)

allchunks = chunks + chunks_2

embedding = HuggingFaceEmbeddings(
    model_name = "BAAI/bge-small-en-v1.5",
    encode_kwargs = {"normalize_embeddings": True}
)

vector_store = Chroma.from_documents(
    documents = allchunks,
    embedding = embedding,
    persist_directory="./chroma_vector_DB",
    collection_name= "muscle_growth"
    
)