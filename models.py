"""
Data model for AI Research & Paradigm Shift news items.
"""

import hashlib
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import List, Optional


@dataclass
class AIResearchItem:
    id: str
    title: str
    source: str
    url: str
    crux: str
    key_points: List[str] = field(default_factory=list)
    pdf_url: Optional[str] = None
    category: str = "Frontier AI Research"
    score: int = 0
    discovered_at: str = ""

    def __post_init__(self):
        if not self.discovered_at:
            self.discovered_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")
        if not self.id:
            self.id = self.generate_id(self.title, self.url)

    @staticmethod
    def generate_id(title: str, url: str) -> str:
        base = f"{title.strip().lower()}|{url.strip().lower()}"
        return hashlib.sha256(base.encode("utf-8")).hexdigest()[:16]

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "AIResearchItem":
        return cls(**data)
