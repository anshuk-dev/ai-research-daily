"""
Source scraper for official research updates from Google DeepMind, Anthropic, OpenAI, and Meta AI.
"""

from typing import List
import xml.etree.ElementTree as ET
import requests
import urllib3

from config import REQUEST_HEADERS, REQUEST_TIMEOUT
from models import AIResearchItem
from summarizer import summarize_ai_research

urllib3.disable_warnings()

LAB_FEEDS = [
    {
        "lab": "Anthropic Research",
        "query": "site:anthropic.com/research OR site:anthropic.com/news",
    },
    {
        "lab": "Google DeepMind",
        "query": "site:deepmind.google/discover/blog OR \"Google DeepMind\" research announcement",
    },
    {
        "lab": "OpenAI Research",
        "query": "site:openai.com/index OR site:openai.com/news frontier model research",
    },
    {
        "lab": "Meta AI Research",
        "query": "site:ai.meta.com/blog OR \"Meta AI\" open source model research",
    }
]


def fetch_lab_breakthroughs(limit_per_lab: int = 1) -> List[AIResearchItem]:
    """Fetches high-impact research announcements from frontier AI labs."""
    items: List[AIResearchItem] = []
    seen_urls = set()

    for feed in LAB_FEEDS:
        lab_name = feed["lab"]
        q = feed["query"]
        rss_url = f"https://news.google.com/rss/search?q={requests.utils.quote(q)}&hl=en-US&gl=US&ceid=US:en"

        try:
            resp = requests.get(rss_url, headers=REQUEST_HEADERS, timeout=REQUEST_TIMEOUT)
            if resp.status_code != 200:
                continue

            root = ET.fromstring(resp.content)
            entries = root.findall(".//item")

            count = 0
            for item in entries:
                title = item.find("title").text if item.find("title") is not None else ""
                link = item.find("link").text if item.find("link") is not None else ""
                pub_date = item.find("pubDate").text if item.find("pubDate") is not None else ""
                desc = item.find("description").text if item.find("description") is not None else ""

                if not title or not link or link in seen_urls:
                    continue

                seen_urls.add(link)

                # Clean title (remove trailing source suffix like ' - OpenAI')
                clean_title = title.split(" - ")[0].strip()

                crux, key_points, category = summarize_ai_research(clean_title, desc or clean_title)

                items.append(AIResearchItem(
                    id=AIResearchItem.generate_id(clean_title, link),
                    title=clean_title,
                    source=lab_name,
                    url=link,
                    pdf_url=None,
                    crux=crux,
                    key_points=key_points,
                    category=category,
                    score=95
                ))

                count += 1
                if count >= limit_per_lab:
                    break

        except Exception as e:
            print(f"[Lab Updates] Error querying {lab_name}: {e}")

    return items
