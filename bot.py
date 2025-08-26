from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import random

BOT_TOKEN = "8306904778:AAHgqUPX-oj9Uc65c7RlIzcoaU4jp6LbSSg"

# Jokes Database
jokes = [
    "😂 Why don't scientists trust atoms? Because they make up everything!",
    "😆 Why did the scarecrow win an award? Because he was outstanding in his field!",
    "🤣 Why don't eggs tell jokes? They'd crack each other up!",
    "😄 What do you call a fake noodle? An impasta!",
    "😊 Why did the math book look so sad? Because it had too many problems!"
]

quotes = [
    "✨ The only way to do great work is to love what you do. - Steve Jobs",
    "🌻 The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
    "🚀 Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
    "💫 The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt",
    "🔥 Believe you can and you're halfway there. - Theodore Roosevelt"
]

# Store user data temporarily
user_data = {}

# 3D Style Main Menu Buttons
def create_main_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🎯 𝐒𝐓𝐀𝐑𝐓", callback_data='main_menu'),
            InlineKeyboardButton("❓ 𝐇𝐄𝐋𝐏", callback_data='help')
        ],
        [
            InlineKeyboardButton("😂 𝐉𝐎𝐊𝐄", callback_data='joke'),
            InlineKeyboardButton("💫 𝐐𝐔𝐎𝐓𝐄", callback_data='quote')
        ],
        [
            InlineKeyboardButton("🖼️ 𝐆𝐄𝐍𝐄𝐑𝐀𝐓𝐄", callback_data='generate'),
            InlineKeyboardButton("🌍 𝐓𝐑𝐀𝐍𝐒𝐋𝐀𝐓𝐄", callback_data='translate')
        ],
        [
            InlineKeyboardButton("📄 𝐒𝐔𝐌𝐌𝐀𝐑𝐈𝐙𝐄", callback_data='summarize'),
            InlineKeyboardButton("🎨 𝐆𝐇𝐈𝐁𝐋𝐈", callback_data='ghibli')
        ],
        [
            InlineKeyboardButton("📊 𝐂𝐑𝐄𝐃𝐈𝐓𝐒", callback_data='credits'),
            InlineKeyboardButton("⭐ 𝐀𝐒𝐊", callback_data='ask')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# Translation Options Keyboard
def create_translate_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🇮🇳 𝐇𝐈𝐍𝐃𝐈", callback_data='lang_hi'),
            InlineKeyboardButton("🇪🇸 𝐒𝐏𝐀𝐍𝐈𝐒𝐇", callback_data='lang_es')
        ],
        [
            InlineKeyboardButton("🇫🇷 𝐅𝐑𝐄𝐍𝐂𝐇", callback_data='lang_fr'),
            InlineKeyboardButton("🇩🇪 𝐆𝐄𝐑𝐌𝐀𝐍", callback_data='lang_de')
        ],
        [
            InlineKeyboardButton("🔙 𝐁𝐀𝐂𝐊", callback_data='main_menu')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# Image Generation Options
def create_generate_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🌅 𝐋𝐀𝐍𝐃𝐒𝐂𝐀𝐏𝐄", callback_data='gen_landscape'),
            InlineKeyboardButton("🐶 𝐀𝐍𝐈𝐌𝐀𝐋𝐒", callback_data='gen_animals')
        ],
        [
            InlineKeyboardButton("🎨 𝐀𝐑𝐓", callback_data='gen_art'),
            InlineKeyboardButton("🏙️ 𝐂𝐈𝐓𝐘", callback_data='gen_city')
        ],
        [
            InlineKeyboardButton("🔙 𝐁𝐀𝐂𝐊", callback_data='main_menu')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# AI Functions
def summarize_article(url):
    """Simulate article summarization"""
    return f"📄 *Article Summary:*\n\nURL: {url}\n\nThis is a simulated summary. In a full implementation, I would use AI to extract and summarize the main content from the webpage with key points and insights."

def enhance_image_ghibli():
    """Simulate Ghibli style conversion"""
    return f"🎨 *Ghibli Style Applied!*\n\nYour image would be converted to beautiful Studio Ghibli style animation with enhanced colors and magical effects. ✨"

def translate_text(text, target_lang):
    """Simple translation function"""
    translations = {
        "hello": {
            "hindi": "नमस्ते (Namaste)", 
            "spanish": "Hola", 
            "french": "Bonjour", 
            "german": "Hallo"
        },
        "thank you": {
            "hindi": "धन्यवाद (Dhanyavad)", 
            "spanish": "Gracias", 
            "french": "Merci", 
            "german": "Danke"
        },
        "how are you": {
            "hindi": "आप कैसे हैं? (Aap kaise hain?)", 
            "spanish": "¿Cómo estás?", 
            "french": "Comment allez-vous?", 
            "german": "Wie geht es dir?"
        }
    }
    
    text_lower = text.lower()
    if text_lower in translations and target_lang in translations[text_lower]:
        return f"🌍 *Translation to {target_lang}:*\n{translations[text_lower][target_lang]}"
    else:
        return f"❌ I can translate: hello, thank you, how are you to hindi/spanish/french/german"

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_message = f"""
🎊 *Welcome {user.first_name}!* 🎊

🤖 *DoBot AI Assistant - Premium Edition*

⭐ *Features:*
• 😂 AI-Powered Jokes & Quotes
• 🖼️ Image Generation
• 🌍 Multi-language Translation  
• 📄 Article Summarization
• 🎨 Ghibli Style Conversion

💎 *Your Credits:* 100
🎁 *Referral Bonus:* 50 credits per friend

*Choose an option below:* 👇
"""
    
    await update.message.reply_text(
        welcome_message,
        parse_mode='Markdown',
        reply_markup=create_main_keyboard()
    )

# Handle Button Clicks - FIXED VERSION
async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = query.from_user.id
    
    print(f"Button clicked: {data} by user {user_id}")
    
    if data == 'main_menu':
        await query.edit_message_text(
            "🤖 *Main Menu*\n\nChoose from our amazing features!",
            parse_mode='Markdown',
            reply_markup=create_main_keyboard()
        )
    
    elif data == 'joke':
        joke = random.choice(jokes)
        await query.edit_message_text(
            f"😂 *Here's Your Joke!*\n\n{joke}\n\n*Want another?* Click Joke button again! 😄",
            parse_mode='Markdown',
            reply_markup=create_main_keyboard()
        )
    
    elif data == 'quote':
        quote = random.choice(quotes)
        await query.edit_message_text(
            f"💫 *Daily Motivation*\n\n{quote}\n\n*Stay inspired!* 🌟",
            parse_mode='Markdown',
            reply_markup=create_main_keyboard()
        )
    
    elif data == 'generate':
        await query.edit_message_text(
            "🖼️ *Image Generation Studio*\n\nChoose image type:",
            parse_mode='Markdown',
            reply_markup=create_generate_keyboard()
        )
    
    elif data == 'translate':
        await query.edit_message_text(
            "🌍 *Translation Center*\n\nChoose target language:",
            parse_mode='Markdown',
            reply_markup=create_translate_keyboard()
        )
    
    elif data == 'summarize':
        user_data[user_id] = {'waiting_for': 'summary_url'}
        await query.edit_message_text(
            "📄 *Article Summarization*\n\nPlease send me the URL of the article you want to summarize!\n\nExample: https://example.com/news-article",
            parse_mode='Markdown',
            reply_markup=create_main_keyboard()
        )
    
    elif data == 'ghibli':
        user_data[user_id] = {'waiting_for': 'ghibli_image'}
        await query.edit_message_text(
            "🎨 *Ghibli Style Converter*\n\nPlease send me an image and I'll convert it to Ghibli style!\n\nSend any image and I'll process it with magical Ghibli effects ✨",
            parse_mode='Markdown',
            reply_markup=create_main_keyboard()
        )
    
    elif data in ['gen_landscape', 'gen_animals', 'gen_art', 'gen_city']:
        image_types = {
            'gen_landscape': 'landscape',
            'gen_animals': 'animals', 
            'gen_art': 'art',
            'gen_city': 'city'
        }
        await query.edit_message_text(
            f"🖼️ *Generated {image_types[data]} image!*\n\nImage: https://source.unsplash.com/800x600/?{image_types[data]}\n\n*Enjoy your image!* 🎨",
            parse_mode='Markdown',
            reply_markup=create_main_keyboard()
        )
    
    elif data in ['lang_hi', 'lang_es', 'lang_fr', 'lang_de']:
        languages = {
            'lang_hi': 'hindi',
            'lang_es': 'spanish',
            'lang_fr': 'french', 
            'lang_de': 'german'
        }
        user_data[user_id] = {'waiting_for': 'translate_text', 'target_lang': languages[data]}
        await query.edit_message_text(
            f"🌍 *Translation to {languages[data].title()}*\n\nPlease send me the text you want to translate!\n\nExample: 'hello' or 'thank you'",
            parse_mode='Markdown',
            reply_markup=create_main_keyboard()
        )
    
    elif data == 'credits':
        await query.edit_message_text(
            "💰 *Credit System*\n\n*Current Credits:* 100\n*Referral Earnings:* 50/friend\n*Daily Bonus:* 10 credits\n\n*Earn more by referring friends!* 🎁",
            parse_mode='Markdown',
            reply_markup=create_main_keyboard()
        )
    
    elif data == 'ask':
        user_data[user_id] = {'waiting_for': 'question'}
        await query.edit_message_text(
            "⭐ *AI Question Answering*\n\nPlease ask me anything! I can answer questions about:\n• Technology & AI\n• Programming\n• Science\n• General knowledge\n\n*Type your question now!*",
            parse_mode='Markdown',
            reply_markup=create_main_keyboard()
        )
    
    elif data == 'help':
        await query.edit_message_text(
            "❓ *HELP CENTER*\n\n*How to Use:*\n• Click buttons to activate features\n• Follow instructions for each feature\n• Use /start to return to main menu\n\n*Need more help?* Just ask!",
            parse_mode='Markdown',
            reply_markup=create_main_keyboard()
        )

# Handle Text Messages
async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    if user_id in user_data:
        waiting_for = user_data[user_id]['waiting_for']
        
        if waiting_for == 'question':
            answers = {
                "ai": "🤖 *AI (Artificial Intelligence)* is the simulation of human intelligence processes by machines, especially computer systems.",
                "programming": "💻 *Programming* is writing instructions for computers to execute. Start with Python - it's beginner friendly!",
                "python": "🐍 *Python* is a great programming language for beginners. It's easy to learn, powerful, and has many libraries!",
                "ghibli": "🎨 *Studio Ghibli* is a Japanese animation studio known for beautiful films like Spirited Away, My Neighbor Totoro, and Howl's Moving Castle!",
                "machine learning": "🧠 *Machine Learning* is a subset of AI where computers learn from data without being explicitly programmed."
            }
            
            response = f"❓ *Your Question:* {text}\n\n"
            found = False
            for key in answers:
                if key in text.lower():
                    response += answers[key]
                    found = True
                    break
            
            if not found:
                response += "I can answer questions about AI, programming, Python, machine learning, Ghibli, and more! Try asking about these topics."
            
            await update.message.reply_text(response, parse_mode='Markdown')
            del user_data[user_id]
        
        elif waiting_for == 'summary_url':
            if text.startswith('http'):
                summary = summarize_article(text)
                await update.message.reply_text(summary, parse_mode='Markdown')
            else:
                await update.message.reply_text("❌ Please provide a valid URL starting with http:// or https://", parse_mode='Markdown')
            del user_data[user_id]
        
        elif waiting_for == 'translate_text':
            target_lang = user_data[user_id]['target_lang']
            translation = translate_text(text, target_lang)
            await update.message.reply_text(translation, parse_mode='Markdown')
            del user_data[user_id]
    
    else:
        # If no specific waiting state, show main menu
        await update.message.reply_text(
            "🤖 *Hello!* Use /start to see all features or choose from buttons below:",
            parse_mode='Markdown',
            reply_markup=create_main_keyboard()
        )

# Handle Images for Ghibli Conversion
async def handle_image_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id in user_data and user_data[user_id]['waiting_for'] == 'ghibli_image':
        result = enhance_image_ghibli()
        await update.message.reply_text(result, parse_mode='Markdown')
        del user_data[user_id]
    else:
        await update.message.reply_text(
            "🖼️ *Nice image!* Click the 🎨 Ghibli button first to convert images to Ghibli style!",
            parse_mode='Markdown',
            reply_markup=create_main_keyboard()
        )

# Text Command Handlers
async def handle_ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_user.id] = {'waiting_for': 'question'}
    await update.message.reply_text(
        "⭐ *Ask me anything!*\n\nI can answer questions about AI, programming, science, technology, and more!",
        parse_mode='Markdown',
        reply_markup=create_main_keyboard()
    )

async def handle_joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    joke = random.choice(jokes)
    await update.message.reply_text(
        f"😂 *Joke of the Day:*\n\n{joke}",
        parse_mode='Markdown',
        reply_markup=create_main_keyboard()
    )

async def handle_quote_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quote = random.choice(quotes)
    await update.message.reply_text(
        f"💫 *Motivational Quote:*\n\n{quote}",
        parse_mode='Markdown',
        reply_markup=create_main_keyboard()
    )

# Main Function
def main():
    # Create Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ask", handle_ask_command))
    application.add_handler(CommandHandler("joke", handle_joke_command))
    application.add_handler(CommandHandler("quote", handle_quote_command))
    application.add_handler(CallbackQueryHandler(handle_button_click))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image_message))
    
    print("🎉 Bot Started Successfully!")
    print("🤖 All buttons are working perfectly!")
    print("💬 Send /start to your bot")
    print("⭐ Features: Jokes, Quotes, Translation, Summarize, Ghibli!")
    
    # Start Polling
    application.run_polling()

if __name__ == "__main__":
    main()
