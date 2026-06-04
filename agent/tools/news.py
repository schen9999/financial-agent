import os
import requests
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()


@tool
def get_company_news(company_name: str) -> list:
    """
    Fetches the 5 most recent news articles about a company.
    Pass the full company name (e.g. 'Apple' not 'AAPL').
    Use this to get recent developments, sentiment, and events
    surrounding a company.
    """
    api_key = os.getenv("NEWS_API_KEY")

    if not api_key:
        return [{"error": "NEWS_API_KEY not found in environment variables"}]

    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": f'"{company_name}" stock OR earnings OR investor',
            "sortBy": "publishedAt",
            "pageSize": 5,
            "language": "en",
            "sources": "bloomberg,reuters,the-wall-street-journal,financial-times,fortune",
            "apiKey": api_key,
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        articles = []
        for article in data.get("articles", []):
            articles.append({
                "title": article.get("title", "N/A"),
                "source": article.get("source", {}).get("name", "N/A"),
                "published_at": article.get("publishedAt", "N/A"),
                "description": article.get("description", "N/A"),
                "url": article.get("url", "N/A"),
            })

        return articles if articles else [{"message": "No articles found"}]

    except Exception as e:
        return [{"error": f"Failed to fetch news for {company_name}: {str(e)}"}]