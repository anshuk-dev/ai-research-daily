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
    Builds a high-end, minimalist Editorial AI Tech Journal newsletter.
    Inspired by Adobe Express and Canva modern editorial publication templates
    (Swiss typographic hierarchy, stark contrast, hairline rules, generous whitespace,
    and elegant monochromatic styling with deep obsidian ink).
    Uses strict table-based architecture for bulletproof rendering across all email clients.
    """
    count = len(items)

    # 1. Plain Text Version
    text_lines = [
        "=================================================================",
        "                      THE AI PARADIGM",
        "        Daily Frontier Intelligence & Research Dispatch",
        "=================================================================",
        f"EDITION: {date_str.upper()}  |  {count} FOUNDATIONAL PAPERS MONITORED\n",
    ]

    for idx, it in enumerate(items, 1):
        text_lines.append(f"[{idx:02d}] {it.title.upper()}")
        text_lines.append(f"     SOURCE   : {it.source} | CATEGORY: {it.category}")
        text_lines.append(f"\n     THE CRUX (PLAIN ENGLISH):\n     {it.crux}\n")
        text_lines.append("     KEY BREAKTHROUGHS & PARADIGM SHIFT:")
        for pt in it.key_points:
            text_lines.append(f"       — {pt}")
        text_lines.append(f"\n     PRIMARY  : {it.url}")
        if it.pdf_url:
            text_lines.append(f"     PDF LINK : {it.pdf_url}")
        text_lines.append("-" * 65)

    text_lines.append(f"\nDispatched automatically to {RECIPIENT_EMAIL} by The AI Paradigm.")
    plain_text = "\n".join(text_lines)

    # 2. Editorial Minimalist HTML Cards
    cards_html = []
    for idx, it in enumerate(items, 1):
        # Action Buttons (Canva/Adobe Minimalist Solid + Ghost Buttons)
        pdf_button_html = ""
        if it.pdf_url:
            pdf_button_html = f"""
            <td style="padding-right: 12px;">
                <table border="0" cellpadding="0" cellspacing="0">
                    <tr>
                        <td align="center" style="background-color: #09090b; border-radius: 2px;">
                            <a href="{it.pdf_url}" target="_blank" style="display: inline-block; padding: 10px 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11px; font-weight: 700; color: #ffffff; text-decoration: none; text-transform: uppercase; letter-spacing: 1.5px;">
                                Read Paper (PDF) &rarr;
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
                    <td align="center" style="background-color: transparent; border: 1px solid #09090b; border-radius: 2px;">
                        <a href="{it.url}" target="_blank" style="display: inline-block; padding: 9px 18px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11px; font-weight: 700; color: #09090b; text-decoration: none; text-transform: uppercase; letter-spacing: 1.5px;">
                            Primary Source &nearr;
                        </a>
                    </td>
                </tr>
            </table>
        </td>
        """

        # Bullets formatting
        bullets_rows = []
        for pt in it.key_points:
            bullets_rows.append(f"""
            <tr>
                <td style="padding: 4px 0; vertical-align: top; width: 22px; color: #09090b; font-weight: 700; font-size: 13px;">
                    —
                </td>
                <td style="padding: 4px 0 6px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 13.5px; color: #3f3f46; line-height: 1.6;">
                    {pt}
                </td>
            </tr>
            """)
        bullets_html = "".join(bullets_rows)

        card = f"""
        <!-- RESEARCH ITEM CARD {idx:02d} -->
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #ffffff; border: 1px solid #e4e4e7; border-radius: 4px; margin-bottom: 28px; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
            <tr>
                <td style="padding: 26px 28px;">

                    <!-- Metadata Eyebrow Header -->
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom: 12px;">
                        <tr>
                            <td align="left">
                                <span style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 10.5px; font-weight: 800; color: #09090b; letter-spacing: 2px; text-transform: uppercase;">
                                    ITEM #{idx:02d} &bull; {it.category}
                                </span>
                            </td>
                            <td align="right">
                                <span style="display: inline-block; border: 1px solid #e4e4e7; background-color: #fafafa; color: #52525b; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 2px; text-transform: uppercase; letter-spacing: 1px;">
                                    {it.source}
                                </span>
                            </td>
                        </tr>
                    </table>

                    <!-- Headline Title -->
                    <h2 style="margin: 0 0 16px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 18.5px; font-weight: 800; line-height: 1.35; letter-spacing: -0.4px;">
                        <a href="{it.url}" target="_blank" style="color: #09090b; text-decoration: none;">
                            {it.title}
                        </a>
                    </h2>

                    <!-- The Crux (Minimalist Callout Box) -->
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #fafafa; border: 1px solid #e4e4e7; border-left: 3px solid #09090b; border-radius: 2px; margin-bottom: 16px;">
                        <tr>
                            <td style="padding: 14px 16px;">
                                <span style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 10px; font-weight: 800; color: #09090b; letter-spacing: 1.5px; text-transform: uppercase; display: block; margin-bottom: 5px;">
                                    THE CRUX (PLAIN ENGLISH)
                                </span>
                                <p style="margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 13.5px; color: #27272a; line-height: 1.55;">
                                    {it.crux}
                                </p>
                            </td>
                        </tr>
                    </table>

                    <!-- Key Takeaways & Paradigm Shift -->
                    <div style="margin-bottom: 18px;">
                        <span style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 10.5px; font-weight: 800; color: #71717a; text-transform: uppercase; letter-spacing: 1.2px; display: block; margin-bottom: 8px;">
                            KEY BREAKTHROUGHS & PARADIGM SHIFT:
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
<body style="margin: 0; padding: 0; background-color: #f4f4f5; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased;">

    <!-- Hidden Preheader for Inbox Preview -->
    <div style="display: none; font-size: 1px; color: #f4f4f5; line-height: 1px; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden; mso-hide: all;">
        The AI Paradigm: {count} foundational research breakthroughs from arXiv, DeepMind, Anthropic, OpenAI & MIT. Plain English crux & verified sources.
    </div>

    <!-- Outer Wrapper -->
    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f4f4f5; padding: 36px 0;">
        <tr>
            <td align="center">

                <!-- Main Container (640px) -->
                <table border="0" cellpadding="0" cellspacing="0" width="640" style="max-width: 640px; width: 100%; background-color: #ffffff; border: 1px solid #e4e4e7; box-shadow: 0 4px 20px -2px rgba(0,0,0,0.03);">
                    
                    <!-- EDITORIAL MASTHEAD (Canva & Adobe Swiss Modern Style) -->
                    <tr>
                        <td style="padding: 34px 34px 24px 34px; background-color: #ffffff;">
                            
                            <!-- Overline / Eyebrow -->
                            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom: 14px;">
                                <tr>
                                    <td align="left">
                                        <span style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 10px; font-weight: 800; color: #09090b; letter-spacing: 2.5px; text-transform: uppercase;">
                                            PRIMARY INTELLIGENCE // RESEARCH DISPATCH
                                        </span>
                                    </td>
                                    <td align="right">
                                        <span style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 10px; font-weight: 700; color: #71717a; letter-spacing: 1.5px; text-transform: uppercase;">
                                            ISSUE #{date_str.replace(' ', '.')}
                                        </span>
                                    </td>
                                </tr>
                            </table>

                            <!-- Sharp Hairline Divider -->
                            <div style="height: 1px; background-color: #09090b; margin-bottom: 18px;"></div>

                            <!-- Publication Title (Neo-Grotesque Bold Sans) -->
                            <h1 style="margin: 0 0 6px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 32px; font-weight: 900; color: #09090b; letter-spacing: -1.2px; text-transform: uppercase; line-height: 1.1;">
                                The AI Paradigm
                            </h1>

                            <!-- Subhead -->
                            <p style="margin: 0 0 16px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; color: #71717a; line-height: 1.45;">
                                A curated daily dispatch of foundational papers, reasoning architectures, and paradigm shifts.
                            </p>

                            <!-- Issue Metadata Strip -->
                            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-top: 1px solid #e4e4e7; border-bottom: 1px solid #e4e4e7; padding: 8px 0;">
                                <tr>
                                    <td align="left" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 10.5px; font-weight: 700; color: #71717a; letter-spacing: 1px; text-transform: uppercase;">
                                        EDITION: {date_str.upper()} &nbsp;&bull;&nbsp; PAPERS MONITORED: {count} &nbsp;&bull;&nbsp; READ: 4 MIN
                                    </td>
                                </tr>
                            </table>

                        </td>
                    </tr>

                    <!-- EDITORIAL SYNTHESIS / MEMORANDUM -->
                    <tr>
                        <td style="padding: 0 34px 20px 34px; background-color: #ffffff;">
                            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #fafafa; border: 1px solid #e4e4e7; border-radius: 4px;">
                                <tr>
                                    <td style="padding: 16px 20px;">
                                        <span style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 10px; font-weight: 800; color: #09090b; text-transform: uppercase; letter-spacing: 1.5px; display: block; margin-bottom: 6px;">
                                            MEMORANDUM // TODAY'S META-THEME
                                        </span>
                                        <p style="margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 13.5px; color: #3f3f46; line-height: 1.6;">
                                            Today's breakthrough research reflects accelerated shifts toward <strong>test-time compute optimization</strong>, <strong>unified visual-token perception</strong>, and <strong>autonomous agent architectures</strong>. Each item below provides its core crux in plain English with direct links to primary source papers.
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- CONTENT CONTAINER -->
                    <tr>
                        <td style="padding: 10px 34px 28px 34px; background-color: #fafafa;">
                            
                            <!-- CARDS INJECTION -->
                            {all_cards}

                        </td>
                    </tr>

                    <!-- MONITORED SOURCES STRIP -->
                    <tr>
                        <td style="padding: 16px 34px; background-color: #ffffff; border-top: 1px solid #e4e4e7; text-align: left;">
                            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tr>
                                    <td align="left">
                                        <span style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 9.5px; font-weight: 800; color: #a1a1aa; letter-spacing: 1.5px; text-transform: uppercase; display: block; margin-bottom: 4px;">
                                            PRIMARY SOURCES CONTINUOUSLY MONITORED
                                        </span>
                                        <span style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11.5px; color: #52525b; font-weight: 600;">
                                            arXiv Daily &bull; Google DeepMind &bull; Anthropic &bull; OpenAI &bull; Meta AI &bull; MIT Tech Review
                                        </span>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- EDITORIAL COLOPHON / FOOTER -->
                    <tr>
                        <td style="padding: 26px 34px; background-color: #ffffff; border-top: 1px solid #09090b; text-align: left;">
                            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tr>
                                    <td align="left">
                                        <span style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 10px; font-weight: 800; color: #09090b; letter-spacing: 2px; text-transform: uppercase; display: block; margin-bottom: 4px;">
                                            THE AI PARADIGM // AUTONOMOUS CLOUD DISPATCH
                                        </span>
                                        <p style="margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11.5px; color: #71717a; line-height: 1.5;">
                                            Delivered to <strong style="color: #09090b;">{RECIPIENT_EMAIL}</strong> &bull; Scheduled daily at 07:30 AM IST<br>
                                            Curated for researchers and engineers. Open source &bull; Powered by GitHub Actions.
                                        </p>
                                    </td>
                                    <td align="right" style="vertical-align: middle;">
                                        <span style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 13px; font-weight: 800; color: #d4d4d8; letter-spacing: 1px;">
                                            PARADIGM.AI
                                        </span>
                                    </td>
                                </tr>
                            </table>
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
