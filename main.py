
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes
)

NAME, MAJOR, CITY, JOB_TYPE, REMOTE = range(5)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا بك في بوت التوظيف لخريجات الكلية التقنية بأبها!\nما اسمك الكامل؟")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("ما تخصصك؟")
    return MAJOR

async def get_major(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["major"] = update.message.text
    await update.message.reply_text("ما المدينة التي ترغبين العمل بها؟")
    return CITY

async def get_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["city"] = update.message.text
    await update.message.reply_text("ما نوع الوظيفة المرغوبة؟ (مثل: إدارية، فنية...)")
    return JOB_TYPE

async def get_job_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["job_type"] = update.message.text
    await update.message.reply_text("هل ترغبين في العمل عن بعد؟ (نعم / لا)")
    return REMOTE

async def get_remote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["remote"] = update.message.text
    summary = (
        "شكرًا لك! هذه بياناتك:\n\n"
        f"الاسم: {context.user_data['name']}\n"
        f"التخصص: {context.user_data['major']}\n"
        f"المدينة: {context.user_data['city']}\n"
        f"نوع الوظيفة: {context.user_data['job_type']}\n"
        f"العمل عن بعد: {context.user_data['remote']}\n\n"
        "جارٍ مطابقة بياناتك مع الوظائف..."
    )
    await update.message.reply_text(summary)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تم الإلغاء.")
    return ConversationHandler.END

def main():
    import os
    TOKEN = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            MAJOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_major)],
            CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_city)],
            JOB_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_job_type)],
            REMOTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_remote)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
