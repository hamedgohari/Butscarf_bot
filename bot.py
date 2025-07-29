
import os
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.helpers import escape_markdown

TOKEN = os.getenv("TOKEN")
CHAT_ID = 94293021  # Chat ID شما
CHANNEL_USERNAME = "@butscarf"

# تابع گرفتن آمار کانال
async def get_report(app):
    try:
        chat = await app.bot.get_chat(CHANNEL_USERNAME)
        members = await app.bot.get_chat_members_count(CHANNEL_USERNAME)

        messages = await app.bot.get_chat_history(CHANNEL_USERNAME, limit=20)
        views = []
        async for msg in messages:
            if msg.views:
                views.append(msg.views)

        avg_views = sum(views)/len(views) if views else 0

        report = f"📊 *گزارش کانال {escape_markdown(CHANNEL_USERNAME,2)}*
"
        report += f"👥 اعضا: *{members}*
"
        report += f"📈 میانگین بازدید ۲۰ پست آخر: *{int(avg_views)}*
"
        return report
    except Exception as e:
        return f"⚠️ خطا در گرفتن آمار: {e}"

# دستور /report
async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    report = await get_report(context.application)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=report, parse_mode="MarkdownV2")

# ارسال گزارش خودکار ساعت ۱۰ شب
async def scheduled_task(app):
    while True:
        now = datetime.now()
        if now.hour == 22 and now.minute == 0:
            report = await get_report(app)
            await app.bot.send_message(chat_id=CHAT_ID, text=report, parse_mode="MarkdownV2")
            await asyncio.sleep(60)
        await asyncio.sleep(30)

async def on_start(app):
    asyncio.create_task(scheduled_task(app))

app = ApplicationBuilder().token(TOKEN).post_init(on_start).build()
app.add_handler(CommandHandler("report", report_command))
app.run_polling()
