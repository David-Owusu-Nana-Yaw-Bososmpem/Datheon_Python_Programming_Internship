#!/usr/bin/env python3
"""
Rule-based Customer Support Chatbot
-----------------------------------
- Loads FAQs and greetings from sample_faq.json
- Normalizes user input (lowercase, strip, simple cleaning)
- Matches intents via keywords + regular expressions
- Supports multi-intent awareness and graceful fallbacks
- Clean exit on 'bye', 'exit', 'quit' (and common variants)
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

FAQ_PATH = Path(__file__).parent / "sample_faq.json"
# Fallback path if the script is run from elsewhere
if not FAQ_PATH.exists():
    FAQ_PATH = Path("/home/workdir/attachments/sample_faq.json")


# ---------------------------------------------------------------------------
# Data Loading
# ---------------------------------------------------------------------------

def load_faq_data(path: Path) -> Dict:
    """Load greetings and FAQs from JSON. Raise clear error if missing."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"[Error] FAQ file not found at: {path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"[Error] Invalid JSON in {path}: {e}")
        sys.exit(1)

    if "greetings" not in data or "faqs" not in data:
        print("[Error] JSON must contain 'greetings' and 'faqs' keys.")
        sys.exit(1)

    return data


# ---------------------------------------------------------------------------
# Input Normalization
# ---------------------------------------------------------------------------

def normalize(text: str) -> str:
    """Lowercase, strip, collapse whitespace, remove trailing punctuation."""
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[?!.,;:]+$", "", text)  # trailing punctuation
    return text


# ---------------------------------------------------------------------------
# Intent Matching
# ---------------------------------------------------------------------------

def is_greeting(text: str, greetings: List[str]) -> bool:
    """Check if the input is a pure greeting."""
    # Exact match or starts with a greeting word/phrase
    for g in greetings:
        if text == g or text.startswith(g + " ") or text.endswith(" " + g):
            return True
    # Common short forms
    if re.fullmatch(r"(hi|hello|hey|hola|yo)(\s+there)?", text):
        return True
    return False


def is_exit(text: str) -> bool:
    """Detect clean exit commands."""
    exit_patterns = [
        r"\b(bye|goodbye|good\s*bye|see\s*you|farewell)\b",
        r"\b(exit|quit|stop|end|close)\b",
        r"^(bye|exit|quit)$",
    ]
    for pat in exit_patterns:
        if re.search(pat, text, re.IGNORECASE):
            return True
    return False


def match_faq(text: str, faqs: List[Dict]) -> Optional[Tuple[str, str]]:
    """
    Match user input against FAQ questions using keyword / regex heuristics.
    Returns (question, answer) of the best match, or None.
    """
    # Pre-defined keyword sets + regex patterns for each FAQ
    # Order matters: more specific patterns first
    patterns = [
        # Hours of operation
        {
            "keywords": ["hour", "hours", "time", "open", "close", "operation",
                         "timing", "schedule", "when are you", "working hours"],
            "regex": [
                r"\b(hours?|timing|schedule|open|close)\b",
                r"(what|when).*(hours?|open|close|operate)",
                r"hours?\s+of\s+operation",
            ],
            "index": 0,
        },
        # Submit internship project
        {
            "keywords": ["submit", "project", "internship", "github", "repository",
                         "repo", "upload", "how do i submit", "submission"],
            "regex": [
                r"\b(submit|upload|send).*(project|internship|work|repo|github)",
                r"(how|where).*(submit|upload).*(project|internship)",
                r"github\s+(repo|repository|link)",
            ],
            "index": 1,
        },
        # Certificate
        {
            "keywords": ["certificate", "cert", "certification", "receive",
                         "when will i get", "completion", "award"],
            "regex": [
                r"\b(certificate|certification|cert)\b",
                r"(when|how long).*(certificate|cert|receive|get)",
                r"(receive|get|issue).*(certificate|cert)",
            ],
            "index": 2,
        },
    ]

    text_lower = text.lower()
    best_score = 0
    best_idx = None

    for p in patterns:
        score = 0
        # Keyword hits
        for kw in p["keywords"]:
            if kw in text_lower:
                score += 2
        # Regex hits
        for rx in p["regex"]:
            if re.search(rx, text_lower, re.IGNORECASE):
                score += 3
        if score > best_score:
            best_score = score
            best_idx = p["index"]

    # Require a minimum confidence
    if best_score >= 2 and best_idx is not None and best_idx < len(faqs):
        faq = faqs[best_idx]
        return faq["question"], faq["answer"]

    return None


def detect_intent(text: str, data: Dict) -> str:
    """
    High-level intent classifier.
    Returns one of: 'greeting', 'exit', 'faq', 'fallback'
    """
    if is_exit(text):
        return "exit"
    if is_greeting(text, data["greetings"]):
        return "greeting"
    if match_faq(text, data["faqs"]) is not None:
        return "faq"
    return "fallback"


# ---------------------------------------------------------------------------
# Response Generation
# ---------------------------------------------------------------------------

def get_response(text: str, data: Dict) -> Tuple[str, bool]:
    """
    Produce a response string and a flag indicating whether the bot should exit.
    """
    intent = detect_intent(text, data)

    if intent == "exit":
        return "Goodbye! Have a great day. Feel free to come back if you have more questions.", True

    if intent == "greeting":
        return (
            "Hello! Welcome to our support assistant. "
            "I can help you with:\n"
            "  • Our hours of operation\n"
            "  • How to submit your internship project\n"
            "  • When you will receive your certificate\n"
            "How can I assist you today?"
        ), False

    if intent == "faq":
        match = match_faq(text, data["faqs"])
        if match:
            question, answer = match
            return f"{answer}", False

    # Fallback – helpful and non-repetitive
    return (
        "I'm not sure I understand that completely. "
        "I can currently help with:\n"
        "  • Hours of operation\n"
        "  • Submitting your internship project\n"
        "  • Certificate issuance timeline\n"
        "Could you rephrase your question or ask about one of the topics above?"
    ), False


# ---------------------------------------------------------------------------
# Main Conversation Loop
# ---------------------------------------------------------------------------

def print_banner():
    print("=" * 60)
    print("  Customer Support Chatbot")
    print("  Type your question or 'bye' / 'exit' / 'quit' to leave")
    print("=" * 60)
    print()


def main():
    data = load_faq_data(FAQ_PATH)
    print_banner()

    # Opening greeting
    print("Bot: Hello! How can I help you today?\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBot: Goodbye! (session interrupted)")
            break

        if not user_input:
            print("Bot: Please type a question or 'bye' to exit.\n")
            continue

        normalized = normalize(user_input)
        response, should_exit = get_response(normalized, data)

        print(f"Bot: {response}\n")

        if should_exit:
            break


if __name__ == "__main__":
    main()
