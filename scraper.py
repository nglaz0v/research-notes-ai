import requests
from bs4 import BeautifulSoup


def fetch_article_from_url(url: str) -> str:
    """Fetch and extract main text content from a web article URL.

    Uses requests + beautifulsoup4 + html5lib for parsing.
    Strips navigation, scripts, styles and keeps only readable text.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; AI-Article-Summarizer/1.0)"
    }
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html5lib")

    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    selectors = ["article", "main", "#content", ".content", ".article-body", "body"]
    for selector in selectors:
        element = soup.select_one(selector)
        if element:
            return element.get_text(separator="\n", strip=True)

    return soup.get_text(separator="\n", strip=True)


def load_article_from_file(filepath: str) -> str:
    """Load article text from a local .txt file."""
    with open(filepath, encoding="utf-8") as f:
        return f.read().strip()
