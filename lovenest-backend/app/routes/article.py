from pydantic import BaseModel
from fastapi import APIRouter
from datetime import datetime
from app.services.db import articles_collection

class GenerateArticleRequest(BaseModel):
    keyword: str
    length: str     # "short", "medium", "long"
    tone: str       # Expected values: "formal", "informal"
    language: str   # "english" only for now

router = APIRouter()

def generate_meta_title(keyword: str) -> str:
    # TODO: Replace this with real LLM API call (e.g., OpenAI, LLaMA, etc.)
    # For now, simulate a human-like title
    if len(keyword.split()) <= 4:
        return keyword.strip().capitalize()
    return f"A Guide to {keyword.strip().capitalize()}"

@router.post("/generate-article")
def generate_article(request: GenerateArticleRequest):
    # Step 1: Extract input
    keyword = request.keyword.strip()
    length = request.length.lower()
    tone = request.tone.lower()
    language = request.language.lower()

    # Step 2: Generate meta title using simulated LLM
    meta_title = generate_meta_title(keyword)

    # Step 3: Simulate article generation
    article = (
        f"This is a {tone} article in {language} about '{keyword}'. "
        f"The article is written with a {length} length format for demonstration purposes."
    )

    # Step 4: Create a document to store in MongoDB
    article_doc = {
        "username": "test_user",  # for now; will be replaced with token later
        "keyword": keyword,
        "meta_title": meta_title,
        "tone": tone,
        "length": length,
        "language": language,
        "article": article,
        "created_at": datetime.now()
    }

    # Step 5: Save to MongoDB
    articles_collection.insert_one(article_doc)

    # Step 6: Return result
    return {
        "message": "Article generated successfully",
        "meta_title": meta_title,
        "article": article
    }