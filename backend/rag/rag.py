import os 
from google import genai
from dotenv import load_dotenv
from langchain_chroma import Chroma
from backend.rag.rag_structure import embedding

load_dotenv()

vector_store = Chroma(
    collection_name="muscle_growth",
    embedding_function=embedding,
    persist_directory="./chroma_vector_DB",
)

user_query = input("ask anything: ")

retriever = vector_store.as_retriever(
    search_type = "similarity",
    search_kwargs = {'k': 4}
)
docs = retriever.invoke(user_query)

context = "\n\n".join(
    doc.page_content for doc in docs
)

client = genai.Client(api_key = os.getenv("gen_ai_api_key"))
interaction = client.interactions.create(
    model = "gemini-3.5-flash",
    system_instruction = "You are the helpfull asstistant. answer ONLY using provided context, if the answer is not in a context say 'Sorry, I couldn't found the context in provide document. Please ask other question'",
    input = f"User query: {user_query} context: {context}"
)

print(interaction.output_text)