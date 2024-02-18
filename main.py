from telegram import Update,InlineQueryResultArticle,InputTextMessageContent
from telegram.ext import CommandHandler,InlineQueryHandler,MessageHandler,ApplicationBuilder,ContextTypes,filters
from genius import findSong,findLyrics
BOT_TOKEN  = "your_token"
START_MESSASGE= """Hello, You can search lyrics with me and find song lyrics
use inline mode to search for songs"""
async def inline(update:Update , context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query
    if not query:return
    songs = findSong(query.query)
    result = []
    id = 0
    for description,url in songs.items():
        result.append(
            InlineQueryResultArticle(id = id,title=description,
            input_message_content=InputTextMessageContent(url,disable_web_page_preview=True) )
        )
        id +=1
    await context.bot.answer_inline_query(query.id,results=result)
async def text_handle(update:Update , context:ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text
    if text.startswith('https://www.genius.com/') or text.startswith('https://genius.com/'):
        try:
            lyrics = findLyrics(text) # you can add stuff before sending it to a user
            await update.message.reply_text(lyrics)
        except Exception as e:
            print(e)
            await update.message.reply_text("sorry i couldnt get this")
    else:
        await update.message.reply_text("sorry this link is not supported")
async def start(update:Update , context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(update.effective_chat.id,START_MESSASGE)
application =  ApplicationBuilder().token(BOT_TOKEN).build()
start_handler = CommandHandler('start',start)
query_handler = InlineQueryHandler(inline)
text_handler = MessageHandler(filters.TEXT,text_handle)
application.add_handler(start_handler)
application.add_handler(query_handler)
application.add_handler(text_handler)
# application.run_webhook()
application.run_polling()
