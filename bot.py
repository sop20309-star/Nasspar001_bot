import telebot
from telebot import types
from datetime import datetime

# 💡 မဖြစ်မနေ ပြင်ဆင်ရမည့် အချက်များ
TOKEN = "9082926169:AAFOnxwX2BfC6P1XfiQFCxAJyz02oZwk3g"            # BotFather ကရတဲ့ Bot Token
CHANNEL_USERNAME = "@seriesmoviesplanet007" # ကိုယ့်ရဲ့ Telegram Channel Username
CREATOR_ID = 5188275898                    # သင့်ရဲ့ Telegram User ID (Log ပို့ရန်)

# ငွေပေးချေမှု အချက်အလက်များ
KPAY_PHONE = "09448948562"
WAVE_PHONE = "09448948562"
ACCOUNT_NAME = "Nyein Sopyay Aung"

bot = telebot.TeleBot(TOKEN)

# User ဝင်သုံးသွားတိုင်း Creator ထံ Log ပို့ပေးမည့် Function
def log_user_activity(message, action="စတင်အသုံးပြုခြင်း (/start)"):
    try:
        user = message.from_user
        name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        username = f"@{user.username}" if user.username else "Username မရှိပါ"
        user_id = user.id
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_text = (
            "🔔 **[Bot Activity Log]**\n"
            f"👤 **အမည်:** {name}\n"
            f"🔗 **Username:** {username}\n"
            f"🆔 **User ID:** `{user_id}`\n"
            f"⚡ **လုပ်ဆောင်ချက်:** {action}\n"
            f"📅 **အချိန်:** {current_time}"
        )
        bot.send_message(CREATOR_ID, log_text, parse_mode="Markdown")
    except Exception as e:
        print(f"Log Error: {e}")

# Channel Join ပြီးပြီလား စစ်ဆေးသည့် Function
def check_user_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ['creator', 'administrator', 'member']:
            return True
    except Exception as e:
        print(f"Error checking sub: {e}")
    return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    log_user_activity(message, "Bot စတင်သုံးစွဲရန် (/start) နှိပ်ခဲ့သည်")
    
    if not check_user_subscription(user_id):
        markup = types.InlineKeyboardMarkup()
        btn_channel = types.InlineKeyboardButton("📢 Channel သို့သွား၍ Join ရန်", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")
        btn_check = types.InlineKeyboardButton("🔄 Join ပြီးပါပြီ (စစ်ဆေးရန်)", callback_data="check_sub")
        markup.add(btn_channel)
        markup.add(btn_check)
        
        bot.send_message(
            message.chat.id, 
            "⚠️ **မင်္ဂလာပါ မိတ်ဆွေ...**\n\n"
            f"ဤ Bot အား အသုံးပြုရန် ကျေးဇူးပြု၍ ပထမဦးစွာ ကျွန်ုပ်တို့၏ Channel ({CHANNEL_USERNAME}) ကို Join ပေးပါရန် တောင်းဆိုအပ်ပါသည်။ Join ပြီးပါက 'Join ပြီးပါပြီ' ခလုတ်ကို နှိပ်ပါ။",
            parse_mode="Markdown",
            reply_markup=markup
        )
        return

    show_main_menu(message.chat.id)

def show_main_menu(chat_id):
    welcome_text = (
        "မင်္ဂလာပါ မိတ်ဆွေ..👋\n"
        "ကျွန်တော်ကတော့ Nasspar's bot ပဲဖြစ်ပါတယ်..🤖\n\n"
        "သင်သိလိုသော အကြောင်းအရာများအား အောက်တွင် ဖော်ပြထားသော ခလုတ်များကို နှိပ်၍ လေ့လာနိုင်ပါတယ် ခင်ဗျာ..✨\n"
        "(သို့မဟုတ်) Ashita No Joe အကြောင်းနှင့် ပတ်သက်သည်များကို စာတိုပေးပို့၍ မေးမြန်းနိုင်ပါသည် 🧠။"
    )
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("🥊 Ashita No Joe Series အကြောင်း လေ့လာရန်", callback_data="q1")
    btn2 = types.InlineKeyboardButton("💳 Ashita No Joe အတွက် ငွေပေးချေရန်", callback_data="q2")
    btn3 = types.InlineKeyboardButton("🎬 Ashita No Joe အစမ်းကြည့်ရှုရန် (Channel)", url="https://t.me/ashitanojoefreeep") 
    btn_admin = types.InlineKeyboardButton("💬 Admin ထံ တိုက်ရိုက် ဆက်သွယ်ရန်", url="https://t.me/Nazzpar")
    btn4 = types.InlineKeyboardButton("🔒 Nasspar's Premium Channel အကြောင်း", callback_data="q3")
    
    markup.add(btn1, btn2, btn3, btn_admin, btn4)
    bot.send_message(chat_id, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "check_sub":
        if check_user_subscription(call.from_user.id):
            bot.answer_callback_query(call.id, "✅ Channel ထဲသို့ ရောက်ရှိကြောင်း အတည်ပြုပြီးပါပြီ။")
            bot.delete_message(call.message.chat.id, call.message.message_id)
            show_main_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "❌ ကျေးဇူးပြု၍ Channel ကို အရင် Join ပေးပါခင်ဗျာ။", show_alert=True)
        return

    bot.answer_callback_query(call.id)
    
    if call.data == "q1":
        caption_text = """Ashita No Joe ခေါ် Tomorrow's Joe က Season အားဖြင့် ၂ ခု ထိ ထွက်ရှိထားပါတယ်။

• Season 1 - Episode 79
• Season 2 - Episode 47
• Total Episode: 126

• Released Date: (1970 - 1981)
• IMDb 8.2/10
• Running Time: Avg 25 min

👑 Member ကြေး ၅၀၀၀ကျပ် (5k)

[⚠️ Ashita No Joe Series တစ်ခုတည်း အတွက်သာ ဖြစ်သည်။]

(ဇာတ်လမ်းနှင့် ပတ်သက်၍ မေးမြန်းလိုပါက Auto AI reply စနစ် ထည့်သွင်း ထားသောကြောင့် စိတ်ကြိုက်မေးမြန်းနိုင်ပါတယ် ခင်ဗျာ..😉)"""
        
        image_url = "https://m.media-amazon.com/images/M/MV5BYTJmZTFlOGEtYmIxMi00NDY4LTlkZjYtOWExOTk3ZjdhYzk4XkEyXkFqcGdeQXVyMzgxNDA4MjM@._V1_.jpg"
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("💳 အခုပဲ ဝယ်ယူမည် (5,000 MMK)", callback_data="q2"))
        markup.add(types.InlineKeyboardButton("🎬 Channel တွင် အစမ်းကြည့်ရှုရန်", url="https://t.me/ashitanojoefreeep"))
        
        bot.send_photo(call.message.chat.id, image_url, caption=caption_text, reply_markup=markup)
        
    elif call.data == "q2":
        answer = f"""💳 *Member ကြေး ပေးချေရန် အချက်အလက်များ*

• **KBZ Pay:** `{KPAY_PHONE}`
• **Wave Pay:** `{WAVE_PHONE}`
• **Account Name:** {ACCOUNT_NAME}
• **ကျသင့်ငွေ:** ၅,၀၀၀ ကျပ် (Joe Series တစ်ခုတည်းအတွက် သီးသန့်)

[⚠️ ငွေပေးချေထားသော Screenshot ဓာတ်ပုံအား အောက်ပါ Admin ထံ ပေးပို့ပေးပါရန်။ ❗]"""
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("👤 Owner (@Nazzpar)", url="https://t.me/Nazzpar"),
            types.InlineKeyboardButton("👥 Admin (@hikarikeen)", url="https://t.me/hikarikenn")
        )
        bot.send_message(call.message.chat.id, answer, parse_mode="Markdown", reply_markup=markup)
        
    elif call.data == "q3":
        answer = "🔒 *Nasspar's Premium Channel*\n\nလက်ရှိတွင် Premium Channel သီးသန့် မဖွင့်လှစ်သေးပါ။ ဝန်ဆောင်မှုအသစ်များ ထွက်ရှိပါက ဤ Bot မှတစ်ဆင့် အသိပေးသွားပါမည်။ 📵"
        bot.send_message(call.message.chat.id, answer, parse_mode="Markdown")

# 🧠 Smart Auto-Reply / Comprehensive AI Brain (ဘာပဲမေးမေး ဖြေပေးနိုင်သော စနစ်)
@bot.message_handler(func=lambda message: not message.text.startswith('/'))
def handle_smart_chat(message):
    user_id = message.from_user.id
    
    if not check_user_subscription(user_id):
        bot.reply_to(message, "⚠️ ကျေးဇူးပြု၍ ပထမဦးစွာ Channel ကို အရင် Join ပေးပါခင်ဗျာ။ /start ကိုနှိပ်ပြီး Channel Join ပါ။")
        return
        
    text = message.text.lower()
    bot.send_chat_action(message.chat.id, 'typing')
    
    # 🧠 အသေးစိတ် မေးခွန်းများနှင့် အချက်အလက်များ Mapping စနစ်
    if any(k in text for k in ["ဈေးဘယ်လောက်", "ဈေး", "ကျပ်", "ဘယ်လောက်လဲ", "price", "5000", "၅၀၀၀"]):
        reply = "💰 Ashita No Joe Series အတွက် Member ကြေးက **၅,၀၀၀ ကျပ် (5k)** ဖြစ်ပါတယ်။ KPay / Wave Pay တို့ဖြင့် ငွေပေးချေနိုင်ပါတယ်။"
    elif any(k in text for k in ["မန်ဘာဝင်ချင်", "member", "ဝယ်ချင်", "ကြည့်ချင်", "join"]):
        reply = "💳 မန်ဘာဝင်ရောက်ရန်အတွက် /start ကိုနှိပ်ပြီး 'Ashita No Joe အတွက် ငွေပေးချေရန်' ခလုတ်ကို နှိပ်ကာ ငွေလွှဲပြေစာ (Screenshot) အား Owner @Nazzpar ထံ ပို့ပေးရပါမယ်။"
    elif any(k in text for k in ["တစ်ခုတည်း", "တစ်ပုဒ်တည်း", "joe series တစ်ခုတည်းအတွက် ၅၀၀၀", "series တစ်ခုတည်း"]):
        reply = "✅ ဟုတ်ကဲ့ပါခင်ဗျာ။ ပေးရမည့် ၅,၀၀၀ ကျပ် (5k) က **Ashita No Joe Series တစ်ခုတည်းအတွက် သီးသန့်** ဖြစ်ပါတယ်။ Season 1 & 2 အစအဆုံး အပြည့်အစုံ ကြည့်ရှုနိုင်မှာ ဖြစ်ပါတယ်။"
    elif any(k in text for k in ["ငွေဘယ်လိုလွှဲ", "ငွေလွှဲ", "kpay", "wave", "ဘယ်လိုပေးရမလဲ", "acc"]):
        reply = f"💳 ငွေလွှဲရန် အချက်အလက်များ:\n• KBZ Pay: `{KPAY_PHONE}`\n• Wave Pay: `{WAVE_PHONE}`\n• အမည်: {ACCOUNT_NAME}\nငွေလွှဲပြီးပါက Screenshot ကို @Nazzpar ထံ ပို့ပေးပါ။"
    elif any(k in text for k in ["history", "ရေးဆွဲ", "ဖန်တီး", "author", "manga", "manga တွေက", "ဘယ်လိုစရေး", "သမိုင်း"]):
        reply = "📜 **Ashita No Joe History & Creation:**\nဤလက်ရာကို **Ikki Kajiwara** (ဇာတ်ညွှန်း) နှင့် **Tetsuya Chiba** (သရုပ်ဖော် ရေးဆွဲသူ) တို့က ပူးပေါင်းဖန်တီးခဲ့ကြပါတယ်။ ဂျပန်မန်ဂါသမိုင်းတွင် အထင်ကရအကျဆုံး လက်ဝှေ့ Anime တစ်ခုဖြစ်ပြီး၊ ဆင်းရဲသားဘဝမှ လမ်းဘေးလူဆိုးကောင်လေး Yabuki Joe တစ်ယောက် လက်ဝှေ့ချန်ပီယံဆီသို့ အသက်ကိုရင်းပြီး လျှောက်လှမ်းခဲ့တဲ့ ဘဝခရီးလမ်းကို အစစ်အမှန်ပေါ်လွင်အောင် အနုပညာမြောက်စွာ ရေးဆွဲဖန်တီးခဲ့ခြင်း ဖြစ်ပါတယ်။"
    elif any(k in text for k in ["လူသိနည်း", "fan", "popular", "နာမည်ကြီးလား", "ပရိသတ်", "impact"]):
        reply = "⭐ **Ashita No Joe ရဲ့ နာမည်ကျော်ကြားမှုနှင့် ပရိသတ်များ:**\nကမ္ဘာတစ်ဝန်းမှာရော ဂျပန်နိုင်ငံမှာပါ **Classic Anime တွေထဲက နံပါတ်တစ် အထင်ကရ လက်ရာတစ်ခု** အဖြစ် သတ်မှတ်ခံထားရပါတယ်။ ဂျပန်ယဉ်ကျေးမှုအပေါ် ကြီးမားတဲ့ ရိုက်ခတ်မှု (Cultural Impact) ရှိခဲ့ပြီး ယနေ့ခေတ်တိုင်အောင် သစ္စာရှိတဲ့ Hardcore Classic Anime Fans တွေ အမြောက်အမြား အခိုင်အမာ ရှိနေဆဲ ဖြစ်ပါတယ်။"
    elif any(k in text for k in ["ဇာတ်လမ်းအကျဉ်း", "အကျဉ်း", "ဇာတ်ကြောင်း", "story", "ဘာဇာတ်လမ်းလဲ", "ဘာလဲ"]):
        reply = "🥊 **Ashita No Joe ဇာတ်လမ်းအကျဉ်း:**\nတိုကျိုမြို့ရဲ့ ဆင်းရဲသားရပ်ကွက်ထဲက လမ်းဘေးလူဆိုးကောင်လေး Yabuki Joe ဟာ ထူးချွန်တဲ့ လက်ဝှေ့ပညာရှင် Danpei Tange နဲ့ ဆုံတွေ့ပြီးနောက် လက်ဝှေ့လောကထဲကို ဝင်ရောက်လာပါတယ်။ ဘဝရဲ့ ဆင်းရဲမွဲတေမှု၊ ကြိုးဝိုင်းပေါ်က သွေးနဲ့ရင်းတဲ့ ပြင်းထန်တဲ့ တိုက်ပွဲတွေနဲ့ ရုန်းကန်လှုပ်ရှားမှုတွေကို အကောင်းဆုံး ရိုက်ကူးပြထားတဲ့ လက်ရာဖြစ်ပါတယ်။"
    elif any(k in text for k in ["admin", "owner", "ဆက်သွယ်", "အက်ဒမင်"]):
        reply = "👨‍💻 Channel Owner ကတော့ @Nazzpar ( Admin: @hikarikeen ) ဖြစ်ပါတယ်။ အသေးစိတ်ကို ဆက်သွယ်မေးမြန်းနိုင်ပါတယ်။"
    elif any(k in text for k in ["hi", "hello", "မင်္ဂလာပါ", "ဟေလို"]):
        reply = "မင်္ဂလာပါခင်ဗျာ! Nasspar's Bot မှ ကြိုဆိုပါတယ်။ Ashita No Joe နဲ့ ပတ်သက်ပြီး ဇာတ်လမ်း၊ History နဲ့ မန်ဘာကြေးများကို စိတ်ကြိုက်မေးမြန်းနိုင်ပါတယ်။"
    else:
        reply = (
            "🤖 **Ashita No Joe Bot AI Assistant:**\n"
            "သင်မေးမြန်းချက်ကို လက်ခံရရှိပါတယ်။ Ashita No Joe ရဲ့ ဇာတ်လမ်း၊ History၊ Season အချက်အလက်များ သို့မဟုတ် မန်ဘာငွေပေးချေမှုများကို Bot ထံမှာ လွတ်လပ်စွာ စာတိုပေးပို့ မေးမြန်းနိုင်ပါတယ်ခင်ဗျာ။ /start ကိုနှိပ်ပြီး ခလုတ်များဖြင့်လည်း လေ့လာနိုင်ပါတယ်! 😉"
        )
        
    bot.reply_to(message, reply)

bot.infinity_polling()
