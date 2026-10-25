"""
Configuration for AI Research & Paradigm Shift Daily Intelligence Digest.
"""

import os

# Auto-load local .env if present
_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(_env_path):
    try:
        with open(_env_path, "r", encoding="utf-8") as _f:
            for _line in _f:
                _line = _line.strip()
                if _line and "=" in _line and not _line.startswith("#"):
                    _k, _v = _line.split("=", 1)
                    os.environ.setdefault(_k.strip(), _v.strip())
    except Exception:
        pass

# Delivery Email Configuration
DEFAULT_RECIPIENT_EMAIL = "anshu.airesearch@gmail.com"
RECIPIENT_EMAIL = os.environ.get("RECIPIENT_EMAIL", DEFAULT_RECIPIENT_EMAIL)

GMAIL_USER = os.environ.get("GMAIL_USER", "anshu.philosophy@gmail.com")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "gtxrzidztjhsskca")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Optional Gemini API Key for deeper semantic synthesis
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Request Settings
REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}
REQUEST_TIMEOUT = 12

# File Paths
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(DATA_DIR, "ai_news_history.json")
README_FILE = os.path.join(DATA_DIR, "README.md")
