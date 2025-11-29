import json
import re
from difflib import get_close_matches
from ai_chatbot import get_response  

# ==================== LOAD DATA ====================
with open("data/orders.json", encoding="utf-8") as f:
    orders = json.load(f)

with open("data/products.json", encoding="utf-8") as f:
    products = json.load(f)

with open("data/faq.json", encoding="utf-8") as f:
    faqs = json.load(f)

# ==================== HELPER FUNCTIONS ====================
def check_faq(user_input: str):
    key = user_input.lower().strip()
    if key in faqs:
        return faqs[key]

    # Fuzzy match
    matches = get_close_matches(key, faqs.keys(), n=1, cutoff=0.6)
    if matches:
        return faqs[matches[0]]
    return None


def get_order_status(order_id: str):
    for order in orders:
        if order["order_id"] == order_id:
            # Find product name
            prod = next((p for p in products if p["product_id"] == order["product_id"]), None)
            prod_name = f" — {prod['name']} (${prod['price']})" if prod else ""
            return f"""Order {order_id}
Status → {order['status']}
Item → {order["product_id"]}{prod_name}
Email → {order['email']}"""
    return "Sorry, I couldn't find that order."


def get_product_info():
    top_products = products[:5]  
    lines = [f"• {p['name']} ({p['category']}) — ${p['price']}" for p in top_products]
    return "Here are some of our most popular products right now:\n\n" + "\n".join(lines)


# ==================== CHAT LOOP ====================
print("ShopEasy Customer Support!")
print("Type 'bye' to exit.\n")

history = []  

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ["bye", "exit", "quit", "goodbye"]:
        print("ShopEasy AI: Thank you for shopping with us! Have a great day!")
        break

    reply = None

    # 1. FAQ first
    faq_reply = check_faq(user_input)
    if faq_reply:
        reply = faq_reply

    # 2. Order ID detection
    order_match = re.search(r"\bORD\d{4}\b", user_input.upper())
    if order_match:
        reply = get_order_status(order_match.group())

    # 3. Product recommendations
    if not reply and any(word in user_input.lower() for word in ["recommend", "suggest", "product", "show me"]):
        reply = get_product_info()

    # 4. LLM fallback only when nothing else matched
    if reply is None:
        reply = get_response(user_input, history[-10:])  

    print(f"ShopEasy AI: {reply}\n")

    # Update history
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": reply})