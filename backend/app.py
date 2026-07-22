from fastapi import FastAPI
from pydantic import BaseModel
from rag.rag import retriever, generateResponse, make_history, format_history, history
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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
    final_response=generateResponse(userquery,context,conversation)
    make_history(userquery,final_response)
    print(final_response)
    
    return{
        "message_to_send": final_response
    }
    
    
    
