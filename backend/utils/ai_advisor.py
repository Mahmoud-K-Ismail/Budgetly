from __future__ import annotations
import logging, traceback

"""AI-driven advisor that consults Gemini to analyse spending and planned purchases."""

from typing import List, Dict, Any
import json
from datetime import date
from hashlib import sha256

from models import User, Expense, PlannedPurchase
from utils.ai_client import gemini_chat


SYSTEM_PROMPT = (
    "You are Budgetly, a frugal financial advisor helping NYU Abu Dhabi students reach their savings goal. "
    "You receive the user's monthly stipend, savings goal, recent discretionary expenses, and list of planned purchases. "
    "Return ONLY valid JSON with two top-level keys: cuts (list) and next_purchases (list).\n\n"
    "cuts: array of objects {expense_id:int, reason:str, amount_saved:float}. Include at most 5 items that should be reduced or cut.\n"
    "next_purchases: array of objects {id:int, verdict:str, suggestion:str, score:int}.\n"
    "verdict must be one of: 'buy_now', 'postpone', 'cancel'. score is 0-100 where 100 = essential."
)


# ---------------------------------------------------------------------------
# Simple in-memory cache to avoid excessive LLM calls. Resets on backend restart.
# Key: (user_id, day_str, purchases_signature)
# Value: advice dict
# ---------------------------------------------------------------------------

_ADVICE_CACHE: dict[tuple, Dict[str, Any]] = {}


def _summarise_expenses(expenses: List[Expense]) -> List[Dict[str, Any]]:
    """Return a lightweight list to send to the LLM (max 10 biggest discretionary)."""
    # Sort by amount desc
    top_exp = sorted(expenses, key=lambda e: e.amount, reverse=True)[:10]
    return [
        {
            "id": e.id,
            "amount": e.amount,
            "category": e.category,
            "description": e.description or "",
            "date": str(e.expense_date),
        }
        for e in top_exp
    ]


def _serialise_purchases(plans: List[PlannedPurchase]) -> List[Dict[str, Any]]:
    return [
        {
            "id": p.id,
            "item_name": p.item_name,
            "expected_price": p.expected_price,
            "priority": p.priority,
            "desired_date": str(p.desired_date),
        }
        for p in plans
    ]


def generate_advice(user: User, expenses: List[Expense], planned_purchases: List[PlannedPurchase]) -> Dict[str, Any]:
    """Return structured advice using Gemini; fallback to heuristics on error."""
    user_profile = {
        "stipend": user.stipend,
        "savings_goal": user.savings_goal,
    }

    # create cache key
    today_str = date.today().isoformat()
    sig_src = json.dumps(_serialise_purchases(planned_purchases), sort_keys=True)
    purchases_sig = sha256(sig_src.encode()).hexdigest()
    cache_key = (user.id, today_str, purchases_sig)

    if cache_key in _ADVICE_CACHE:
        return _ADVICE_CACHE[cache_key]

    payload = {
        "user": user_profile,
        "recent_expenses": _summarise_expenses(expenses),
        "planned_purchases": _serialise_purchases(planned_purchases),
    }

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": json.dumps(payload)},
    ]

    try:
        reply = gemini_chat(messages, temperature=0.2)
        # Gemini may prepend annotations; try strict parse then fallback to extracting first JSON block.
        try:
            data = json.loads(reply)
        except json.JSONDecodeError:
            start = reply.find('{')
            end = reply.rfind('}')
            if start != -1 and end != -1 and start < end:
                try:
                    data = json.loads(reply[start:end+1])
                except Exception:
                    raise
            else:
                raise
        # basic structure check
        if not isinstance(data, dict):
            raise ValueError("Expected dict")
        data.setdefault("cuts", [])
        data.setdefault("next_purchases", [])
        _ADVICE_CACHE[cache_key] = data
        return data
    except Exception as e:  # pragma: no cover – fallback when LLM fails
        logging.error("Gemini error:\n%s", traceback.format_exc())
        # naive fallback: mark high-priority plans as buy_now else postpone
        fallback_next = []
        for p in planned_purchases:
            verdict = "buy_now" if p.priority == "high" else "postpone"
            fallback_next.append({
                "id": p.id,
                "verdict": verdict,
                "suggestion": "AI unavailable, simple heuristic applied.",
                "score": 80 if verdict == "buy_now" else 40,
            })
        return {"cuts": [], "next_purchases": fallback_next} 