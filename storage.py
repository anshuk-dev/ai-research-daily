"""
Storage and README briefing archive generator for AI Research Daily.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Tuple

from config import HISTORY_FILE, README_FILE
from models import AIResearchItem


def load_history() -> Dict[str, dict]:
    """Load previously discovered AI research items."""
    if not os.path.exists(HISTORY_FILE):
        return {}
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_history(history: Dict[str, dict]) -> None:
    """Save history back to file."""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[Storage] Error writing history: {e}")


def filter_new_items(items: List[AIResearchItem]) -> Tuple[List[AIResearchItem], List[AIResearchItem]]:
    """Deduplicates items against history."""
    history = load_history()
    new_items: List[AIResearchItem] = []
    all_dict: Dict[str, dict] = dict(history)

    for item in items:
        if item.id not in history:
            new_items.append(item)
            all_dict[item.id] = item.to_dict()

    save_history(all_dict)
    all_items = [AIResearchItem.from_dict(d) for d in all_dict.values()]
    all_items.sort(key=lambda x: x.discovered_at or "", reverse=True)

    return new_items, all_items


def update_readme_briefing(today_items: List[AIResearchItem], date_str: str) -> None:
    """Generates an executive briefing in README.md."""
    sections = []
    for idx, item in enumerate(today_items, 1):
        bullets_md = "\n".join([f"  - {b}" for b in item.key_points])
        pdf_md = f" &bull; [📥 Download PDF]({item.pdf_url})" if item.pdf_url else ""
        sections.append(f"""### {idx}. {item.title}
**🏛️ Source:** `{item.source}` &bull; **🏷️ Pillar:** `{item.category}`

> **The Crux (Simple English):**  
> {item.crux}

**Key Takeaways & Paradigm Shift:**
{bullets_md}

🔗 **Primary Source URL:** [{item.url}]({item.url}){pdf_md}
""")

    articles_md = "\n---\n".join(sections) if sections else "*All research digests are up to date.*"

    readme_content = f"""# ⚡ AI Research & Paradigm Shifts: Daily Intelligence Brief

> Automated high-signal executive intelligence briefing covering cutting-edge AI breakthroughs, research papers, and paradigm shifts from top primary sources (OpenAI, Google DeepMind, Anthropic, arXiv, Hugging Face, MIT Tech Review).

[![AI Daily Briefing](https://github.com/actions/workflows/ai_daily_brief.yml/badge.svg)](https://github.com/actions/workflows/ai_daily_brief.yml)
**Latest Edition:** `{date_str}`  
**Delivery Inboxes:** `anshu.airesearch@gmail.com`

---

## 🔬 Today's Top Breakthroughs & Paradigm Shifts

{articles_md}

---

## 🎯 Primary Intelligence Sources Monitored
- **Frontier Research Labs:** Google DeepMind, OpenAI Research, Anthropic Research, Meta AI.
- **Academic Curators:** Hugging Face Top Daily Papers (Community-voted arXiv breakthroughs).
- **Elite Publications:** MIT Technology Review (AI Section), Nature Machine Intelligence.

---

## ⚡ How This Automated System Works
1. **GitHub Actions Workflow** executes every morning at **07:30 AM IST** completely free on cloud runners.
2. It collects papers and announcements from primary sources, discarding hype and retaining high-signal breakthroughs.
3. Distills each breakthrough into:
   - **The Crux** in simple English.
   - **Key Bullet Points** (Core Innovation, Benchmark Results, Paradigm Shift).
   - **Verified Source URLs** for peer review and replication.
4. Dispatches an executive HTML morning briefing directly to **`anshu.airesearch@gmail.com`**.
"""

    try:
        with open(README_FILE, "w", encoding="utf-8") as f:
            f.write(readme_content)
    except Exception as e:
        print(f"[Storage] Error writing README: {e}")
