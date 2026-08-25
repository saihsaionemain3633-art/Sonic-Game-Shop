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
# Reseller Group ID
RESELLER_GROUP_ID = -1004382542271

# ဆိုင်ဖွင့်/ပိတ် အခြေအနေကို မှတ်သားရန် Global Variable (Default အနေဖြင့် ဆိုင်ဖွင့်ထားသည် - True)
SHOP_IS_OPEN = True

# အသုံးပြုပြီးသား ငွေလွှဲနံပါတ်များကို သိမ်းဆည်းရန် Set တစ်ခု ဖန်တီးခြင်း
USED_TRANSACTIONS = set()

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
        "အောက်ပါ Menu ကိုနှိပ်ပြီး လူကြီးမင်း လိုအပ်တာ ရွေးချယ်လို့ရပါတယ်ရှင်。",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Admin အတွက် ဆိုင်ဖွင့်/ပိတ် ထိန်းချုပ်မည့် Command (/admin)
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    if user_id != ADMIN_CHAT_ID:
        await update.message.reply_text("❌ ဤခလုတ်သည် ဆိုင်ရှင် (Admin) အတွက်သာ ဖြစ်ပါသည်။")
        return

    status_text = "🟢 လက်ရှိအခြေအနေ - ဆိုင်ဖွင့်ထားသည်" if SHOP_IS_OPEN else "🔴 လက်ရှိအခြေအနေ - ဆိုင်ပိတ်ထားသည်"
    
    keyboard = [
        [InlineKeyboardButton("🟢 ဆိုင်ဖွင့်မည်", callback_data="shop_open"),
         InlineKeyboardButton("🔴 ဆိုင်ပိတ်မည်", callback_data="shop_close")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"⚙️ **Admin Control Panel**\n\n{status_text}\n\nဆိုင်အခြေအနေကို ပြောင်းလဲလိုပါက အောက်ပါခလုတ်များကို နှိပ်ပါရှင်။",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Mochi Chat Beans ဈေးနှုန်းခလုတ်များ
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
    global SHOP_IS_OPEN
    text = update.message.text
    chat_id = update.message.chat_id
    
    if "Mochi Chat Beans" in text or "Mobile Legends Diamonds" in text:
        # ဆိုင်ပိတ်ထားပါက မည်သည့် Package ကိုမှ နှိပ်၍မရအောင် တားမြစ်မည်
        if not SHOP_IS_OPEN:
            await update.message.reply_text(
                "🌙 **ဆိုင်ပိတ်ချိန်လေးရောက်ပါပြီရှင့်!**\n\n"
                "ကျွန်ုပ်တို့၏ Sonic Gameshop ဆိုင်ပိတ်ထားပါပြီ။ သို့သော် Admin မအိပ်သေးပါက ဆိုင်ရှင်ထံသို့ တိုက်ရိုက်ဆက်သွယ်၍ ဝယ်ယူနိုင်ပါသေးတယ်ရှင့်ရှင်။ 📞\n\n"
                "ဆက်သွယ်ရန် - @jack200211 သို့မဟုတ် @eiei98765",
                parse_mode="Markdown"
            )
            return

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
        await update.message.reply_text("📌 Package ရွေးချယ်ပြီး Player ID / UID ပေးပို့ကာ ငွေလွှဲပြေစာပုံနှင့် နံပါတ် ၅ လုံးဖြင့် မှာယူနိုင်ပါပြီရှင်။")
    else:
        # ဆိုင်ပိတ်ထားစဉ် အခြားစာများ ပို့လာပါက
        if not SHOP_IS_OPEN and chat_id != ADMIN_CHAT_ID:
            # အကယ်၍ UID တောင်းနေချိန် သို့မဟုတ် ငွေလွှဲပုံ တောင်းနေချိန် မဟုတ်ဘဲ အလကားစာပို့လျှင်
            if not context.user_data.get("waiting_for_uid") and not context.user_data.get("waiting_for_photo") and not context.user_data.get("waiting_for_txn"):
                await update.message.reply_text(
                    "🌙 **ဆိုင်ပိတ်ချိန်လေးရောက်ပါပြီရှင့်!**\n\n"
                    "ယခုအချိန်သည် ဆိုင်ပိတ်ချိန်ဖြစ်ပါသည်။ Admin မအိပ်သေးပါက ဆက်သွယ်ဝယ်ယူနိုင်ပါသည်ရှင့်။ 🙏",
                    parse_mode="Markdown"
                )
                return

        # ၁။ UID တောင်းခံနေသည့် အဆင့်
        if context.user_data.get("waiting_for_uid"):
            raw_input = text.strip()
            cleaned_uid = raw_input
            
            if cleaned_uid.lower().startswith("uid"):
                cleaned_uid = cleaned_uid[3:].strip()
            elif cleaned_uid.lower().startswith("id"):
                cleaned_uid = cleaned_uid[2:].strip()

            selected_item = context.user_data.get("selected_item", "")
            is_mochi = "Beans" in selected_item

            if is_mochi:
                if not cleaned_uid.isdigit():
                    await update.message.reply_text(
                        "❌ **UID အချက်အလက် မှားယွင်းနေပါသည်!**\n\n"
                        "UID သည် ကိန်းဂဏန်း (Numbers) သက်သက်သာ ဖြစ်ရပါမည်။\n\n"
                        "💡 **အကြံပြုချက်:** သင့်ရဲ့ UID ကို Mochi Chat profile ဘယ်ဘက်ထောင့်တွင် ကြည့်ရှုနိုင်ပါသည်။ ကျေးဇူးပြု၍ ဂဏန်းများကိုသာ မှန်ကန်စွာ ပြန်လည်ရိုက်ထည့်ပေးပါရှင်။ 🙏",
                        parse_mode="Markdown"
                    )
                    return

            user_uid = cleaned_uid
            context.user_data["user_uid"] = user_uid
            context.user_data["waiting_for_uid"] = False 
            context.user_data["waiting_for_photo"] = True 
            
            payment_text = (
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
                f"ငွေလွှဲပြီးပါက **ငွေလွှဲပြေစာပုံ (Screenshot) ကို ဤချတ်ထဲသို့ အရင်ပို့ပေးပါရှင်** 📸 ကျေးဇူးတင်ပါတယ် 🙏"
            )
            await update.message.reply_text(payment_text, parse_mode="Markdown")

        # ၃။ ငွေလွှဲနံပါတ် ၅ လုံး တောင်းခံနေသည့် အဆင့်
        elif context.user_data.get("waiting_for_txn"):
            txn_input = text.strip()
            
            if txn_input in USED_TRANSACTIONS:
                await update.message.reply_text(
                    "❌ အချက်အလက်မမှန်ပါ! ဤငွေလွှဲပြေစာနံပါတ်ကို အသုံးပြုပြီးပါပြီ။ ကျေးဇူးပြု၍ ပြေစာအသစ်ဖြင့် ပြန်လည်ကြိုးစားပါရန်။ 🙏"
                )
                return

            context.user_data["txn"] = txn_input
            context.user_data["waiting_for_txn"] = False
            
            USED_TRANSACTIONS.add(txn_input)
            context.user_data["used_txn_code"] = txn_input
            
            selected_item = context.user_data.get("selected_item", "မသိရှိရပါ")
            user_uid = context.user_data.get("user_uid", "မသိရှိရပါ")
            receipt_photo_id = context.user_data.get("receipt_photo_id")
            
            await update.message.reply_text(
                "🎉 **လူကြီးမင်း Order တင်ပေးထားပါပြီ!**\n\n"
                "ဆိုင်ရှင်မှ အချက်အလက်များကို စစ်ဆေးနေပါသည် စိတ်ရှည်စွာနဲ့ စောင့်ပေးပါဗျ။ ⏳"
            )
            
            admin_keyboard = [
                [InlineKeyboardButton("✅ Correct (မှန်ကန်သည်)", callback_data=f"correct_{chat_id}"),
                 InlineKeyboardButton("❌ Incorrect (အချက်အလက်မမှန်ပါ)", callback_data=f"incorrect_{chat_id}")]
            ]
            admin_reply_markup = InlineKeyboardMarkup(admin_keyboard)
            
            order_summary = (
                f"🔔 **စစ်ဆေးရန် အချက်အလက်အသစ် ဝင်လာပါပြီရှင်!**\n\n"
                f"• Item: `{selected_item}`\n"
                f"• ID / UID: `{user_uid}`\n"
                f"• ငွေလွှဲနံပါတ် နောက်ဆုံး ၅ လုံး: `{txn_input}`"
            )
            
            context.application.bot_data[f"order_{chat_id}"] = {
                "chat_id": chat_id,
                "selected_item": selected_item,
                "user_uid": user_uid,
                "txn_info": txn_input,
                "receipt_photo_id": receipt_photo_id
            }

            try:
                if receipt_photo_id:
                    await context.bot.send_photo(
                        chat_id=ADMIN_CHAT_ID,
                        photo=receipt_photo_id,
                        caption=order_summary,
                        reply_markup=admin_reply_markup,
                        parse_mode="Markdown"
                    )
                else:
                    await context.bot.send_message(
                        chat_id=ADMIN_CHAT_ID,
                        text=order_summary,
                        reply_markup=admin_reply_markup,
                        parse_mode="Markdown"
                    )
            except Exception as e:
                print(f"Admin ဆီသို့ ပို့ရာတွင် အမှားဖြစ်နေပါသည်: {e}")
        else:
            await update.message.reply_text("ဟုတ်ကဲ့ရှင်။ အခြားသိလိုသည်များကိုလည်း မေးမြန်းနိုင်ပါတယ်ရှင်။ 🙏")

# ၂။ ပြေစာပုံ (Photo) ပို့လာသည်ကို လက်ခံမည့် အပိုင်း
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("waiting_for_photo"):
        photo_file_id = update.message.photo[-1].file_id
        context.user_data["receipt_photo_id"] = photo_file_id
        context.user_data["waiting_for_photo"] = False
        context.user_data["waiting_for_txn"] = True 
        
        await update.message.reply_text(
            "✅ ပြေစာပုံ လက်ခံရရှိပါပြီရှင်။\n\n"
            "ကျေးဇူးပြု၍ **လုပ်ငန်းစဉ်နံပါတ် (ငွေလွှဲနံပါတ်) နောက်ဆုံး ၅ လုံး** ကို ဆက်လက် ရေးပြီး ပို့ပေးပါရှင် ✍️",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text("ကျေးဇူးပြု၍ လိုအပ်သော အချက်အလက်များကို ပုံစံအတိုင်း အစဉ်လိုက် ဆက်လက် ပို့ပေးပါရှင် ✍️")

# ခလုတ်များ နှိပ်ခြင်းကို စီမံရန်
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global SHOP_IS_OPEN
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    # ဆိုင်ဖွင့်/ပိတ် ခလုတ်များအတွက်
    if data == "shop_open":
        SHOP_IS_OPEN = True
        await query.edit_message_text(text="🟢 ဆိုင်ဖွင့်လိုက်ပါပြီရှင်။ ယခုအခါ ဝယ်သူများ ပုံမှန် Order တင်နိုင်ပါပြီ။")
        return
    elif data == "shop_close":
        SHOP_IS_OPEN = False
        await query.edit_message_text(text="🔴 ဆိုင်ပိတ်လိုက်ပါပြီရှင်။ ယခုအခါ ဆိုင်ပိတ်ချိန် စာသားများ ပေါ်လာပါမည်။")
        return

    if data == "dummy":
        return
        
    # ဆိုင်ပိတ်ထားလျှင် ခလုတ်နှိပ်၍ မရအောင် တားမြစ်ရန်
    if not SHOP_IS_OPEN:
        await query.message.reply_text(
            "🌙 **ဆိုင်ပိတ်ချိန်လေးရောက်ပါပြီရှင့်!**\n\n"
            "ယခုအချိန်သည် ဆိုင်ပိတ်ချိန်ဖြစ်ပါသည်။ Admin မအိပ်သေးပါက ဆက်သွယ်ဝယ်ယူနိုင်ပါသည်ရှင့်။ 📞\n\n"
            "ဆက်သွယ်ရန် - @jack200211 သို့မဟုတ် @eiei98765",
            parse_mode="Markdown"
        )
        return

    if data.startswith("bean_"):
        raw_bean = data.replace("bean_", "")
        bean_name = raw_bean + " Beans"
        
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
            item_name = "Weekly Pass"
        elif ml_key == "weekly_elite":
            item_name = "Weekly Elite package"
        elif ml_key == "epic_monthly":
            item_name = "Epic Monthly Package"
        elif ml_key == "50_50":
            item_name = "50 + 50 Diamonds"
        elif ml_key == "150_150":
            item_name = "150 + 150 Diamonds"
        elif ml_key == "250_250":
            item_name = "250 + 250 Diamonds"
        elif ml_key == "500_500":
            item_name = "500 + 500 Diamonds"
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
        
    # Admin ဘက်မှ CORRECT နှိပ်လိုက်သောအခါ
    elif data.startswith("correct_"):
        buyer_chat_id = data.replace("correct_", "")
        order_data = context.application.bot_data.get(f"order_{buyer_chat_id}")
        
        try:
            if query.message.caption:
                await query.edit_message_caption(
                    caption=f"{query.message.caption}\n\n✅ **[အခြေအနေ: အချက်အလက်မှန်ကန်၍ Group သို့ ပို့လိုက်ပါပြီ]**",
                    parse_mode="Markdown"
                )
            else:
                await query.edit_message_text(
                    text=f"{query.message.text}\n\n✅ **[အခြေအနေ: အချက်အလက်မှန်ကန်၍ Group သို့ ပို့လိုက်ပါပြီ]**",
                    parse_mode="Markdown"
                )
        except:
            pass
            
        if order_data:
            group_keyboard = [
                [InlineKeyboardButton("✅ Done (ပြီးပြီ)", callback_data=f"done_{buyer_chat_id}"),
                 InlineKeyboardButton("⚠️ Order Error", callback_data=f"error_{buyer_chat_id}")]
            ]
            group_reply_markup = InlineKeyboardMarkup(group_keyboard)
            
            group_summary = (
                f"🔔 **Order အသစ်ဝင်လာပါပြီရှင်!**\n\n"
                f"• Item: `{order_data['selected_item']}`\n\n"
                f"• ID / UID: `{order_data['user_uid']}`"
            )
            
            try:
                await context.bot.send_message(
                    chat_id=RESELLER_GROUP_ID,
                    text=group_summary,
                    reply_markup=group_reply_markup,
                    parse_mode="Markdown"
                )
            except Exception as e:
                print(f"Group ဆီသို့ ပို့ရာတွင် အမှားဖြစ်နေပါသည်: {e}")

    # Admin ဘက်မှ INCORRECT နှိပ်လိုက်သောအခါ
    elif data.startswith("incorrect_"):
        buyer_chat_id = data.replace("incorrect_", "")
        
        try:
            if query.message.caption:
                await query.edit_message_caption(
                    caption=f"{query.message.caption}\n\n❌ **[အခြေအနေ: အချက်အလက် မမှန်ကန်ပါ]**",
                    parse_mode="Markdown"
                )
            else:
                await query.edit_message_text(
                    text=f"{query.message.text}\n\n❌ **[အခြေအနေ: အချက်အလက် မမှန်ကန်ပါ]**",
                    parse_mode="Markdown"
                )
        except:
            pass
            
        await context.bot.send_message(
            chat_id=int(buyer_chat_id),
            text="❌ လူကြီးမင်း ပို့ထားသော အချက်အလက်များ မမှန်ကန်ပါ။ ကျေးဇူးပြု၍ ပြန်လည်စစ်ဆေးပြီး အသစ်ထပ်မံ မှာယူပေးပါရန်။ 🙏"
        )

    # Group ထဲမှ DONE နှိပ်လိုက်သောအခါ
    elif data.startswith("done_"):
        buyer_chat_id = data.replace("done_", "")
        try:
            if query.message.caption:
                await query.edit_message_caption(
                    caption=f"{query.message.caption}\n\n✅ **[အခြေအနေ: Order ထည့်ပြီးပါပြီ]**",
                    parse_mode="Markdown"
                )
            else:
                await query.edit_message_text(
                    text=f"{query.message.text}\n\n✅ **[အခြေအနေ: Order ထည့်ပြီးပါပြီ]**",
                    parse_mode="Markdown"
                )
        except:
            pass
        await context.bot.send_message(
            chat_id=int(buyer_chat_id),
            text="လူကြီးမင်းရဲ့ Order ထည့်ပြီးပါပြီရှင့် ✨ ကျေးဇူးတင်ပါတယ်ရှင်။ 🙏"
        )
        
    # Group ထဲမှ ORDER ERROR နှိပ်လိုက်သောအခါ
    elif data.startswith("error_"):
        buyer_chat_id = data.replace("error_", "")
        
        buyer_order = context.application.bot_data.get(f"order_{buyer_chat_id}")
        if buyer_order and "txn_info" in buyer_order:
            USED_TRANSACTIONS.discard(buyer_order["txn_info"])

        try:
            if query.message.caption:
                await query.edit_message_caption(
                    caption=f"{query.message.caption}\n\n⚠️ **[အခြေအနေ: Order Error ဖြစ်ပါသည်]**",
                    parse_Mode="Markdown"
                )
            else:
                await query.edit_message_text(
                    text=f"{query.message.text}\n\n⚠️ **[အခြေအနေ: Order Error ဖြစ်ပါသည်]**",
                    parse_mode="Markdown"
                )
        except:
            pass
            
        await context.bot.send_message(
            chat_id=int(buyer_chat_id),
            text="⚠️ လူကြီးမင်း၏ Order တွင် အချက်အလက် မှားယွင်းမှုရှိနေပါသဖြင့် ကျေးဇူးပြု၍ Admin ထံသို့ တိုက်ရိုက် ဆက်သွယ်ပေးပါရန် မေတ္တာရပ်ခံအပ်ပါတယ်ရှင်။ 📞\n\nဆက်သွယ်ရန် - @jack200211 သို့မဟုတ် @eiei98765"
        )

if __name__ == '__main__':
    application = ApplicationBuilder().token("8997131571:AAHcQ6lo_6D4LTmsgxXhaSq7pZ8JW-Oxx_0").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin_panel))  # ဆိုင်ဖွင့်/ပိတ် ထိန်းချုပ်ရန်
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("Sonic Gameshop Bot is running...")
    application.run_polling()
