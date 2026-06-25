import telebot
import feedparser
import threading
import time

# Bot token
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
bot = telebot.TeleBot(BOT_TOKEN)

# Store user settings
user_keywords = {}
user_feeds = {}
sent_articles = {}
user_state = {}
user_lang = {}

# All texts in two languages
TEXTS = {
    "ru": {
        "choose_lang": "👋 Привет! Выбери язык:",
        "welcome": "👋 Привет! Я мониторю новостные сайты и присылаю статьи по ключевым словам.\n\nКак начать:\n1. Добавь источники новостей (RSS)\n2. Добавь ключевые слова\n3. Нажми ▶️ Запустить мониторинг\n4. Получай нужные новости автоматически!",
        "sources_btn": "📡 Источники",
        "keywords_btn": "🔑 Ключевые слова",
        "settings_btn": "📋 Мои настройки",
        "start_btn": "▶️ Запустить мониторинг",
        "stop_btn": "⏹ Остановить",
        "clear_btn": "🗑 Очистить всё",
        "lang_btn": "🌐 Язык",
        "manage_sources": "Управление источниками:",
        "add_feed_btn": "➕ Добавить свой RSS",
        "popular_btn": "⭐ Популярные источники",
        "my_sources_btn": "📋 Мои источники",
        "remove_btn": "➖ Удалить",
        "manage_keywords": "Управление ключевыми словами:",
        "add_btn": "➕ Добавить",
        "list_btn": "📋 Список слов",
        "settings_title": "📋 Твои настройки:\n\n",
        "sources_count": "📡 Источники",
        "keywords_count": "🔑 Ключевые слова",
        "empty": "• пусто",
        "no_keywords_warning": "⚠️ Сначала добавь ключевые слова!",
        "no_feeds_warning": "⚠️ Сначала добавь источники новостей!",
        "monitoring_started": "✅ Мониторинг запущен! Буду присылать новости по твоим ключевым словам.",
        "monitoring_stopped": "⏹ Мониторинг остановлен.",
        "cleared": "✅ Все настройки очищены.",
        "feed_prompt": "Введи ссылку на RSS ленту. Пример:\nhttps://techcrunch.com/feed/\n\nБольшинство новостных сайтов имеют RSS по адресу:\nсайт.com/rss или сайт.com/feed",
        "choose_source": "Выбери источник:",
        "source_added": "✅ Добавлен источник: {name}",
        "source_exists": "Этот источник уже добавлен.",
        "my_feeds": "📡 Твои источники:\n",
        "no_feeds": "Источников нет.",
        "remove_source": "Выбери источник для удаления:",
        "source_removed": "✅ Источник удалён.",
        "keyword_prompt": "Введи ключевые слова через запятую:\n\nПример: Bitcoin, крипто, ethereum",
        "no_keywords": "Ключевых слов нет.",
        "remove_keyword_msg": "Выбери слово для удаления:",
        "keyword_removed": "✅ Слово '{kw}' удалено.",
        "keywords_list": "🔑 Твои слова:\n",
        "feed_added": "✅ Источник добавлен! Найдено {count} статей.",
        "feed_exists": "Этот источник уже есть.",
        "feed_error": "❌ Не удалось загрузить RSS. Проверь ссылку.",
        "keywords_added": "✅ Добавлено: {added}\n",
        "keywords_skipped": "⚠️ Уже есть: {skipped}",
        "new_article": "🔔 Новая статья!\n🔑 Ключевое слово: {keyword}\n\n📰 {title}\n\n🔗 {url}",
        "lang_changed": "✅ Язык изменён на Русский 🇷🇺",
    },
    "en": {
        "choose_lang": "👋 Hello! Choose your language:",
        "welcome": "👋 Hello! I monitor news sites and send articles by keywords.\n\nHow to start:\n1. Add news sources (RSS)\n2. Add keywords\n3. Press ▶️ Start monitoring\n4. Get relevant news automatically!",
        "sources_btn": "📡 Sources",
        "keywords_btn": "🔑 Keywords",
        "settings_btn": "📋 My settings",
        "start_btn": "▶️ Start monitoring",
        "stop_btn": "⏹ Stop",
        "clear_btn": "🗑 Clear all",
        "lang_btn": "🌐 Language",
        "manage_sources": "Manage sources:",
        "add_feed_btn": "➕ Add RSS feed",
        "popular_btn": "⭐ Popular sources",
        "my_sources_btn": "📋 My sources",
        "remove_btn": "➖ Remove",
        "manage_keywords": "Manage keywords:",
        "add_btn": "➕ Add",
        "list_btn": "📋 List",
        "settings_title": "📋 Your settings:\n\n",
        "sources_count": "📡 Sources",
        "keywords_count": "🔑 Keywords",
        "empty": "• empty",
        "no_keywords_warning": "⚠️ Add keywords first!",
        "no_feeds_warning": "⚠️ Add news sources first!",
        "monitoring_started": "✅ Monitoring started! I'll send news matching your keywords.",
        "monitoring_stopped": "⏹ Monitoring stopped.",
        "cleared": "✅ All settings cleared.",
        "feed_prompt": "Enter RSS feed URL. Example:\nhttps://techcrunch.com/feed/\n\nMost news sites have RSS at:\nsite.com/rss or site.com/feed",
        "choose_source": "Choose a source:",
        "source_added": "✅ Source added: {name}",
        "source_exists": "This source is already added.",
        "my_feeds": "📡 Your sources:\n",
        "no_feeds": "No sources added.",
        "remove_source": "Choose source to remove:",
        "source_removed": "✅ Source removed.",
        "keyword_prompt": "Enter keywords separated by comma:\n\nExample: Bitcoin, crypto, ethereum",
        "no_keywords": "No keywords added.",
        "remove_keyword_msg": "Choose keyword to remove:",
        "keyword_removed": "✅ Keyword '{kw}' removed.",
        "keywords_list": "🔑 Your keywords:\n",
        "feed_added": "✅ Source added! Found {count} articles.",
        "feed_exists": "This source already exists.",
        "feed_error": "❌ Failed to load RSS. Check the URL.",
        "keywords_added": "✅ Added: {added}\n",
        "keywords_skipped": "⚠️ Already exist: {skipped}",
        "new_article": "🔔 New article!\n🔑 Keyword: {keyword}\n\n📰 {title}\n\n🔗 {url}",
        "lang_changed": "✅ Language changed to English 🇬🇧",
    }
}

POPULAR_FEEDS = [
    ("🌍 BBC News", "http://feeds.bbci.co.uk/news/rss.xml"),
    ("💰 CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
    ("📱 TechCrunch", "https://techcrunch.com/feed/"),
    ("📈 Reuters", "https://feeds.reuters.com/reuters/topNews"),
    ("🇺🇦 Украина", "https://www.pravda.com.ua/rss/view_news/"),
    ("⚽ ESPN", "https://www.espn.com/espn/rss/news"),
]

def t(chat_id, key, **kwargs):
    # Get text in user's language
    lang = user_lang.get(chat_id, "ru")
    text = TEXTS[lang][key]
    return text.format(**kwargs) if kwargs else text

def lang_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        telebot.types.InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
    )
    return markup

def main_menu(chat_id):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(t(chat_id, "sources_btn"), t(chat_id, "keywords_btn"))
    markup.row(t(chat_id, "settings_btn"), t(chat_id, "start_btn"))
    markup.row(t(chat_id, "stop_btn"), t(chat_id, "clear_btn"))
    markup.row(t(chat_id, "lang_btn"))
    return markup

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id,
        "👋 Привет! / Hello!\nВыбери язык / Choose language:",
        reply_markup=lang_markup()
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("lang_"))
def callback_lang(call):
    lang = call.data.replace("lang_", "")
    user_lang[call.message.chat.id] = lang
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id,
        t(call.message.chat.id, "welcome"),
        reply_markup=main_menu(call.message.chat.id)
    )

@bot.message_handler(func=lambda m: m.text in [
    "📡 Источники", "🔑 Ключевые слова", "📋 Мои настройки",
    "▶️ Запустить мониторинг", "⏹ Остановить", "🗑 Очистить всё", "🌐 Язык",
    "📡 Sources", "🔑 Keywords", "📋 My settings",
    "▶️ Start monitoring", "⏹ Stop", "🗑 Clear all", "🌐 Language"
])
def handle_buttons(message):
    chat_id = message.chat.id
    text = message.text

    if text in ["🌐 Язык", "🌐 Language"]:
        bot.send_message(chat_id, "🇷🇺 / 🇬🇧", reply_markup=lang_markup())

    elif text in ["📡 Источники", "📡 Sources"]:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton(t(chat_id, "add_feed_btn"), callback_data="add_feed"))
        markup.row(telebot.types.InlineKeyboardButton(t(chat_id, "popular_btn"), callback_data="popular_feeds"))
        markup.row(
            telebot.types.InlineKeyboardButton(t(chat_id, "my_sources_btn"), callback_data="list_feeds"),
            telebot.types.InlineKeyboardButton(t(chat_id, "remove_btn"), callback_data="remove_feed")
        )
        bot.send_message(chat_id, t(chat_id, "manage_sources"), reply_markup=markup)

    elif text in ["🔑 Ключевые слова", "🔑 Keywords"]:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton(t(chat_id, "add_btn"), callback_data="add_keyword"),
            telebot.types.InlineKeyboardButton(t(chat_id, "remove_btn"), callback_data="remove_keyword")
        )
        markup.row(telebot.types.InlineKeyboardButton(t(chat_id, "list_btn"), callback_data="list_keywords"))
        bot.send_message(chat_id, t(chat_id, "manage_keywords"), reply_markup=markup)

    elif text in ["📋 Мои настройки", "📋 My settings"]:
        keywords = user_keywords.get(chat_id, [])
        feeds = user_feeds.get(chat_id, [])
        msg = t(chat_id, "settings_title")
        msg += f"{t(chat_id, 'sources_count')} ({len(feeds)}):\n"
        msg += "\n".join([f"• {f}" for f in feeds]) if feeds else t(chat_id, "empty")
        msg += f"\n\n{t(chat_id, 'keywords_count')} ({len(keywords)}):\n"
        msg += "\n".join([f"• {k}" for k in keywords]) if keywords else t(chat_id, "empty")
        bot.send_message(chat_id, msg)

    elif text in ["▶️ Запустить мониторинг", "▶️ Start monitoring"]:
        keywords = user_keywords.get(chat_id, [])
        feeds = user_feeds.get(chat_id, [])
        if not keywords:
            bot.send_message(chat_id, t(chat_id, "no_keywords_warning"))
            return
        if not feeds:
            bot.send_message(chat_id, t(chat_id, "no_feeds_warning"))
            return
        user_state[chat_id] = "monitoring"
        if chat_id not in sent_articles:
            sent_articles[chat_id] = set()
        bot.send_message(chat_id, t(chat_id, "monitoring_started"))

    elif text in ["⏹ Остановить", "⏹ Stop"]:
        user_state[chat_id] = "stopped"
        bot.send_message(chat_id, t(chat_id, "monitoring_stopped"))

    elif text in ["🗑 Очистить всё", "🗑 Clear all"]:
        user_keywords[chat_id] = []
        user_feeds[chat_id] = []
        user_state[chat_id] = "stopped"
        sent_articles[chat_id] = set()
        bot.send_message(chat_id, t(chat_id, "cleared"))

@bot.callback_query_handler(func=lambda call: not call.data.startswith("lang_"))
def callback_handler(call):
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id)

    if call.data == "add_feed":
        user_state[chat_id] = "waiting_feed"
        bot.send_message(chat_id, t(chat_id, "feed_prompt"))

    elif call.data == "popular_feeds":
        markup = telebot.types.InlineKeyboardMarkup()
        for name, url in POPULAR_FEEDS:
            markup.row(telebot.types.InlineKeyboardButton(name, callback_data=f"add_popular_{url}"))
        bot.send_message(chat_id, t(chat_id, "choose_source"), reply_markup=markup)

    elif call.data.startswith("add_popular_"):
        url = call.data.replace("add_popular_", "")
        if chat_id not in user_feeds:
            user_feeds[chat_id] = []
        if url not in user_feeds[chat_id]:
            user_feeds[chat_id].append(url)
            name = next((n for n, u in POPULAR_FEEDS if u == url), url)
            bot.send_message(chat_id, t(chat_id, "source_added", name=name))
        else:
            bot.send_message(chat_id, t(chat_id, "source_exists"))

    elif call.data == "list_feeds":
        feeds = user_feeds.get(chat_id, [])
        if feeds:
            bot.send_message(chat_id, t(chat_id, "my_feeds") + "\n".join([f"• {f}" for f in feeds]))
        else:
            bot.send_message(chat_id, t(chat_id, "no_feeds"))

    elif call.data == "remove_feed":
        feeds = user_feeds.get(chat_id, [])
        if not feeds:
            bot.send_message(chat_id, t(chat_id, "no_feeds"))
            return
        markup = telebot.types.InlineKeyboardMarkup()
        for feed in feeds:
            short = feed[:40] + "..." if len(feed) > 40 else feed
            markup.row(telebot.types.InlineKeyboardButton(f"🗑 {short}", callback_data=f"del_feed_{feed}"))
        bot.send_message(chat_id, t(chat_id, "remove_source"), reply_markup=markup)

    elif call.data.startswith("del_feed_"):
        feed = call.data.replace("del_feed_", "")
        if chat_id in user_feeds and feed in user_feeds[chat_id]:
            user_feeds[chat_id].remove(feed)
            bot.send_message(chat_id, t(chat_id, "source_removed"))

    elif call.data == "add_keyword":
        user_state[chat_id] = "waiting_keyword"
        bot.send_message(chat_id, t(chat_id, "keyword_prompt"))

    elif call.data == "remove_keyword":
        keywords = user_keywords.get(chat_id, [])
        if not keywords:
            bot.send_message(chat_id, t(chat_id, "no_keywords"))
            return
        markup = telebot.types.InlineKeyboardMarkup()
        for kw in keywords:
            markup.row(telebot.types.InlineKeyboardButton(f"🗑 {kw}", callback_data=f"del_kw_{kw}"))
        bot.send_message(chat_id, t(chat_id, "remove_keyword_msg"), reply_markup=markup)

    elif call.data.startswith("del_kw_"):
        kw = call.data.replace("del_kw_", "")
        if chat_id in user_keywords and kw in user_keywords[chat_id]:
            user_keywords[chat_id].remove(kw)
            bot.send_message(chat_id, t(chat_id, "keyword_removed", kw=kw))

    elif call.data == "list_keywords":
        keywords = user_keywords.get(chat_id, [])
        if keywords:
            bot.send_message(chat_id, t(chat_id, "keywords_list") + "\n".join([f"• {k}" for k in keywords]))
        else:
            bot.send_message(chat_id, t(chat_id, "no_keywords"))

@bot.message_handler(func=lambda m: user_state.get(m.chat.id) in ["waiting_feed", "waiting_keyword"])
def handle_input(message):
    chat_id = message.chat.id
    state = user_state.get(chat_id)

    if state == "waiting_feed":
        url = message.text.strip()
        feed = feedparser.parse(url)
        if feed.entries:
            if chat_id not in user_feeds:
                user_feeds[chat_id] = []
            if url not in user_feeds[chat_id]:
                user_feeds[chat_id].append(url)
                bot.send_message(chat_id, t(chat_id, "feed_added", count=len(feed.entries)), reply_markup=main_menu(chat_id))
            else:
                bot.send_message(chat_id, t(chat_id, "feed_exists"))
        else:
            bot.send_message(chat_id, t(chat_id, "feed_error"))

    elif state == "waiting_keyword":
        raw = message.text.strip()
        new_keywords = [k.strip().lower() for k in raw.split(",") if k.strip()]
        if chat_id not in user_keywords:
            user_keywords[chat_id] = []
        added = []
        skipped = []
        for keyword in new_keywords:
            if keyword not in user_keywords[chat_id]:
                user_keywords[chat_id].append(keyword)
                added.append(keyword)
            else:
                skipped.append(keyword)
        result = ""
        if added:
            result += t(chat_id, "keywords_added", added=", ".join(added))
        if skipped:
            result += t(chat_id, "keywords_skipped", skipped=", ".join(skipped))
        bot.send_message(chat_id, result, reply_markup=main_menu(chat_id))

    user_state[chat_id] = None

def check_feeds():
    # Background thread — checks RSS feeds every 5 minutes
    while True:
        for chat_id, feeds in list(user_feeds.items()):
            if user_state.get(chat_id) != "monitoring":
                continue
            keywords = user_keywords.get(chat_id, [])
            if not keywords:
                continue
            if chat_id not in sent_articles:
                sent_articles[chat_id] = set()

            for feed_url in feeds:
                try:
                    feed = feedparser.parse(feed_url)
                    for entry in feed.entries[:10]:
                        url = entry.get("link", "")
                        if url in sent_articles[chat_id]:
                            continue
                        title = entry.get("title", "")
                        summary = entry.get("summary", "")
                        full_text = f"{title} {summary}".lower()

                        for keyword in keywords:
                            if keyword.lower() in full_text:
                                sent_articles[chat_id].add(url)
                                bot.send_message(chat_id,
                                    t(chat_id, "new_article",
                                      keyword=keyword,
                                      title=title,
                                      url=url)
                                )
                                break
                except Exception:
                    pass
        time.sleep(300)

# Start background monitor
threading.Thread(target=check_feeds, daemon=True).start()
print("✅ Bot started!")
bot.polling()