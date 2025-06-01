from fastapi import FastAPI
from app.services import db # triggers MongoDB setup

from app.routes import auth, article

app = FastAPI()

@app.get("/")
def root():
    return {"Message" : "loveNest API is running!"}

app.include_router(auth.router)
app.include_router(article.router)