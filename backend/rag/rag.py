import os 
from groq import Groq
from dotenv import load_dotenv
from langchain_chroma import Chroma
from rag.rag_structure import embedding
from prompts.llm_prompt import prompt

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
    
def format_history(history):
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
        search_type = "mmr",
        search_kwargs = {
            'k': 4,
            "fetch_k":20
        }
    )
    docs = retriever.invoke(user_query)

    context = "\n\n".join(
        doc.page_content for doc in docs
    )
    return context

def generateResponse(user_query,context,conversation_history):
    client = Groq(
        api_key= os.getenv("GROQ_API_KEY")
    )
    completion = client.chat.completions.create(
        model = "openai/gpt-oss-120b",
        messages = [
            {
               "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": f"user_query: {user_query}, context: {context}, conversation history: {conversation_history}",
                
            }]
        )

    response = completion.choices[0].message.content
    return response