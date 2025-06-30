from __future__ import annotations

from typing import List, Dict, Any
import json
from datetime import date
from hashlib import sha256

from utils.ai_client import gemini_chat

# simple cache daily
_DEAL_CACHE: dict[tuple, List[Dict[str, Any]]] = {}

SYSTEM_PROMPT = (
    "You are a helpful shopping assistant. Given a product name, return the three best places (online or Abu Dhabi local stores) to buy it cheaply but with good quality. "
    "Return ONLY valid JSON array of objects, each having merchant, item_name, price, url. "
    "If unsure of exact price, estimate reasonably."
)

def find_deals(item_name: str) -> List[Dict[str, Any]]:
    key = (item_name.lower(), date.today().isoformat())
    if key in _DEAL_CACHE:
        return _DEAL_CACHE[key]

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": item_name},
    ]
    try:
        reply = gemini_chat(messages, temperature=0.3)
        try:
            deals = json.loads(reply)
        except json.JSONDecodeError:
            start = reply.find('[')
            end = reply.rfind(']')
            deals = json.loads(reply[start:end+1])
        _DEAL_CACHE[key] = deals
        return deals
    except Exception:
        # fallback: generic google search link
        return [
            {
                "merchant": "Google Shopping",
                "item_name": item_name,
                "price": 0.0,
                "url": f"https://www.google.com/search?tbm=shop&q={item_name.replace(' ', '+')}"
            }
        ] 