from dotenv import load_dotenv
import os
import requests
import json
import re
from difflib import get_close_matches

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Load orders
if os.path.exists("data/orders.json"):
    with open("data/orders.json") as f:
        ORDERS = json.load(f)
else:
    print("Warning: orders.json not found. Order tracking will not work.")
    ORDERS = []

# Load products
if os.path.exists("data/products.json"):
    with open("data/products.json") as f:
        PRODUCTS = json.load(f)
else:
    print("Warning: products.json not found. Product recommendations will not work.")
    PRODUCTS = []

# Load FAQs
if os.path.exists("data/faq.json"):
    with open("data/faq.json") as f:
        FAQS = json.load(f)
else:
    print("Warning: faq.json not found. FAQ answers will not work.")
    FAQS = {}

# ================= Rule-based helpers =================

def check_faq(user_input: str):
    key = user_input.lower().strip()
    if key in FAQS:
        return FAQS[key]
    
    # Fuzzy match
    matches = get_close_matches(key, FAQS.keys(), n=1, cutoff=0.4)
    if matches:
        return FAQS[matches[0]]
    
    return None


def get_order_status(order_id: str):
    for order in ORDERS:
        if order["order_id"].upper() == order_id.upper():
            # Find product info
            product = next((p for p in PRODUCTS if p["product_id"] == order.get("product_id")), None)
            prod_text = f" — {product['name']} (${product['price']})" if product else ""
            
            email = order.get("email", "No email available")
            status = order.get("status", "No status available")
            
            return (
                f"Order {order['order_id']} ({email})\n"
                f"Status: {status}\n"
                f"Item: {order.get('product_id', 'Unknown')}{prod_text}"
            )
    return "I couldn't find that order. Please check the ID."


def get_product_info():
    text = "Here are some recommended products:\n"
    for p in PRODUCTS:
        text += f"- {p['name']} — ${p['price']} ({p['category']})\n"
    return text


# ================= Rule-based main function =================

def rule_based_response(user_input: str):
    #FAQ match
    faq = check_faq(user_input)
    if faq:
        return faq

    # Order ID match
    order_match = re.search(r"\bORD\d{4}\b", user_input.upper())
    if order_match:
        return get_order_status(order_match.group())

    # Product recommendation
    if any(word in user_input.lower() for word in ["recommend", "suggest", "product", "show me"]):
        return get_product_info()

    return None


# ================= LLM fallback =================

def get_response(user_input: str, chat_history: list = None):
    if chat_history is None:
        chat_history = []

    system_prompt = """
You are ShopEasy AI.

RULES:
- Use ONLY the provided product, order, and FAQ data.
- Never invent new info.
- Keep replies short and friendly.
- If something isn't in the data, say: "Let me check that for you."
- Do NOT re-check order IDs, FAQs, or product matches. Python handles that before sending the query.

Your job:
- Explain things clearly
- Answer product questions
- Expand simple responses
- Chat naturally
"""

    messages = [{"role": "system", "content": system_prompt}] + chat_history + [
        {"role": "user", "content": user_input}
    ]

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "max_tokens": 250,
        "temperature": 0.3
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=15)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Technical issue: {str(e)}"
