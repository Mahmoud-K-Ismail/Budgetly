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
    "For price: use a specific number (e.g., 250.0) if you can estimate it reasonably. If the price varies significantly or you cannot estimate, use the string 'Price varies - contact merchant' instead of a number. "
    "Be specific with merchant names and provide real URLs when possible."
)

def find_deals(item_name: str) -> List[Dict[str, Any]]:
    key = (item_name.lower(), date.today().isoformat())
    if key in _DEAL_CACHE:
        return _DEAL_CACHE[key]

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Find the best deals for: {item_name}"},
    ]
    try:
        reply = gemini_chat(messages, temperature=0.3)
        try:
            deals = json.loads(reply)
        except json.JSONDecodeError:
            # Try to extract JSON from response
            start = reply.find('[')
            end = reply.rfind(']')
            if start != -1 and end != -1:
                deals = json.loads(reply[start:end+1])
            else:
                raise ValueError("No valid JSON array found in response")
        
        # Validate and clean the deals data
        cleaned_deals = []
        for deal in deals:
            if isinstance(deal, dict) and all(key in deal for key in ['merchant', 'item_name', 'price', 'url']):
                # Handle price field - ensure it's either a number or a descriptive string
                if isinstance(deal['price'], str) and any(word in deal['price'].lower() for word in ['varies', 'depending', 'contact', 'call']):
                    deal['price'] = "Price varies - contact merchant"
                elif isinstance(deal['price'], str):
                    try:
                        # Try to extract a number from the string
                        import re
                        price_match = re.search(r'[\d,]+\.?\d*', deal['price'].replace(',', ''))
                        if price_match:
                            deal['price'] = float(price_match.group())
                        else:
                            deal['price'] = "Price varies - contact merchant"
                    except:
                        deal['price'] = "Price varies - contact merchant"
                
                cleaned_deals.append(deal)
        
        if not cleaned_deals:
            raise ValueError("No valid deals found in AI response")
            
        _DEAL_CACHE[key] = cleaned_deals
        return cleaned_deals
        
    except Exception as e:
        print(f"Error finding deals for {item_name}: {e}")
        # fallback: generic google search link
        return [
            {
                "merchant": "Google Shopping",
                "item_name": item_name,
                "price": "Price varies - contact merchant",
                "url": f"https://www.google.com/search?tbm=shop&q={item_name.replace(' ', '+')}"
            }
        ] 