import os 
import json
from pathlib import Path
import uuid
from huggingface_hub import InferenceClient
from groq import Groq
from dotenv import load_dotenv
from langchain_chroma import Chroma
from rag.rag_structure import embedding
from prompts.llm_prompt import prompt,query_expander_prompt

load_dotenv()
client = Groq(
        api_key= os.getenv("GROQ_API_KEY")
)

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
    
    
def queryExpander(user_query):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": query_expander_prompt,
            },
            {
                "role": "user",
                "content": user_query,
            }
        ],
        model = "llama-3.3-70b-versatile"
    )
    response = chat_completion.choices[0].message.content
    queries = []
    for query in response.split("\n"):
        query = query.strip()
        if query != "":
            queries.append(query)
    return queries
    
    
def retriever(queries):
    retriever = vector_store.as_retriever(
        search_type = "mmr",
        search_kwargs = {
            'k': 15,
            "fetch_k": 20,
        }
    )
    context = []
    for query in queries:
        retrived_info = retriever.invoke(query)
        if retrived_info :    # this checks wheater list is comming from invoke is empty or not if it is empty than it will become false and if !empty than it will become true this doing len(retrived_info) > 0 
            context.extend(retrived_info)
    full_context = "\n\n".join(
        doc.page_content for doc in context
    )
    return full_context

def generateResponse(user_query,context,conversation_history):
    chat_completion = client.chat.completions.create(
    messages = [
        {
           "role": "system",
            "content": prompt
        },
        {
            "role": "user",
            "content": f"user_query: {user_query}, context: {context}, conversation history: {conversation_history}",
    
        }],
    model= "llama-3.3-70b-versatile"
    )

    response = chat_completion.choices[0].message.content
    return json.loads(response)

def imageGeneration(image_prompt):
    client = InferenceClient(
        api_key= os.getenv("HF_TOKEN")
    )
    image = client.text_to_image(
        prompt=image_prompt,
        model="black-forest-labs/FLUX.1-schnell"
    )
    file_name = f"{uuid.uuid4()}.png"
    save_dir = Path("generated_image")
    image_path = save_dir/file_name
    image.save(image_path)
    return file_name

def main():
    while True:
        user_query = input("ask anything about SBL: ")
        if user_query == "exit":
            break
        queries = queryExpander(user_query)
        print(queries)
        context = retriever(queries)
        print(context)
        conversation_history = format_history(history)
        print(history)
        print(conversation_history)
        llm_response = generateResponse(user_query,context,conversation_history)
        print(llm_response)
        make_history(user_query,llm_response)
        

if __name__ == "__main__":
    main()
