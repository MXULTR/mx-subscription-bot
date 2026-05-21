import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# --- الإعدادات ---
TOKEN = os.environ.get("PAYMENT_BOT_TOKEN") 
ADMIN_USERNAME = "@MX23I" 

# رسالة معلومات الدفع الموحدة
PAYMENT_INFO = (
    "💳 **معلومات الدفع:**\n\n"
    "• مصرف الراجحي: `SA64 8000 0539 6080 1586 2568`\n\n"
    "💬 **ملاحظة:** إذا كنت تفضل طريقة دفع أخرى (STC Pay، محفظة رقمية، إلخ)، لا تتردد بالتواصل معي مباشرة في أي وقت: " + ADMIN_USERNAME + "\n\n"
    "⚠️ **بعد التحويل:** أرسل صورة الإيصال مع رقم الـ ID الخاص بك للمطور لتفعيل طلبك فوراً."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # إضافة خيار التبرع للقائمة
    keyboard = [
        [InlineKeyboardButton("💎 شهر واحد = 2$", callback_data='sub')],
        [InlineKeyboardButton("💎 3 أشهر = 5$", callback_data='sub')],
        [InlineKeyboardButton("💎 6 أشهر = 7$", callback_data='sub')],
        [InlineKeyboardButton("💎 سنة كاملة = 12$", callback_data='sub')],
        [InlineKeyboardButton("🎁 دعم المشروع (تبرع حر)", callback_data='sub')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "👑 **قائمة خدمات شبكة MX**\n\n"
        "شكراً لثقتك ودعمك! اختر الباقة المناسبة أو خيار التبرع لدعم استمرار المشروع.\n\n"
        "👇 اختر ما يناسبك:"
    )
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.callback_query.edit_message_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'back':
        await start(update, context)
        return

    # عرض نفس معلومات الدفع للجميع
    await query.edit_message_text(
        text=f"{PAYMENT_INFO}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data='back')]]),
        parse_mode="Markdown"
    )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("البوت يعمل الآن مع خيار التبرع.. 🚀")
    app.run_polling()
    
