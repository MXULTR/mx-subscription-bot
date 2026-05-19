import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# --- الإعدادات (تأكد من إضافتها كـ Environment Variables في Railway) ---
TOKEN = os.environ.get("PAYMENT_BOT_TOKEN") 
ADMIN_USERNAME = "@MXULT" # تم تثبيت يوزرك مباشرة لسهولة التواصل

# نص معلومات الدفع (يمكنك تعديل الأرقام لاحقاً في Railway إذا أردت)
PAYMENT_INFO = (
    "💳 **معلومات الدفع والاستلام:**\n\n"
    "تقدر تحول عن طريق الوسائل المتاحة حالياً:\n"
    "• STC Pay: [رقمك هنا]\n"
    "• PayPal: [إيميلك هنا]\n"
    "• Binance (USDT): [رابط محفظتك]\n\n"
    "⚠️ **ملاحظة هامة:** بعد التحويل، صور الشاشة (إيصال الدفع) وأرسلها للمطور فوراً مع رقم الآي دي (ID) حقك لتفعيل حسابك VIP: " + ADMIN_USERNAME
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ترتيب الأزرار الجديد: إضافة باقة الشهر وحذف الأبدي
    keyboard = [
        [InlineKeyboardButton("💎 اشتراك شهر واحد (اقتصادي) = 2$", callback_data='sub_2')],
        [InlineKeyboardButton("💎 اشتراك 3 أشهر = 5$", callback_data='sub_5')],
        [InlineKeyboardButton("💎 اشتراك 6 أشهر = 7$", callback_data='sub_7')],
        [InlineKeyboardButton("💎 سنة كاملة = 12$", callback_data='sub_12')],
        [InlineKeyboardButton("────────────────", callback_data='none')],
        [InlineKeyboardButton("🎁 1$", callback_data='don_1'), InlineKeyboardButton("🎁 5$", callback_data='don_5')],
        [InlineKeyboardButton("🎁 10$", callback_data='don_10'), InlineKeyboardButton("🎁 50$", callback_data='don_50')],
        [InlineKeyboardButton("✨ دعم ماسي 100$ ✨", callback_data='don_100')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "👑 **قائمة الاشتراكات والدعم لشبكة MX**\n\n"
        "لو عجبك الشغل وتحب تدعم المشروع لتطوير الخوادم وإضافة ميزات جديدة مستقبلاً، "
        "تقدر تختار باقة الاشتراك المناسبة لك أو تدعمنا بمبلغ مباشر مجرد تبرع ودعم لي.\n\n"
        "👇 اختر الباقة أو مبلغ الدعم المالي:"
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

    # تنسيق النص النهائي المكتوب تحت معلومات الدفع ليظهر بشكل احترافي
    label = data.replace('sub_', 'باقة اشتراك بقيمة ').replace('don_', 'دعم مالي وتبرع بقيمة ') + "$"
    
    await query.edit_message_text(
        text=f"{PAYMENT_INFO}\n\n✨ *اختيارك الحالي:* {label}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data='back')]]),
        parse_mode="Markdown"
    )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("بوت الدفع شغال.. بانتظار الملايين! 🚀")
    app.run_polling()
    
