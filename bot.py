import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, filters

# Logging သတ်မှတ်ခြင်း
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ထည့်သွင်းပေးလိုက်သော ဆိုင်ရှင် (Admin) ၏ Chat ID
ADMIN_CHAT_ID = 7658208028

# /start လို့ ရိုက်လိုက်ရင် ပေါ်လာမယ့် ပင်မ Menu 
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🫘 Mochi Chat Beans"],
        ["🎮 Mobile Legends Diamonds"],
        ["📞 ဆိုင်ရှင်ကို ဆက်သွယ်ရန်", "📌 မှာယူနည်း"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "✨ **Sonic Gameshop မှ ကြိုဆိုပါတယ်ရှင်** ✨\n\n"
        "အောက်ပါ Menu ကိုနှိပ်ပြီး လူကြီးမင်း လိုအပ်တာ ရွေးချယ်လို့ရပါတယ်ရှင်။",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Mochi Chat Beans ဈေးနှုန်းခလုတ်များ (Inline Buttons)
def get_bean_menu():
    keyboard = [
        [InlineKeyboardButton("100 Beans = 1,500 ks", callback_data="bean_100"), InlineKeyboardButton("200 Beans = 3,000 ks", callback_data="bean_200")],
        [InlineKeyboardButton("300 Beans = 4,500 ks", callback_data="bean_300"), InlineKeyboardButton("400 Beans = 6,000 ks", callback_data="bean_400")],
        [InlineKeyboardButton("500 Beans = 7,000 ks", callback_data="bean_500"), InlineKeyboardButton("600 Beans = 8,500 ks", callback_data="bean_600")],
        [InlineKeyboardButton("700 Beans = 10,000 ks", callback_data="bean_700"), InlineKeyboardButton("800 Beans = 11,500 ks", callback_data="bean_800")],
        [InlineKeyboardButton("900 Beans = 13,000 ks", callback_data="bean_900"), InlineKeyboardButton("1000 Beans = 14,000 ks", callback_data="bean_1000")],
        [InlineKeyboardButton("2800 Beans = 33,000 ks", callback_data="bean_2800")],
        [InlineKeyboardButton("4000 Beans = 45,000 ks", callback_data="bean_4000")],
        [InlineKeyboardButton("6000 Beans = 67,000 ks", callback_data="bean_6000")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Mobile Legends Diamonds ဈေးနှုန်းခလုတ်များ
def get_ml_menu():
    keyboard = [
        [InlineKeyboardButton("Weekly Pass = 6,500 ks", callback_data="ml_weekly")],
        [InlineKeyboardButton("Weekly Elite package = 3,500 ks", callback_data="ml_weekly_elite")],
        [InlineKeyboardButton("Epic Monthly Package = 16,900 ks", callback_data="ml_epic_monthly")],
        [InlineKeyboardButton("86 💎 = 5,400 ks", callback_data="ml_86"), InlineKeyboardButton("172 💎 = 10,500 ks", callback_data="ml_172")],
        [InlineKeyboardButton("257 💎 = 15,300 ks", callback_data="ml_257"), InlineKeyboardButton("706 💎 = 40,600 ks", callback_data="ml_706")],
        [InlineKeyboardButton("2195 💎 = 123,000 ks", callback_data="ml_2195"), InlineKeyboardButton("3688 💎 = 210,000 ks", callback_data="ml_3688")],
        [InlineKeyboardButton("5532 💎 = 311,000 ks", callback_data="ml_5532"), InlineKeyboardButton("9288 💎 = 516,000 ks", callback_data="ml_9288")],
        [InlineKeyboardButton("--- Diamond 2ဆ တစ်ကြိမ်သာ ---", callback_data="dummy")],
        [InlineKeyboardButton("50 + 50 💎 = 3,500 ks", callback_data="ml_50_50")],
        [InlineKeyboardButton("150 + 150 💎 = 11,000 ks", callback_data="ml_150_150")],
        [InlineKeyboardButton("250 + 250 💎 = 17,500 ks", callback_data="ml_250_250")],
        [InlineKeyboardButton("500 + 500 💎 = 33,500 ks", callback_data="ml_500_500")]
    ]
    return InlineKeyboardMarkup(keyboard)

# စာသားများကို ကိုင်တွယ်မည့် အပိုင်း
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if "Mochi Chat Beans" in text:
        await update.message.reply_text(
            "🫘 **Mochi Chat Bean ဈေးနှုန်းများ:**\n\n"
            "အောက်ပါ Package များမှ လိုချင်သည်ကို နှိပ်၍ ဝယ်ယူနိုင်ပါပြီရှင်။ 👇",
            reply_markup=get_bean_menu(),
            parse_mode="Markdown"
        )
    elif "Mobile Legends Diamonds" in text:
        await update.message.reply_text(
            "🎮 **Mobile Legends Diamond ဈေးနှုန်းများ:**\n\n"
            "အောက်ပါ Package များမှ လိုချင်သည်ကို နှိပ်၍ ဝယ်ယူနိုင်ပါပြီရှင်။ 👇",
            reply_markup=get_ml_menu(),
            parse_mode="Markdown"
        )
    elif "ဆက်သွယ်ရန်" in text:
        await update.message.reply_text("📞 ဆိုင်ရှင် Telegram ID - @jack200211 သို့မဟုတ် @eiei98765")
    elif "မှာယူနည်း" in text:
        await update.message.reply_text("📌 Package ရွေးချယ်ပြီး Game ID (သို့မဟုတ် Mochi UID) ပေးပို့ကာ ငွေလွှဲစခရင်ရှော့ ပို့ပေးရပါမယ်ရှင်။")
    else:
        if context.user_data.get("waiting_for_uid"):
            selected_item = context.user_data.get("selected_item")
            user_uid = text
            
            context.user_data["user_uid"] = user_uid
            context.user_data["waiting_for_uid"] = False 
            context.user_data["waiting_for_screenshot"] = True
            
            await update.message.reply_text(
                f"✅ **မှာယူမည့် အချက်အလက်:**\n"
                f"• Package: `{selected_item}`\n"
                f"• ID / UID: `{user_uid}`\n\n"
                f"━━━━━━━━━━━━━━━━━━━\n"
                f"💳 **PAYMENT CENTER (ငွေလွှဲရန် အကောင့်များ)**\n"
                f"━━━━━━━━━━━━━━━━━━━\n\n"
                f"🔵 **KBZ Pay**\n"
                f"• အမည် - `Sai Hseng Wan`\n"
                f"• ဖုန်းနံပါတ် - `09452230307`\n\n"
                f"🟢 **UAB Pay**\n"
                f"• အမည် - `Sai Hsai One`\n"
                f"• ဖုန်းနံပါတ် - `09452230307`\n\n"
                f"🟢 **AYA Pay**\n"
                f"• အမည် - `Sai Hsai One`\n"
                f"• ဖုန်းနံပါတ် - `09452230307`\n\n"
                f"🟡 **Wave Money**\n"
                f"• အမည် - `Sai Hsai Wam`\n"
                f"• ဖုန်းနံပါတ် - `09664123218`\n\n"
                f"━━━━━━━━━━━━━━━━━━━\n"
                f"ငွေလွှဲပြီးပါက ငွေလွှဲစခရင်ရှော့ (Screenshot) ပုံကို ဤချတ်ထဲသို့ ပို့ပေးပါရှင်။ 🙏",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text("ဟုတ်ကဲ့ရှင်။ အခြားသိလိုသည်များကိုလည်း မေးမြန်းနိုင်ပါတယ်ရှင်။ 🙏")

# ဝယ်သူက Screenshot ပို့လာရင် Admin ဆီသို့ ပို့ပေးမည့် အပိုင်း
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📥 ငွေလွှဲပြေစာကို လက်ခံရရှိပါပြီရှင်။ ဆိုင်ရှင်မှ စစ်ဆေးနေပါပြီ၊ ခဏစောင့်ပေးပါရှင်။ 🙏"
    )
    
    selected_item = context.user_data.get("selected_item", "မသိရှိရပါ")
    user_uid = context.user_data.get("user_uid", "မသိရှိရပါ")
    user_chat_id = update.message.chat_id 
    
    context.user_data["waiting_for_screenshot"] = False
    
    keyboard = [
        [InlineKeyboardButton("✅ Done (ပြီးပြီ)", callback_data=f"done_{user_chat_id}"),
         InlineKeyboardButton("❌ Cancel (ပယ်ဖျက်ရန်)", callback_data=f"cancel_{user_chat_id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    photo_file = update.message.photo[-1].file_id
    try:
        await context.bot.send_photo(
            chat_id=ADMIN_CHAT_ID,
            photo=photo_file,
            caption=f"🔔 **ဝယ်ယူမှု အသစ်ဝင်လာပါပြီရှင်!**\n\n"
                    f"📦 Item - `{selected_item}`\n"
                    f"🎮 ID / UID - `{user_uid}`\n"
                    f"👤 Buyer Chat ID - `{user_chat_id}`",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Admin ဆီသို့ ပုံပို့ရာတွင် အမှားဖြစ်နေပါသည်: {e}")

# ခလုတ်များ နှိပ်ခြင်းကို စီမံရန်
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "dummy":
        return
        
    if data.startswith("bean_"):
        bean_name = data.replace("bean_", "") + " Beans"
        context.user_data["selected_item"] = bean_name
        context.user_data["waiting_for_uid"] = True 
        
        await query.message.reply_text(
            f"🛒 လူကြီးမင်း ရွေးချယ်ထားသော Package: **{bean_name}**\n\n"
            f"ကျေးဇူးပြု၍ Mochi Chat ၏ **UID** နံပါတ်ကို ဤချတ်ထဲသို့ ရိုက်ထည့်ပေးပါရှင် ✍️",
            parse_mode="Markdown"
        )
    elif data.startswith("ml_"):
        ml_key = data.replace("ml_", "")
        
        if ml_key == "weekly":
            item_name = "Weekly Pass (6,500 ks)"
        elif ml_key == "weekly_elite":
            item_name = "Weekly Elite package (3,500 ks)"
        elif ml_key == "epic_monthly":
            item_name = "Epic Monthly Package (16,900 ks)"
        elif ml_key == "50_50":
            item_name = "50 + 50 Diamonds (3,500 ks)"
        elif ml_key == "150_150":
            item_name = "150 + 150 Diamonds (11,000 ks)"
        elif ml_key == "250_250":
            item_name = "250 + 250 Diamonds (17,500 ks)"
        elif ml_key == "500_500":
            item_name = "500 + 500 Diamonds (33,500 ks)"
        else:
            item_name = f"{ml_key} Diamonds"
            
        context.user_data["selected_item"] = item_name
        context.user_data["waiting_for_uid"] = True 
        
        await query.message.reply_text(
            f"🛒 လူကြီးမင်း ရွေးချယ်ထားသော Package: **{item_name}**\n\n"
            f"ကျေးဇူးပြု၍ Mobile Legends ၏ **Game ID နှင့် Server ID (ကွင်းစကွင်းပိတ်)** ကို ဤပုံစံအတိုင်း ရိုက်ထည့်ပေးပါရှင် ✍️\n"
            f"*(ဥပမာ - `1254697 (2728)`)*",
            parse_mode="Markdown"
        )
    elif data.startswith("done_"):
        buyer_chat_id = data.replace("done_", "")
        try:
            await query.edit_message_caption(
                caption=f"{query.message.caption}\n\n✅ **[အခြေအနေ: Order ထည့်ပြီးပါပြီ]**",
                parse_mode="Markdown"
            )
        except:
            pass
        await context.bot.send_message(
            chat_id=int(buyer_chat_id),
            text="လူကြီးမင်းရဲ့ Order ထည့်ပြီးပါပြီရှင့် ✨ ကျေးဇူးတင်ပါတယ်ရှင်။ 🙏"
        )
    elif data.startswith("cancel_"):
        buyer_chat_id = data.replace("cancel_", "")
        try:
            await query.edit_message_caption(
                caption=f"{query.message.caption}\n\n❌ **[အခြေအနေ: ပယ်ဖျက်လိုက်ပါပြီ]**",
                parse_mode="Markdown"
            )
        except:
            pass
        await context.bot.send_message(
            chat_id=int(buyer_chat_id),
            text="❌ ဝယ်ယူမှုမှာ အချက်အလက် မမှန်ကန်သဖြင့် ပယ်ဖျက်ခြင်း ခံရပါသည်ရှင်။"
        )

if __name__ == '__main__':
    # ဤနေရာတွင် ကိုယ့်ရဲ့ Telegram Bot Token ကို ထည့်ပါ
    application = ApplicationBuilder().token("8997131571:AAHcQ6lo_6D4LTmsgxXhaSq7pZ8JW-Oxx_0").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("Sonic Gameshop Bot is running...")
    application.run_polling()