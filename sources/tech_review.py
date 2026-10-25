"""
Source scraper for MIT Technology Review AI breakthrough analysis.
"""

from typing import List
import xml.etree.ElementTree as ET
import requests
import urllib3

from config import REQUEST_HEADERS, REQUEST_TIMEOUT
from models import AIResearchItem
from summarizer import summarize_ai_research

urllib3.disable_warnings()

MIT_FEED_URL = "https://www.technologyreview.com/topic/artificial-intelligence/feed/"


def fetch_tech_review_articles(limit: int = 2) -> List[AIResearchItem]:
    """Fetches top AI analysis and paradigm shifts from MIT Technology Review."""
    items: List[AIResearchItem] = []

    try:
        resp = requests.get(MIT_FEED_URL, headers=REQUEST_HEADERS, timeout=REQUEST_TIMEOUT)
        if resp.status_code != 200:
            return items

        root = ET.fromstring(resp.content)
        entries = root.findall(".//item")

        for item in entries[:limit]:
            title = item.find("title").text if item.find("title") is not None else ""
            link = item.find("link").text if item.find("link") is not None else ""
            desc = item.find("description").text if item.find("description") is not None else ""

            if not title or not link:
                continue

            crux, key_points, category = summarize_ai_research(title, desc or title)

            items.append(AIResearchItem(
                id=AIResearchItem.generate_id(title, link),
                title=title,
                source="MIT Technology Review",
                url=link,
                pdf_url=None,
                crux=crux,
                key_points=key_points,
                category=category,
                score=90
            ))

    except Exception as e:
        print(f"[Tech Review] Error: {e}")

    return items
