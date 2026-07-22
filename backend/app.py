from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def fn():
    return {"message": "hello World"}

