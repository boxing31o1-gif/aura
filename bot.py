from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import requests

# التوكن الخاص ببوتك من BotFather
TOKEN = "8458580877:AAHfUa0-a8Ey_tbjU6gTL0LD9uqW6RiZ9zA"

# معرف القناة (اسم المستخدم للقناة العامة)
CHANNEL_ID = "@auracompany1"  # لازم البوت يكون مشرف بالقناة

# أمر /start مع أزرار روابط
async def start(update, context):
    keyboard = [
        [InlineKeyboardButton("💬 مجتمع شركة Aura عبر واتساب", url="https://chat.whatsapp.com/FuUJWYQSlmbAdMTBK48cwj?mode=hqrt1")],
        [InlineKeyboardButton("📢 قناة شركة Aura عبر تلغرام", url="https://t.me/auracompany1")],
        [InlineKeyboardButton("👨‍💼 للتواصل مع محمد", url="https://t.me/mrv8i")],
        [InlineKeyboardButton("👩‍💼 للتواصل مع رهف", url="https://t.me/Rahaf585")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 يسعدنا انضمامك إلى Aura Marketing،\n"
        "اختر أحد الروابط أدناه للتواصل معنا أو متابعة أحدث نشاطاتنا:",
        reply_markup=reply_markup
    )

# قاموس الكلمات والردود
responses = {
    "مرحبا": "🌸 أهلاً وسهلاً بك، يسعدنا خدمتك.",
    "السلام عليكم": "🤝 وعليكم السلام ورحمة الله، أهلاً بك في Aura Marketing.",
    "سعر": "💼 السعر 120 ألف",
    "طلب": "📝 نرجو تزويدنا بتفاصيل الطلب لنقوم بخدمتك بالشكل الأمثل.",
    "توصيل": "🚚 نوفر خدمة التوصيل داخل حماة والشحن إلى جميع المحافظات السورية.",
    "جملة": "📦 نوفر البيع مفرقاً وجملة بأسعار تنافسية."
}

# استقبال الرسائل النصية
async def handle_message(update, context):
    user_message = update.message.text.lower()
    reply = None

    for keyword, response in responses.items():
        if keyword in user_message:
            reply = response
            break

    if not reply:
        reply = "📩 شكراً لتواصلك. سيتم إحالة رسالتك إلى الإدارة (محمد_رهف) ومتابعتها في أقرب فرصة."

    await update.message.reply_text(reply)

# استقبال الصور
async def handle_photo(update, context):
    await update.message.reply_text(
        "📷 تم استلام الصورة.\n"
        "🗂 سيتم مراجعة تفاصيلك والتواصل معك من قِبل الإدارة (محمد_رهف) في أقرب وقت."
    )

# أمر /publish للنشر في القناة
async def publish(update, context):
    if update.message.text:
        message = update.message.text.replace("/publish", "").strip()
        if message:
            await context.bot.send_message(chat_id=CHANNEL_ID, text=message)
            await update.message.reply_text("✅ تم نشر الرسالة في قناة Aura.")
        else:
            await update.message.reply_text("⚠️ يرجى كتابة نص بعد الأمر /publish.")
    elif update.message.photo:
        photo = update.message.photo[-1].file_id
        caption = update.message.caption if update.message.caption else ""
        await context.bot.send_photo(chat_id=CHANNEL_ID, photo=photo, caption=caption)
        await update.message.reply_text("✅ تم نشر الصورة في قناة Aura.")
    else:
        await update.message.reply_text("⚠️ يمكنك استخدام /publish مع نص أو صورة.")

# إعداد التطبيق
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("publish", publish))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

print("✅ Aura Marketing Bot جاهز — جرب /start أو /publish")
app.run_polling()
