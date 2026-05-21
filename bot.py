import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# --- الإعدادات ---
# تأكد من إضافة TOKEN الخاص ببوت الدفع في Railway
TOKEN = os.environ.get("PAYMENT_BOT_TOKEN") 
ADMIN_USERNAME = "@MXULT" 

# النص النهائي المعتمد
PAYMENT_INFO = (
    "💳 **معلومات الدفع:**\n\n"
    "• مصرف الراجحي: `539000010006085862568`\n\n"
    "💬 **ملاحظة:** إذا كنت تفضل طريقة دفع أخرى (STC Pay، محفظة رقمية، إلخ)، لا تتردد بالتواصل معي مباشرة في أي وقت: " + ADMIN_USERNAME + "\n\n"
    "⚠️ **بعد التحويل:** أرسل صورة الإيصال مع رقم الـ ID الخاص بك للمطور لتفعيل اشتراكك فوراً."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # قائمة الباقات المختصرة
    keyboard = [
        [InlineKeyboardButton("💎 شهر واحد (اقتصادي) = 2$", callback_data='sub_2')],
        [InlineKeyboardButton("💎 3 أشهر = 5$", callback_data='sub_5')],
        [InlineKeyboardButton("💎 6 أشهر = 7$", callback_data='sub_7')],
        [InlineKeyboardButton("💎 سنة كاملة = 12$", callback_data='sub_12')],
        [InlineKeyboardButton("────────────────", callback_data='none')],
        [InlineKeyboardButton("🎁 دعم المشروع (تبرع حر)", callback_data='don_custom')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "👑 **قائمة الاشتراكات - شبكة MX**\n\n"
        "شكراً لثقتك ودعمك للمشروع! اختر الباقة المناسبة لك لبدء التحميل بدون حدود.\n\n"
        "👇 اختر الباقة:"
    )
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.callback_query.edit_message_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'none': return
    if query.data == 'back':
        await start(update, context)
        return

    # عرض معلومات الدفع الموحدة
    await query.edit_message_text(
        text=f"{PAYMENT_INFO}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data='back')]]),
        parse_mode="Markdown"
    )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("بوت الدفع شغال.. بانتظار الملايين! 🚀")
    app.run_polling()
    
