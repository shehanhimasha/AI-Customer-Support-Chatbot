# ShopEasy AI – E-Commerce Customer Support Chatbot  

AI-powered customer support chatbot for an e-commerce platform  
Built with Python, Groq (Llama 3.3 70B), and a hybrid rule-based + LLM architecture.

## Features
- Instant & 100% accurate **order status** lookup (`ORD1001`, etc.)
- Exact + fuzzy matching for **FAQs** (return policy, shipping time, etc.)
- Smart **product recommendations** with name, price, and category
- Natural language understanding (“track my order”, “reccomend me products”, “shipping tim”)
- Zero hallucination on critical data (all answers come from JSON datasets)
- Ultra-fast responses (Groq inference < 300 ms)
- Clean console app + ready for Streamlit web deployment

## Tech Stack
- **Backend**: Python 3.11+
- **LLM**: Groq Cloud – `llama-3.3-70b-versatile` (fastest open LLM)
- **Data**: Synthetic datasets (`orders.json`, `products.json`, `faq.json`)
- **Libraries**: `requests`, `python-dotenv`, `difflib`, `re`, `streamlit` (optional)

