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
    """
    Builds an executive-grade, world-class HTML tech newsletter and plain-text briefing.
    Designed in the visual style of top industry publications (The Batch, TLDR AI, Import AI),
    with table-based bulletproof rendering for flawless display across all email clients.
    """
    count = len(items)

    # 1. Plain Text Version
    text_lines = [
        "=================================================================",
        "   ⚡ THE AI PARADIGM // DAILY RESEARCH INTELLIGENCE BRIEFING",
        "        Frontier Papers • Foundation Models • Paradigm Shifts",
        "=================================================================",
        f"Edition: {date_str} | {count} High-Impact Breakthroughs\n",
    ]

    for idx, it in enumerate(items, 1):
        text_lines.append(f"[{idx:02d}] {it.title.upper()}")
        text_lines.append(f"     Source   : {it.source} | Category: {it.category}")
        text_lines.append(f"\n     💡 THE CRUX (Simple English):\n     {it.crux}\n")
        text_lines.append("     ⚡ KEY BREAKTHROUGHS & TAKEAWAYS:")
        for pt in it.key_points:
            text_lines.append(f"       • {pt}")
        text_lines.append(f"\n     🔗 Primary Source: {it.url}")
        if it.pdf_url:
            text_lines.append(f"     📥 Paper PDF    : {it.pdf_url}")
        text_lines.append("-" * 65)

    text_lines.append(f"\nDelivered automatically to {RECIPIENT_EMAIL} by AI Research Daily.")
    plain_text = "\n".join(text_lines)

    # 2. Executive HTML Cards
    cards_html = []
    for idx, it in enumerate(items, 1):
        # Color coding for primary sources
        source_lower = it.source.lower()
        if "deepmind" in source_lower:
            src_bg = "#eff6ff"
            src_border = "#bfdbfe"
            src_color = "#1d4ed8"
            src_icon = "🏛️ DeepMind"
        elif "anthropic" in source_lower:
            src_bg = "#fef3c7"
            src_border = "#fde68a"
            src_color = "#92400e"
            src_icon = "🤖 Anthropic"
        elif "openai" in source_lower:
            src_bg = "#ecfdf5"
            src_border = "#a7f3d0"
            src_color = "#065f46"
            src_icon = "🧠 OpenAI"
        elif "meta" in source_lower:
            src_bg = "#eff6ff"
            src_border = "#bfdbfe"
            src_color = "#1e40af"
            src_icon = "🌐 Meta AI"
        elif "mit" in source_lower:
            src_bg = "#fef2f2"
            src_border = "#fecaca"
            src_color = "#991b1b"
            src_icon = "🔬 MIT Tech"
        else:
            src_bg = "#fffbeb"
            src_border = "#fef3c7"
            src_color = "#b45309"
            src_icon = "📄 arXiv / HF"

        # Bullets formatting
        bullets_rows = []
        for pt in it.key_points:
            bullets_rows.append(f"""
            <tr>
                <td style="padding: 3px 0; vertical-align: top; width: 18px; color: #6366f1; font-weight: 800; font-size: 14px;">
                    ✦
                </td>
                <td style="padding: 3px 0 6px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 13.5px; color: #334155; line-height: 1.55;">
                    {pt}
                </td>
            </tr>
            """)
        bullets_html = "".join(bullets_rows)

        # Action Buttons
        pdf_button_html = ""
        if it.pdf_url:
            pdf_button_html = f"""
            <td style="padding-right: 10px;">
                <table border="0" cellpadding="0" cellspacing="0">
                    <tr>
                        <td align="center" style="border-radius: 6px; background-color: #4f46e5;">
                            <a href="{it.pdf_url}" target="_blank" style="display: inline-block; padding: 8px 16px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 12.5px; font-weight: 700; color: #ffffff; text-decoration: none; border-radius: 6px;">
                                📥 Read PDF Paper &rarr;
                            </a>
                        </td>
                    </tr>
                </table>
            </td>
            """

        source_button_html = f"""
        <td>
            <table border="0" cellpadding="0" cellspacing="0">
                <tr>
                    <td align="center" style="border-radius: 6px; background-color: #0f172a;">
                        <a href="{it.url}" target="_blank" style="display: inline-block; padding: 8px 15px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 12.5px; font-weight: 600; color: #ffffff; text-decoration: none; border-radius: 6px;">
                            🔗 View Primary Source &nearr;
                        </a>
                    </td>
                </tr>
            </table>
        </td>
        """

        card = f"""
        <!-- RESEARCH ITEM CARD {idx:02d} -->
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #ffffff; border: 1px solid #e2e8f0; border-top: 3px solid #6366f1; border-radius: 8px; margin-bottom: 22px; box-shadow: 0 2px 6px rgba(0,0,0,0.04);">
            <tr>
                <td style="padding: 20px 22px;">

                    <!-- Metadata Header -->
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom: 10px;">
                        <tr>
                            <td align="left">
                                <span style="display: inline-block; background-color: #0f172a; color: #38bdf8; font-family: 'SF Mono', Menlo, Consolas, monospace; font-size: 10.5px; font-weight: 700; padding: 3px 8px; border-radius: 4px; margin-right: 6px;">
                                    #{idx:02d}
                                </span>
                                <span style="display: inline-block; background-color: #ede9fe; border: 1px solid #ddd6fe; color: #5b21b6; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 10.5px; font-weight: 700; padding: 3px 10px; border-radius: 12px; text-transform: uppercase; letter-spacing: 0.5px;">
                                    ⚡ {it.category}
                                </span>
                            </td>
                            <td align="right">
                                <span style="display: inline-block; background-color: {src_bg}; border: 1px solid {src_border}; color: {src_color}; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 12px;">
                                    {src_icon}
                                </span>
                            </td>
                        </tr>
                    </table>

                    <!-- Headline Title -->
                    <h2 style="margin: 0 0 12px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 17.5px; font-weight: 800; line-height: 1.4; letter-spacing: -0.3px;">
                        <a href="{it.url}" target="_blank" style="color: #0f172a; text-decoration: none;">
                            {it.title}
                        </a>
                    </h2>

                    <!-- The Crux (Simple English Callout Box) -->
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f5f3ff; border-left: 4px solid #6366f1; border-radius: 0 6px 6px 0; margin-bottom: 14px;">
                        <tr>
                            <td style="padding: 12px 14px;">
                                <p style="margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 13.5px; color: #312e81; font-weight: 600; line-height: 1.5;">
                                    <strong style="color: #4f46e5; text-transform: uppercase; font-size: 11px; letter-spacing: 0.8px; display: block; margin-bottom: 4px;">💡 THE CRUX (Simple English)</strong>
                                    {it.crux}
                                </p>
                            </td>
                        </tr>
                    </table>

                    <!-- Key Takeaways & Paradigm Shift -->
                    <div style="margin-bottom: 14px;">
                        <span style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11px; font-weight: 800; color: #64748b; text-transform: uppercase; letter-spacing: 0.8px; display: block; margin-bottom: 6px;">
                            ⚡ Key Breakthroughs & Paradigm Shift:
                        </span>
                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                            {bullets_html}
                        </table>
                    </div>

                    <!-- Action Buttons -->
                    <table border="0" cellpadding="0" cellspacing="0">
                        <tr>
                            {pdf_button_html}
                            {source_button_html}
                        </tr>
                    </table>

                </td>
            </tr>
        </table>
        """
        cards_html.append(card)

    all_cards = "\n".join(cards_html)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>THE AI PARADIGM // Daily Research Intelligence Briefing</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0b0f19; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased;">

    <!-- Hidden Preheader for Inbox Preview -->
    <div style="display: none; font-size: 1px; color: #0b0f19; line-height: 1px; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden; mso-hide: all;">
        ⚡ Today's AI Breakthroughs: {count} paradigm-shifting papers & announcements from arXiv, DeepMind, Anthropic, OpenAI & MIT. Simple English Crux & verified links inside.
    </div>

    <!-- Outer Wrapper -->
    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #0b0f19; padding: 25px 0;">
        <tr>
            <td align="center">

                <!-- Main Container (640px) -->
                <table border="0" cellpadding="0" cellspacing="0" width="640" style="max-width: 640px; width: 100%; background-color: #111827; border-radius: 12px; overflow: hidden; border: 1px solid #1f2937; box-shadow: 0 12px 30px -5px rgba(0,0,0,0.5);">
                    
                    <!-- ELECTRIC GRADIENT ACCENT STRIP -->
                    <tr>
                        <td height="4" style="background: linear-gradient(90deg, #6366f1 0%, #a855f7 35%, #06b6d4 70%, #10b981 100%); font-size: 1px; line-height: 1px;">
                            &nbsp;
                        </td>
                    </tr>

                    <!-- MODERN OBSIDIAN HEADER (The Batch & TLDR AI Style) -->
                    <tr>
                        <td style="background-color: #090d16; padding: 32px 30px; text-align: left; border-bottom: 1px solid #1f2937;">
                            
                            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tr>
                                    <td>
                                        <span style="font-family: 'SF Mono', Menlo, Consolas, monospace; font-size: 11px; font-weight: 700; color: #38bdf8; letter-spacing: 2px; text-transform: uppercase;">
                                            DAILY RESEARCH BRIEFING &bull; EDITION {date_str}
                                        </span>
                                        <h1 style="margin: 8px 0 6px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 26px; font-weight: 800; color: #ffffff; letter-spacing: -0.8px; line-height: 1.2;">
                                            ⚡ THE AI PARADIGM
                                        </h1>
                                        <p style="margin: 0 0 14px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 13.5px; color: #94a3b8; font-weight: 500;">
                                            Frontier Papers &bull; Foundation Reasoning &bull; Architectural Breakthroughs
                                        </p>
                                        <span style="display: inline-block; background-color: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.35); color: #c7d2fe; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11.5px; font-weight: 700; padding: 4px 12px; border-radius: 16px;">
                                            🔥 {count} High-Impact Breakthroughs Monitored Today
                                        </span>
                                    </td>
                                </tr>
                            </table>

                        </td>
                    </tr>

                    <!-- EXECUTIVE SYNTHESIS / TLDR CALLOUT -->
                    <tr>
                        <td style="background-color: #0d1322; padding: 18px 28px; border-bottom: 1px solid #1f2937;">
                            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tr>
                                    <td style="padding: 12px 16px; background-color: #162033; border-left: 3px solid #38bdf8; border-radius: 0 6px 6px 0;">
                                        <span style="font-family: 'SF Mono', Menlo, monospace; font-size: 11px; font-weight: 700; color: #38bdf8; text-transform: uppercase; letter-spacing: 1px; display: block; margin-bottom: 4px;">
                                            📌 TODAY'S RESEARCH SYNTHESIS
                                        </span>
                                        <p style="margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 13px; color: #cbd5e1; line-height: 1.55;">
                                            Today's releases highlight massive advancements in <strong>test-time compute scaling</strong>, <strong>multi-token reasoning</strong>, and <strong>autonomous agent architectures</strong>. Each item below includes its plain English crux, core breakthroughs, and direct links to the official paper/code.
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- CONTENT CONTAINER (Light Canvas for High Contrast Reading) -->
                    <tr>
                        <td style="padding: 24px 26px; background-color: #f8fafc;">
                            
                            <!-- CARDS INJECTION -->
                            {all_cards}

                        </td>
                    </tr>

                    <!-- MONITORED SOURCES STRIP -->
                    <tr>
                        <td style="background-color: #0d1322; padding: 16px 24px; text-align: center; border-top: 1px solid #1f2937;">
                            <span style="font-family: 'SF Mono', Menlo, monospace; font-size: 10px; font-weight: 700; color: #64748b; letter-spacing: 1.5px; text-transform: uppercase; display: block; margin-bottom: 8px;">
                                PRIMARY SOURCES CONTINUOUSLY MONITORED
                            </span>
                            <span style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11.5px; color: #94a3b8; font-weight: 600;">
                                Google DeepMind &bull; Anthropic &bull; OpenAI &bull; Meta AI &bull; Hugging Face / arXiv &bull; MIT Tech Review
                            </span>
                        </td>
                    </tr>

                    <!-- EXECUTIVE TECH FOOTER -->
                    <tr>
                        <td style="background-color: #090d16; padding: 24px 30px; text-align: center; border-top: 1px solid #1f2937;">
                            <p style="margin: 0 0 6px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 13px; font-weight: 700; color: #f1f5f9;">
                                THE AI PARADIGM &bull; Autonomous Research Intelligence Dispatch
                            </p>
                            <p style="margin: 0 0 10px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 12px; color: #64748b; line-height: 1.5;">
                                Delivered automatically every morning at 07:30 AM IST to <strong style="color: #38bdf8;">{RECIPIENT_EMAIL}</strong><br>
                                Running 24x7 Cloud Pipeline via GitHub Actions &bull; 100% Free & Open Source
                            </p>
                            <p style="margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11px; color: #475569;">
                                Curated for researchers, engineers, and AI pioneers. Unbiased primary source synthesis.
                            </p>
                        </td>
                    </tr>

                </table><!-- /Main Container -->

            </td>
        </tr>
    </table><!-- /Outer Wrapper -->

</body>
</html>
"""

    return plain_text, html_content

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
