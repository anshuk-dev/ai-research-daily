"""
Source scraper for Hugging Face Daily Papers (Top Community-Voted Research Breakthroughs).
"""

from typing import List
import requests
import urllib3

from config import REQUEST_HEADERS, REQUEST_TIMEOUT
from models import AIResearchItem
from summarizer import summarize_ai_research

urllib3.disable_warnings()

HF_DAILY_PAPERS_API = "https://huggingface.co/api/daily_papers"


def fetch_huggingface_top_papers(limit: int = 5) -> List[AIResearchItem]:
    """Fetches top upvoted daily AI papers from Hugging Face."""
    items: List[AIResearchItem] = []

    try:
        resp = requests.get(HF_DAILY_PAPERS_API, headers=REQUEST_HEADERS, timeout=REQUEST_TIMEOUT)
        if resp.status_code != 200:
            print(f"[HF Papers] Failed with HTTP {resp.status_code}")
            return items

        data = resp.json()
        if not isinstance(data, list):
            return items

        # Sort by upvotes descending
        data.sort(key=lambda x: x.get("paper", {}).get("upvotes", 0), reverse=True)

        for entry in data[:limit]:
            paper = entry.get("paper", {})
            title = paper.get("title", "").strip()
            summary = paper.get("summary", "").strip()
            paper_id = paper.get("id", "")
            upvotes = paper.get("upvotes", 0)

            if not title or not summary:
                continue

            primary_url = f"https://huggingface.co/papers/{paper_id}"
            pdf_url = f"https://arxiv.org/pdf/{paper_id}.pdf"

            crux, key_points, category = summarize_ai_research(title, summary)

            items.append(AIResearchItem(
                id=AIResearchItem.generate_id(title, primary_url),
                title=title,
                source=f"arXiv / Hugging Face ({upvotes} upvotes)",
                url=primary_url,
                pdf_url=pdf_url,
                crux=crux,
                key_points=key_points,
                category=category,
                score=upvotes
            ))

    except Exception as e:
        print(f"[HF Papers] Error: {e}")

    return items
