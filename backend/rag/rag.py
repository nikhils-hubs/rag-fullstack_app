import os 
from google import genai
from dotenv import load_dotenv
from langchain_chroma import Chroma
from rag_structure import embedding

load_dotenv()

vector_store = Chroma(
    collection_name="muscle_growth",
    embedding_function=embedding,
    persist_directory="./chroma_vector_DB",
)

history = []
def make_history(user_query,LLm_reponse):
    MAX_LIMIT = 15
    history.append(
        {
            "role": "user",
            "content": user_query,
        }
    )
    history.append(
        {
            "role" : "ai",
            "content": LLm_reponse
        }
    )
    if len(history) > MAX_LIMIT: 
        del history[:2]
    
def format_history():
    conversation = ""
    for message in history:
        role = message['role']
        content = message['content']

        if role == "user":
            
            conversation += f"User: {message['content']}"
        else: 
            conversation += f"Ai: {message['content']}"
    
    
def retriever(user_query):
    retriever = vector_store.as_retriever(
        search_type = "similarity",
        search_kwargs = {'k': 4}
    )
    docs = retriever.invoke(user_query)

    context = "\n\n".join(
        doc.page_content for doc in docs
    )
    return context

def generateResponse(user_query,context,conversation_history):
    client = genai.Client(api_key = os.getenv("gen_ai_api_key"))
    interaction = client.interactions.create(
        model = "gemini-3.5-flash",
        system_instruction = "You are the helpfull asstistant. answer ONLY using provided context, if the answer is not in a context say 'Sorry, I couldn't found the context in provide document. Please ask other question'",
        input = f"User query: {user_query} context: {context} conversation_history: {conversation_history}"
    )

    response = interaction.output_text
    return response