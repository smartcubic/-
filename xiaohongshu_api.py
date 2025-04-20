from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import uvicorn
from xiaohongshu_scraper import scrape_xiaohongshu, extract_url_from_share_text
from typing import List, Optional

# Create FastAPI app
app = FastAPI(
    title="Xiaohongshu Scraper API",
    description="API for scraping content from Xiaohongshu posts",
    version="1.0.0"
)

# Define response model
class MediaResponse(BaseModel):
    title: str
    content: str
    media_type: str
    media_urls: List[str]

# Define request model
class ScrapeRequest(BaseModel):
    url: str

@app.get("/")
async def root():
    """
    Root endpoint that returns API information
    """
    return {
        "name": "Xiaohongshu Scraper API",
        "version": "1.0.0",
        "endpoints": [
            {"path": "/", "method": "GET", "description": "API information"},
            {"path": "/scrape", "method": "POST", "description": "Scrape content from a Xiaohongshu URL"}
        ]
    }

@app.post("/scrape", response_model=MediaResponse)
async def scrape_content(request: ScrapeRequest):
    """
    Scrape content from a Xiaohongshu URL
    
    - **url**: The URL of the Xiaohongshu post or mobile share text
    """
    # Check if the input is a mobile share text
    if "小红书" in request.url and "http" in request.url:
        url = extract_url_from_share_text(request.url)
        if not url:
            raise HTTPException(status_code=400, detail="Could not extract URL from the share text")
    else:
        url = request.url
    
    # Scrape the content
    result = scrape_xiaohongshu(url)
    
    if not result:
        raise HTTPException(status_code=500, detail="Failed to scrape content from the URL")
    
    return result

if __name__ == "__main__":
    uvicorn.run("xiaohongshu_api:app", host="0.0.0.0", port=8000, reload=True) 