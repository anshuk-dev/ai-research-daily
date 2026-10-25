"""
Intelligent AI Research Summarizer.
Extracts:
  - The Crux (1-2 sentences in simple English)
  - Key bullet points (Core Breakthrough, Benchmark Metrics, Paradigm Shift / Why It Matters)
  - Domain Category classification
Works out of the box with built-in NLP, and optionally supports Gemini API if a key is provided.
"""

import json
import re
from typing import List, Tuple
from config import GEMINI_API_KEY


def classify_category(title: str, text: str) -> str:
    """Classifies AI research into clear topical pillars."""
    combined = f"{title} {text}".lower()
    if any(k in combined for k in ["agent", "recursive", "tool use", "planning", "autonomous", "self-improve"]):
        return "Autonomous Agents & Self-Improvement"
    if any(k in combined for k in ["reasoning", "math", "code", "post-training", "distillation", "cot", "chain of thought"]):
        return "Reasoning & Frontier Architectures"
    if any(k in combined for k in ["interpretability", "safety", "alignment", "red team", "probe", "steering", "jailbreak"]):
        return "Alignment & Interpretability"
    if any(k in combined for k in ["embodied", "robot", "vision", "video", "multimodal", "audio"]):
        return "Embodied & Multimodal AI"
    if any(k in combined for k in ["scale", "cluster", "distributed", "serving", "quantization", "latency", "hardware"]):
        return "AI Systems & Infrastructure"
    return "Frontier AI Research"


def clean_text_for_summary(text: str) -> str:
    """Removes citations like [1], [2], urls, and excessive academic fluff."""
    text = re.sub(r'\[\d+\]', '', text)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def nlp_summarize_paper(title: str, abstract: str) -> Tuple[str, List[str]]:
    """Built-in pure-Python NLP extraction of crux and bullet points."""
    clean_abs = clean_text_for_summary(abstract)
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', clean_abs) if len(s.strip()) > 25]

    if not sentences:
        return clean_abs[:200], [f"💡 **Overview:** {clean_abs[:180]}..."]

    # 1. The Crux: First 1 or 2 sentences stating the problem and solution
    if len(sentences) >= 2:
        crux = f"{sentences[0]} {sentences[1]}"
    else:
        crux = sentences[0]

    # 2. Key Bullet Points
    bullets = []

    # A. Core Breakthrough
    breakthrough_sentences = [
        s for s in sentences
        if any(w in s.lower() for w in ["propose", "introduce", "develop", "present", "framework", "architecture", "method", "model", "show that"])
    ]
    if breakthrough_sentences:
        bullets.append(f"💡 **Core Innovation:** {breakthrough_sentences[0]}")
    elif len(sentences) > 1:
        bullets.append(f"💡 **Core Innovation:** {sentences[1]}")

    # B. Key Metric / Empirical Result
    metric_sentences = [
        s for s in sentences
        if any(w in s.lower() for w in ["achieve", "outperform", "%", "x", "result", "benchmark", "accuracy", "faster", "evaluat", "state-of-the-art", "sota"])
    ]
    if metric_sentences:
        bullets.append(f"📊 **Key Results:** {metric_sentences[0]}")

    # C. Paradigm Shift / Why It Matters
    shift_sentences = [
        s for s in sentences
        if any(w in s.lower() for w in ["shift", "foundational", "enable", "future", "implication", "crucial", "demonstrate", "open the door", "pave", "critical"])
    ]
    if shift_sentences:
        bullets.append(f"🚀 **Paradigm Shift:** {shift_sentences[0]}")
    elif len(sentences) > 2:
        bullets.append(f"🚀 **Why It Matters:** {sentences[-1]}")

    # Fallback if fewer than 2 bullets found
    if len(bullets) < 2 and len(sentences) > 2:
        bullets.append(f"📌 **Key Finding:** {sentences[2]}")

    return crux, bullets


def summarize_ai_research(title: str, text_or_abstract: str) -> Tuple[str, List[str], str]:
    """
    Main summarization entry point.
    Returns: (crux, key_points, category)
    """
    category = classify_category(title, text_or_abstract)

    # If Gemini API key is provided, use Google GenAI
    if GEMINI_API_KEY:
        try:
            from google import genai
            client = genai.Client(api_key=GEMINI_API_KEY)
            prompt = f"""You are an elite AI research analyst. Summarize this research paper or breakthrough for senior AI researchers and engineers.
Title: {title}
Content: {text_or_abstract[:2500]}

Respond ONLY in valid JSON format with these exact keys:
{{
  "crux": "1 to 2 crisp, simple English sentences explaining what was created or discovered",
  "key_points": [
    "💡 Core Breakthrough: ...",
    "📊 Key Results / Metric: ...",
    "🚀 Paradigm Shift / Why It Matters: ..."
  ]
}}
"""
            resp = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            data = json.loads(resp.text)
            return data.get("crux", ""), data.get("key_points", []), category
        except Exception:
            pass

    # Default to built-in NLP summarizer
    crux, bullets = nlp_summarize_paper(title, text_or_abstract)
    return crux, bullets, category
