from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.services.db import articles_collection
from bson.objectid import ObjectId

from app.utils.auth_handler import get_current_user 

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

@router.get("/article-history")
def article_history():
    username = "test_user"      # For now, hardcoded user

    # Query last 5 articles (newest first)
    articles = (
        articles_collection.find({"username": username})
        .sort("created_at", -1)
        .limit(5)
    )

    result = []
    for index, article in enumerate(articles, start = 1):
        result.append({
            "serial_number": index,
            "id": str(article["_id"]),
            "meta_title": article.get("meta_title", ""),
            "created_at": article.get("created_at")
        })
    
    return result

@router.get("/view/{article_id}")
def view_article(article_id: str):
    article = articles_collection.find_one({"_id": ObjectId(article_id)})

    if not article:
        raise HTTPException(status_code = 404, detail = "Article not found")
    
    return {
        "meta_title": article["meta_title"],
        "keyword": article["keyword"],
        "article": article["article"],
        "created_at": article["created_at"]
    }

@router.get("/download/{article_id}")
def download_article(article_id: str):
    article = articles_collection.find_one({"_id": ObjectId(article_id)})

    if not article:
        raise HTTPException(status_code = 404, detail = "Article not found")
    
    return {
        "filename": f"{article["meta_title"].replace(' ', '_')}.txt",
        "content": article["article"]
    }

@router.delete("/delete/{article_id}")
def delete_article(article_id: str):
    result = articles_collection.delete_one({"_id": ObjectId(article_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Article not found or already deleted")
    
    return { "Message": "Article deleted successfully"}
