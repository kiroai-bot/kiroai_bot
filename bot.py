import requests
import sqlite3
import time
import random
import secrets

# Bot Token
BOT_TOKEN = "8306904778:AAHgqUPX-oj9Uc65c7RlIzcoaU4jp6LbSSg"

# Database setup
def init_db():
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        credits INTEGER DEFAULT 100,
        referral_code TEXT,
        join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Usage table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usage_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        feature TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        credit_cost INTEGER
    )
    ''')
    
    conn.commit()
    conn.close()

# Get user credits
def get_user_credits(user_id):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT credits FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 100

# Update user credits
def update_user_credits(user_id, credit_change):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET credits = credits + ? WHERE user_id = ?", (credit_change, user_id))
    conn.commit()
    conn.close()

# Generate referral code
def generate_referral_code(user_id):
    code = secrets.token_urlsafe(6)
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET referral_code = ? WHERE user_id = ?", (code, user_id))
    conn.commit()
    conn.close()
    
    return code

# Telegram functions
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except:
        return False

def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {"timeout": 25, "offset": offset}
    
    try:
        response = requests.get(url, params=params, timeout=15)
        return response.json()
    except:
        return {"result": []}

# AI Functions
def answer_question(question):
    answers = {
        "hello": "👋 Hello! How can I help you today?",
        "hi": "👋 Hi there! Nice to meet you!",
        "how are you": "I'm doing great! Ready to assist you! 😊",
        "what is ai": "AI is Artificial Intelligence - computer systems that can think and learn!",
        "what is your name": "I'm your friendly AI assistant bot! 🤖",
        "time": f"🕒 Current time: {time.strftime('%H:%M:%S')}",
        "date": f"📅 Today's date: {time.strftime('%Y-%m-%d')}",
        "weather": "🌤️ I'd need your location to check weather accurately",
        "thank you": "You're welcome! 😊",
        "thanks": "Anytime! 👍"
    }
    
    question_lower = question.lower().strip()
    for key in answers:
        if key in question_lower:
            return answers[key]
    
    return f"🤖 I received: '{question}'\n\nI can answer questions about AI, technology, time, dates, and more!"

def generate_image(prompt):
    try:
        search_query = requests.utils.quote(prompt)
        return f"https://source.unsplash.com/800x600/?{search_query}"
    except:
        return None

def translate_text(text, target_lang):
    translations = {
        "hello": {
            "hindi": "नमस्ते", "spanish": "Hola", "french": "Bonjour",
            "german": "Hallo", "japanese": "こんにちは"
        },
        "thank you": {
            "hindi": "धन्यवाद", "spanish": "Gracias", "french": "Merci",
            "german": "Danke", "japanese": "ありがとう"
        },
        "how are you": {
            "hindi": "आप कैसे हैं", "spanish": "¿Cómo estás?", "french": "Comment allez-vous?",
            "german": "Wie geht es dir?", "japanese": "お元気ですか？"
        }
    }
    
    text_lower = text.lower().strip()
    target_lang = target_lang.lower()
    
    if text_lower in translations and target_lang in translations[text_lower]:
        return f"Translation to {target_lang}:\n{translations[text_lower][target_lang]}"
    else:
        return "I can translate: hello, thank you, how are you to hindi/spanish/french/german/japanese"

def summarize_article(url):
    return f"Article summary for: {url}\n\nIn a full implementation, I would summarize the web article content using AI."

# Text processing functions
def generate_joke():
    jokes = [
        "😂 Why don't scientists trust atoms? Because they make up everything!",
        "😆 Why did the scarecrow win an award? Because he was outstanding in his field!",
        "🤣 Why don't eggs tell jokes? They'd crack each other up!",
        "😄 What do you call a fake noodle? An impasta!",
        "😊 Why did the math book look so sad? Because it had too many problems!",
        "💻 Why do programmers prefer dark mode? Because light attracts bugs!",
        "🚀 Why did the developer go broke? Because he used up all his cache!"
    ]
    return random.choice(jokes)

def generate_quote():
    quotes = [
        "✨ The only way to do great work is to love what you do. - Steve Jobs",
        "🌻 The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
        "🚀 Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
        "💫 The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt",
        "🔥 Believe you can and you're halfway there. - Theodore Roosevelt"
    ]
    return random.choice(quotes)

# Credit costs
CREDIT_COSTS = {
    "question": 2,
    "image": 5,
    "translation": 3,
    "summary": 4,
    "joke": 1,
    "quote": 1
}

# Main bot function
def main():
    init_db()
    print("🤖 Advanced AI Bot Started Successfully!")
    print("💬 Bot is now listening for messages...")
    
    last_update_id = None
    
    while True:
        try:
            updates = get_updates(last_update_id)
            
            if "result" in updates and updates["result"]:
                for update in updates["result"]:
                    last_update_id = update["update_id"] + 1
                    
                    if "message" in update:
                        message = update["message"]
                        chat_id = message["chat"]["id"]
                        text = message.get("text", "")
                        user_id = message["from"]["id"]
                        username = message["from"].get("username", "User")
                        
                        print(f"📩 Received: '{text}' from {username}")
                        
                        # Handle /start command
                        if text.startswith("/start"):
                            # Add user to database
                            conn = sqlite3.connect('bot_data.db')
                            cursor = conn.cursor()
                            cursor.execute(
                                "INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
                                (user_id, username)
                            )
                            conn.commit()
                            conn.close()
                            
                            # Generate referral code
                            ref_code = generate_referral_code(user_id)
                            credits = get_user_credits(user_id)
                            
                            welcome_msg = f"""
👋 Welcome to Advanced AI Bot!

🤖 I can help you with:
• Answering questions (/ask)
• Generating images (/generate)
• Language translation (/translate)
• Article summarization (/summarize)
• Telling jokes (/joke)
• Motivational quotes (/quote)

💎 Credits: {credits}

🔗 Your Referral Code: {ref_code}
Share with friends to earn more credits!

📋 Commands:
/help - Show all commands
/ask [question] - Ask me anything
/generate [prompt] - Create image
/translate [text] to [language]
/summarize [url] - Summarize article
/joke - Get a funny joke
/quote - Motivational quote
/credits - Check your credits

✨ Examples:
/ask What is AI?
/generate sunset
/translate hello to hindi
/joke
                            """
                            send_message(chat_id, welcome_msg)
                        
                        # Handle /help command
                        elif text.startswith("/help"):
                            help_msg = """
🤖 Advanced AI Bot - Help Menu

Available Commands:
/ask [question] - Ask any question (2 credits)
/generate [prompt] - Generate image (5 credits)
/translate [text] to [language] - Translate text (3 credits)
/summarize [url] - Summarize article (4 credits)
/joke - Get random joke (1 credit)
/quote - Motivational quote (1 credit)
/credits - Check credit balance

Examples:
/ask What is artificial intelligence?
/generate beautiful landscape
/translate thank you to spanish
/summarize https://example.com
/joke
                            """
                            send_message(chat_id, help_msg)
                        
                        # Handle /credits command
                        elif text.startswith("/credits"):
                            credits = get_user_credits(user_id)
                            send_message(chat_id, f"💰 Your Credits: {credits}")
                        
                        # Handle /ask command
                        elif text.startswith("/ask"):
                            credits = get_user_credits(user_id)
                            if credits >= CREDIT_COSTS["question"]:
                                question = text[4:].strip()
                                if question:
                                    answer = answer_question(question)
                                    send_message(chat_id, answer)
                                    update_user_credits(user_id, -CREDIT_COSTS["question"])
                                else:
                                    send_message(chat_id, "Please provide a question after /ask")
                            else:
                                send_message(chat_id, f"Not enough credits. You need {CREDIT_COSTS['question']} credits.")
                        
                        # Handle /generate command
                        elif text.startswith("/generate"):
                            credits = get_user_credits(user_id)
                            if credits >= CREDIT_COSTS["image"]:
                                prompt = text[10:].strip()
                                if prompt:
                                    image_url = generate_image(prompt)
                                    if image_url:
                                        send_message(chat_id, f"🖼️ Generated Image for: {prompt}\n\n{image_url}")
                                        update_user_credits(user_id, -CREDIT_COSTS["image"])
                                    else:
                                        send_message(chat_id, "Error generating image")
                                else:
                                    send_message(chat_id, "Please provide a prompt after /generate")
                            else:
                                send_message(chat_id, f"Not enough credits. You need {CREDIT_COSTS['image']} credits.")
                        
                        # Handle /translate command
                        elif text.startswith("/translate"):
                            credits = get_user_credits(user_id)
                            if credits >= CREDIT_COSTS["translation"]:
                                parts = text.split()
                                if len(parts) >= 4 and parts[-2] == "to":
                                    text_to_translate = " ".join(parts[1:-2])
                                    target_lang = parts[-1].lower()
                                    
                                    if text_to_translate:
                                        translation = translate_text(text_to_translate, target_lang)
                                        send_message(chat_id, translation)
                                        update_user_credits(user_id, -CREDIT_COSTS["translation"])
                                    else:
                                        send_message(chat_id, "Please provide text to translate")
                                else:
                                    send_message(chat_id, "Format: /translate [text] to [language]")
                            else:
                                send_message(chat_id, f"Not enough credits. You need {CREDIT_COSTS['translation']} credits.")
                        
                        # Handle /summarize command
                        elif text.startswith("/summarize"):
                            credits = get_user_credits(user_id)
                            if credits >= CREDIT_COSTS["summary"]:
                                url = text[10:].strip()
                                if url:
                                    summary = summarize_article(url)
                                    send_message(chat_id, summary)
                                    update_user_credits(user_id, -CREDIT_COSTS["summary"])
                                else:
                                    send_message(chat_id, "Please provide a URL after /summarize")
                            else:
                                send_message(chat_id, f"Not enough credits. You need {CREDIT_COSTS['summary']} credits.")
                        
                        # Handle /joke command
                        elif text.startswith("/joke"):
                            credits = get_user_credits(user_id)
                            if credits >= CREDIT_COSTS["joke"]:
                                joke = generate_joke()
                                send_message(chat_id, joke)
                                update_user_credits(user_id, -CREDIT_COSTS["joke"])
                            else:
                                send_message(chat_id, f"Not enough credits. You need {CREDIT_COSTS['joke']} credit.")
                        
                        # Handle /quote command
                        elif text.startswith("/quote"):
                            credits = get_user_credits(user_id)
                            if credits >= CREDIT_COSTS["quote"]:
                                quote = generate_quote()
                                send_message(chat_id, quote)
                                update_user_credits(user_id, -CREDIT_COSTS["quote"])
                            else:
                                send_message(chat_id, f"Not enough credits. You need {CREDIT_COSTS['quote']} credit.")
            
            time.sleep(2)
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(3)

if __name__ == "__main__":
    main()
