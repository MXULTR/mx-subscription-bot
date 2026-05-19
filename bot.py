import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# --- الإعدادات (تأكد من إضافتها في Railway لاحقاً) ---
TOKEN = os.environ.get("PAYMENT_BOT_TOKEN") 
ADMIN_USERNAME = "@YourUsername" # <--- استبدله بيوزرك في تليجرام عشان يكلمونك

# نص معلومات الدفع (عدله باللي يناسبك)
PAYMENT_INFO = (
    "💳 **معلومات الدفع والاستلام:**\n\n"
    "تقدر تحول عن طريق:\n"
    "• STC Pay: [رقمك هنا]\n"
    "• PayPal: [إيميلك هنا]\n"
    "• Binance (USDT): [رابط محفظتك]\n\n"
    "⚠️ **ملاحظة:** بعد التحويل، صور الشاشة (الإيصال) وأرسلها للمطور مع رقم الآي دي (ID) حقك لتفعيل الاشتراك فوراً: " + ADMIN_USERNAME
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ترتيب الأزرار بشكل نظيف
    keyboard = [
        [InlineKeyboardButton("💎 اشتراك 3 أشهر = 5$", callback_data='sub_5')],
        [InlineKeyboardButton("💎 اشتراك 6 أشهر = 7$", callback_data='sub_7')],
        [InlineKeyboardButton("💎 سنة كاملة = 12$", callback_data='sub_12')],
        [InlineKeyboardButton("👑 اشتراك أبدي = 25$", callback_data='sub_25')],
        [InlineKeyboardButton("────────────────", callback_data='none')],
        [InlineKeyboardButton("🎁 1$", callback_data='don_1'), InlineKeyboardButton("🎁 5$", callback_data='don_5')],
        [InlineKeyboardButton("🎁 10$", callback_data='don_10'), InlineKeyboardButton("🎁 50$", callback_data='don_50')],
        [InlineKeyboardButton("✨ دعم ماسي 100$ ✨", callback_data='don_100')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "👑 **قائمة الاشتراكات والدعم**\n\n"
        "لو عجبك الشغل وتحب تدعمني تقدر :) من هنا بكل سهولة من غير الاشتراك نفسه، "
        "علشان نتطور ونضيف مميزات أكثر بالمستقبل وشكراً بالنهاية.\n\n"
        "👇 اختر الباقة أو مبلغ الدعم:"
    )
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
    else: # في حال تم طلبه من زر العودة
        await update.callback_query.edit_message_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    if data == 'none': return
    if data == 'back':
        await start(update, context)
        return

    # عرض معلومات الدفع عند الضغط على أي باقة
    await query.edit_message_text(
        text=f"{PAYMENT_INFO}\n\n*اختيارك:* {data.replace('sub_', 'اشتراك ').replace('don_', 'تبرع ')}$",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة للقائمة", callback_data='back')]]),
        parse_mode="Markdown"
    )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("بوت الدفع شغال.. بانتظار الملايين! 🚀")
    app.run_polling()
  
