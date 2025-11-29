from ai_chatbot import rule_based_response, get_response

print("🛒 ShopEasy AI Customer Support (Type 'bye' to exit)\n")
history = []

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ["bye", "exit", "quit"]:
        print("ShopEasy AI: Thank you for shopping with us! 😊")
        break

    # Rule-based engine
    rule_reply = rule_based_response(user_input)

    # LLM fallback if nothing matched
    reply = rule_reply if rule_reply else get_response(user_input, history[-10:])

    print("ShopEasy AI:", reply)

    # Update history
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": reply})
