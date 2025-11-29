from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


with open("data/orders.json") as f:
    ORDERS = json.load(f)
with open("data/products.json") as f:
    PRODUCTS = json.load(f)
with open("data/faq.json") as f:
    FAQS = json.load(f)

def get_response(user_input: str, chat_history: list = None) -> str:
    if chat_history is None:
        chat_history = []

    # Build few-shot examples + data summary for the model
    system_prompt = f"""You are ShopEasy AI, a precise and friendly e-commerce support bot.

IMPORTANT RULES:
- First check if the user is asking about an order status → look for "ORD" followed by 4 digits.
- First check FAQs (exact or very close match).
- First check if they mention a product ID or ask for recommendations.
- ONLY answer using the data below. NEVER invent information.
- Keep replies short and friendly.
- If you are not 100% sure, say "Let me check that for you" and use the data.

FAQ database (answer exactly these when matched):
{json.dumps(FAQS, indent=2)}

Available orders (only answer for these order IDs):
{json.dumps([o["order_id"] + " → " + o["status"] for o in ORDERS], indent=2)}

Available products:
{json.dumps({p["product_id"]: f"{p['name']} (${p['price']}) - {p['category']}" for p in PRODUCTS}, indent=2)}

Examples:
User: what's my order status ORD1001
Assistant: Order ORD1001 (alice@example.com)
Status: Shipped, expected 2 days
Product ID: P001 → Wireless Mouse (Electronics) — $25.99

User: return policy
Assistant: You can return products within 30 days of delivery. Visit our Returns page for details.

User: recommend products
Assistant: Here are some popular items:
- Wireless Mouse — $25.99
- Bluetooth Headphones — $49.99
- Smart Watch — $89.99

Now answer the user.
"""

    messages = [{"role": "system", "content": system_prompt}] + chat_history + [{"role": "user", "content": user_input}]

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "max_tokens": 250,
        "temperature": 0.2,   
        "top_p": 0.95
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
        return f"Sorry, I'm having technical issues right now. Error: {str(e)}"