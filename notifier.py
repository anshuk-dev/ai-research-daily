"""
Email notification module for AI Research Daily.
Generates an executive-grade HTML intelligence briefing and sends via Gmail SMTP.
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

from config import (
    GMAIL_USER,
    GMAIL_APP_PASSWORD,
    RECIPIENT_EMAIL,
    SMTP_SERVER,
    SMTP_PORT
)
from models import AIResearchItem


def build_newsletter_content(items: List[AIResearchItem], date_str: str) -> tuple[str, str]:
    """Builds both plain-text and executive HTML newsletter."""
    count = len(items)

    # 1. Plain Text Version
    text_lines = [
        "AI RESEARCH & BREAKTHROUGH INTELLIGENCE BRIEFING",
        f"Edition: {date_str} | {count} High-Impact Breakthroughs\n",
        "=" * 65,
    ]

    for idx, it in enumerate(items, 1):
        text_lines.append(f"\n[{idx}] {it.title}")
        text_lines.append(f"Source: {it.source} | Category: {it.category}")
        text_lines.append(f"\nTHE CRUX (Simple English):\n{it.crux}")
        text_lines.append("\nKEY TAKEAWAYS & PARADIGM SHIFT:")
        for pt in it.key_points:
            text_lines.append(f"  • {pt}")
        text_lines.append(f"\nSource URL: {it.url}")
        if it.pdf_url:
            text_lines.append(f"PDF URL: {it.pdf_url}")
        text_lines.append("-" * 45)

    text_lines.append(f"\nDelivered automatically to {RECIPIENT_EMAIL} by AI Research Daily.")
    plain_text = "\n".join(text_lines)

    # 2. Executive HTML Cards
    cards_html = []
    for it in items:
        bullets_html = "".join([
            f"<li style='margin-bottom:8px; line-height:1.6; color:#334155; font-size:13.5px;'>{b}</li>"
            for b in it.key_points
        ])

        pdf_btn = ""
        if it.pdf_url:
            pdf_btn = f"""
            <a href="{it.pdf_url}" style="display:inline-block; padding:8px 16px; margin-top:10px; margin-right:8px; background-color:#475569; color:#ffffff; text-decoration:none; border-radius:6px; font-weight:600; font-size:12.5px;">
                📥 Read Full PDF
            </a>
            """

        source_btn = f"""
        <a href="{it.url}" style="display:inline-block; padding:8px 16px; margin-top:10px; background-color:#2563eb; color:#ffffff; text-decoration:none; border-radius:6px; font-weight:600; font-size:12.5px;">
            🔗 View Primary Source
        </a>
        """

        card = f"""
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:22px; margin-bottom:22px; box-shadow:0 1px 3px rgba(0,0,0,0.06);">
            <!-- Card Header Badge -->
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <span style="font-size:11.5px; font-weight:700; background:#ede9fe; color:#5b21b6; padding:4px 10px; border-radius:16px; text-transform:uppercase; letter-spacing:0.5px;">
                    {it.category}
                </span>
                <span style="font-size:12px; color:#64748b; font-weight:600;">
                    🏛️ {it.source}
                </span>
            </div>

            <!-- Title -->
            <h2 style="margin:0 0 10px 0; color:#0f172a; font-size:17.5px; font-weight:800; line-height:1.4;">
                {it.title}
            </h2>

            <!-- The Crux Box -->
            <div style="background:#f0f9ff; border-left:4px solid #0284c7; padding:12px 16px; border-radius:6px; margin-bottom:14px;">
                <p style="margin:0; font-size:13.5px; color:#0369a1; font-weight:600; line-height:1.5;">
                    💡 <strong>The Crux:</strong> {it.crux}
                </p>
            </div>

            <!-- Key Takeaways & Paradigm Shift -->
            <div style="margin-bottom:14px;">
                <p style="margin:0 0 8px 0; font-size:13px; font-weight:700; color:#475569; text-transform:uppercase; letter-spacing:0.4px;">
                    Key Takeaways & Paradigm Shift:
                </p>
                <ul style="margin:0; padding-left:20px;">
                    {bullets_html}
                </ul>
            </div>

            <!-- Action Buttons -->
            <div>
                {source_btn}
                {pdf_btn}
            </div>
        </div>
        """
        cards_html.append(card)

    all_cards = "\n".join(cards_html)

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>AI Research & Paradigm Shift Intelligence</title>
    </head>
    <body style="font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color:#f1f5f9; margin:0; padding:24px; color:#1e293b;">
        <div style="max-width:680px; margin:0 auto; background:#ffffff; border-radius:14px; overflow:hidden; border:1px solid #cbd5e1; box-shadow:0 10px 15px -3px rgba(0,0,0,0.1);">
            <!-- Header Banner -->
            <div style="background:linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #312e81 100%); padding:30px 24px; text-align:center; color:#ffffff;">
                <h1 style="margin:0 0 8px 0; font-size:24px; font-weight:800; letter-spacing:-0.5px;">
                    ⚡ AI Research & Paradigm Shifts
                </h1>
                <p style="margin:0 0 10px 0; font-size:14.5px; color:#cbd5e1; font-weight:500;">
                    Daily Executive Intelligence Digest
                </p>
                <span style="display:inline-block; background:rgba(255,255,255,0.15); padding:4px 12px; border-radius:20px; font-size:12px; font-weight:600; color:#e2e8f0;">
                    📅 {date_str} &bull; {count} Breakthroughs Monitored
                </span>
            </div>

            <!-- Body -->
            <div style="padding:24px; background:#f8fafc;">
                <p style="margin:0 0 20px 0; font-size:14px; color:#475569; line-height:1.6;">
                    Hello <strong>Anshu</strong>, here is your curated daily intelligence brief summarizing today's most significant AI research papers, foundational announcements, and paradigm shifts from top primary sources:
                </p>

                {all_cards}
            </div>

            <!-- Footer -->
            <div style="background:#f1f5f9; padding:18px 24px; text-align:center; border-top:1px solid #e2e8f0; font-size:12px; color:#64748b;">
                <p style="margin:0 0 4px 0;">
                    Automated 100% Free Intelligence Digest for <strong>{RECIPIENT_EMAIL}</strong>
                </p>
                <p style="margin:0;">
                    Sources: Google DeepMind &bull; OpenAI &bull; Anthropic &bull; arXiv &bull; Hugging Face &bull; MIT Tech Review
                </p>
            </div>
        </div>
    </body>
    </html>
    """

    return plain_text, html_content


def send_briefing_email(items: List[AIResearchItem], date_str: str) -> bool:
    """Sends executive briefing to anshu.airesearch@gmail.com."""
    if not items:
        print("[Notifier] No items to send.")
        return True

    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        print("[Notifier] Missing GMAIL credentials.")
        return False

    count = len(items)
    subject = f"⚡ [AI Daily] {count} Breakthrough Research Papers & Paradigm Shifts ({date_str})"

    plain_body, html_body = build_newsletter_content(items, date_str)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"AI Research Intelligence <{GMAIL_USER}>"
    msg["To"] = RECIPIENT_EMAIL

    msg.attach(MIMEText(plain_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        print(f"[Notifier] Connecting to {SMTP_SERVER}:{SMTP_PORT}...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=20)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, [RECIPIENT_EMAIL], msg.as_string())
        server.quit()
        print(f"[Notifier] ✅ Successfully sent AI Research Digest to {RECIPIENT_EMAIL}!")
        return True
    except Exception as e:
        print(f"[Notifier] Error sending email: {e}")
        return False
