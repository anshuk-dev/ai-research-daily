"""
Main Orchestrator for AI Research & Paradigm Shifts Daily Digest.
Coordinates fetching from primary sources, NLP summarization, deduplication, README updating, and email delivery.
"""

from datetime import datetime
import pytz

from sources.huggingface_papers import fetch_huggingface_top_papers
from sources.lab_updates import fetch_lab_breakthroughs
from sources.tech_review import fetch_tech_review_articles
from storage import filter_new_items, update_readme_briefing
from notifier import send_briefing_email


def get_current_date_str() -> str:
    """Returns formatted date string in IST."""
    try:
        ist = pytz.timezone("Asia/Kolkata")
        return datetime.now(ist).strftime("%d %B %Y")
    except Exception:
        return datetime.now().strftime("%d %B %Y")


def main():
    date_str = get_current_date_str()
    print("=" * 70)
    print(f"⚡ AI Research & Paradigm Shift Intelligence Digest ({date_str})")
    print("=" * 70)

    all_discovered = []

    # 1. Fetch Top Community-Voted Papers from Hugging Face / arXiv
    print("\n[1/3] Fetching Top Community-Voted arXiv Research (Hugging Face)...")
    try:
        hf_papers = fetch_huggingface_top_papers(limit=5)
        print(f"      Fetched {len(hf_papers)} top research papers.")
        all_discovered.extend(hf_papers)
    except Exception as e:
        print(f"      Error: {e}")

    # 2. Fetch Frontier Lab Updates (DeepMind, Anthropic, OpenAI, Meta AI)
    print("\n[2/3] Fetching Frontier Lab Research Updates (DeepMind, Anthropic, OpenAI)...")
    try:
        lab_items = fetch_lab_breakthroughs(limit_per_lab=1)
        print(f"      Fetched {len(lab_items)} lab announcements.")
        all_discovered.extend(lab_items)
    except Exception as e:
        print(f"      Error: {e}")

    # 3. Fetch MIT Technology Review AI Insights
    print("\n[3/3] Fetching MIT Technology Review AI Analysis...")
    try:
        mit_items = fetch_tech_review_articles(limit=2)
        print(f"      Fetched {len(mit_items)} analysis articles.")
        all_discovered.extend(mit_items)
    except Exception as e:
        print(f"      Error: {e}")

    print("\n" + "-" * 70)
    print(f"Total candidate research stories collected: {len(all_discovered)}")

    # Deduplicate against history
    new_items, all_items = filter_new_items(all_discovered)

    print(f"New breakthrough items detected for today's briefing: {len(new_items)}")

    # Pick top items to feature in today's newsletter (max 6-7 high-signal items)
    items_to_send = new_items if new_items else all_items[:5]

    # Update README Dashboard Archive
    update_readme_briefing(items_to_send, date_str)
    print("✅ README.md briefing archive updated.")

    # Send Daily Email Digest
    if items_to_send:
        print(f"\n🚀 Sending AI Daily Briefing with {len(items_to_send)} breakthroughs to recipient...")
        send_briefing_email(items_to_send, date_str)
    else:
        print("\nℹ️ No items to send today.")

    print("\n" + "=" * 70)
    print("🏁 AI Daily Briefing completed successfully.")
    print("=" * 70)


if __name__ == "__main__":
    main()
