from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def root():
    return {"message":"Hello World Gogi Singh"}

@app.get("/posts")
def get_posts():
    return {"data" : "This is your post"}

@app.post("/createpost")
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"new post": f"title {payload['title']} content {payload['body']}"}