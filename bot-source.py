#    License can be found in < https://github.com/xditya/ChannelAutoForwarder/blob/main/License> .

import logging
from telethon import TelegramClient, events, Button
from decouple import config

# @EmilySweetyBabe
APP_ID = 20586238
API_HASH = "5accd362e03a50741b7d0c5623acfcb9"

# ForwarderBot
# @ForwarderTimBot
BOT_TOKEN = "6025839502:AAFgHIWJ_E3K4Xg5qsqwoYqE-GcuSwWBz_4"

# The IDs of the main channel from where posts have to be copied
# eg: `-100xxxx -100yyyy -100abcd ...`
# Test-Channel-Source -1001824520184
FROM_CHANNEL = "-1001824520184"

# The ID of the channel to which the posts are to be sent, split by space. 
# eg: `-100xxxx -100yyyy -100abcd ...`
# Test-Channel-Destination -1001872595824
# Collect Channel TimGahmenEmu -1002225320095
TO_CHANNEL = "-1001872595824"

logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s] %(asctime)s - %(message)s"
)
log = logging.getLogger("ChannelAutoPost")

# start the bot
log.info("Starting...")
try:
    # apiid = config("APP_ID", cast=int)
    # apihash = config("API_HASH")
    # bottoken = config("BOT_TOKEN")
    # frm = config("FROM_CHANNEL", cast=lambda x: [int(_) for _ in x.split(" ")])
    # tochnls = config("TO_CHANNEL", cast=lambda x: [int(_) for _ in x.split(" ")])

    frm = FROM_CHANNEL.split(" ")
    tochnls = TO_CHANNEL.split(" ")
    datgbot = TelegramClient(None, APP_ID, API_HASH).start(bot_token=BOT_TOKEN)

except Exception as exc:
    log.error("Environment vars are missing! Kindly recheck.")
    log.info("Bot is quiting...")
    log.error(exc)
    exit()


@datgbot.on(events.NewMessage(pattern="/start"))
async def _(event):
    await event.reply(
        f"Hi `{event.sender.first_name}`!\n\nI am a channel auto-post bot!! Read /help to know more!\n\nI can be used in only two channels (one user) at a time. Kindly deploy your own bot.\n\n[More bots](https://t.me/its_xditya)..",
        buttons=[
            Button.url("Repo", url="https://github.com/xditya/ChannelAutoForwarder"),
            Button.url("Dev", url="https://xditya.me"),
        ],
        link_preview=False,
    )


@datgbot.on(events.NewMessage(pattern="/help"))
async def helpp(event):
    await event.reply(
        "**Help**\n\nThis bot will send all new posts in one channel to the other channel. (without forwarded tag)!\nIt can be used only in two channels at a time, so kindly deploy your own bot from [here](https://github.com/xditya/ChannelAutoForwarder).\n\nAdd me to both the channels and make me an admin in both, and all new messages would be autoposted on the linked channel!!\n\nLiked the bot? Drop a ♥ to @xditya_Bot :)"
    )


@datgbot.on(events.NewMessage(incoming=True, chats=frm))
async def _(event):
    for tochnl in tochnls:
        try:
            if event.poll:
                return
            if event.photo:
                photo = event.media.photo
                await datgbot.send_file(
                    tochnl, photo, caption=event.text, link_preview=False
                )
            elif event.media:
                try:
                    if event.media.webpage:
                        await datgbot.send_message(
                            tochnl, event.text, link_preview=False
                        )
                except Exception:
                    media = event.media.document
                    await datgbot.send_file(
                        tochnl, media, caption=event.text, link_preview=False
                    )
                finally:
                    return
            else:
                await datgbot.send_message(tochnl, event.text, link_preview=False)
        except Exception as exc:
            log.error(
                "TO_CHANNEL ID is wrong or I can't send messages there (make me admin).\nTraceback:\n%s",
                exc,
            )


log.info("Bot has started.")
log.info("Do visit https://xditya.me !")
datgbot.run_until_disconnected()