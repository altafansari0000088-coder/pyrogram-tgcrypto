import os
import subprocess
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = 32124905
API_HASH = "227aa77657fbbc1b624761ce58835439"
BOT_TOKEN = "9062426057:AAFtpkDppKHwiH8uFHwJtKvx5rJiyXrrAY0"

app = Client("drama_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_handler(client, message: Message):
    await message.reply_text(
        "👋 Welcome! Story TV, Kuku TV, Rocket Reels ya QuickTV ka video link bhejein."
    )

@app.on_message(filters.text & ~filters.command(["start", "help"]))
async def link_handler(client, message: Message):
    url = message.text.strip()

    if not url.startswith("http"):
        await message.reply_text("Kripya valid video link bhejein.")
        return

    status = await message.reply_text("⏳ Download shuru ho raha hai...")
    output_filename = f"video_{message.from_user.id}.mp4"

    cmd = [
        "ffmpeg",
        "-y",
        "-headers", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n",
        "-i", url,
        "-c", "copy",
        "-bsf:a", "aac_adtstoasc",
        output_filename
    ]

    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process.communicate()

        if os.path.exists(output_filename) and os.path.getsize(output_filename) > 0:
            await status.edit_text("📤 Telegram par upload ho raha hai...")
            await message.reply_video(
                video=output_filename,
                caption="✅ Download complete!"
            )
            os.remove(output_filename)
            await status.delete()
        else:
            await status.edit_text("❌ Download fail ho gaya. Link direct streamable nahi hai.")

    except Exception as e:
        await status.edit_text(f"❌ Error: {str(e)}")
        if os.path.exists(output_filename):
            os.remove(output_filename)

app.run()
