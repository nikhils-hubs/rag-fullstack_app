from fastapi import FastAPI
from pydantic import BaseModel
from rag.rag import retriever, generateResponse, make_history, format_history, history, imageGeneration
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/images",StaticFiles(directory="generated_image"),name="images")
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],
)


@app.get("/")
def fn():
    return {"message": "hello World"}


class chatRequest(BaseModel):
    message: str
    
@app.post("/chat")
def chat(request: chatRequest):
    userquery = request.message
    
    context = retriever(userquery)
    conversation = format_history(history)
    response=generateResponse(userquery,context,conversation)
    final_response = response['answer']
    image_path = None
    if response['generate_image']:
        image_prompt = response['image_prompt']
        image_path = imageGeneration(image_prompt)
    
    make_history(userquery,final_response)
    print(final_response)
    
    return{
        "message_to_send": final_response,
        "image_url": f"/images/{image_path}" if image_path else None
    }
    
    
    
