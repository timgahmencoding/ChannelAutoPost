# https://github.com/xditya/ChannelAutoForwarder).

import logging
from telethon import TelegramClient, events, Button
from decouple import config

logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s] %(asctime)s - %(message)s"
)
log = logging.getLogger("ChannelAutoPost")


# ----------------------------------------------------------------------------------------------
# start the bot

log.info("Starting...")


try:
    apiid = config("APP_ID", cast=int)
    apihash = config("API_HASH")
    bottoken = config("BOT_TOKEN")

    FROM_ = config("FROM_CHANNEL")
    TO_ = config("TO_CHANNEL")

    FROM = [int(i) for i in FROM_.split(",")]
    TO = [int(i) for i in TO_.split(",")]

    # log.info(f"\n\nFROM_ {FROM_}\nTO_ {TO_}\n\nFROM {FROM}\nTO {TO}\n\n")
    log.info(f"Forwarding:")
    # log.info(f"\n\nFROM_ {FROM_}\nTO_ {TO_}\n")
    log.info(f"\n\nFROM {FROM}\nTO {TO}")


    datgbot = TelegramClient("ChannelAutoForwarder", apiid, apihash).start(bot_token=bottoken)

except Exception as exc:
    log.error("Environment vars are missing! Kindly recheck.")
    log.info("Bot is quiting...")
    log.error(exc)
    exit()


# ----------------------------------------------------------------------------------------------
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


# ----------------------------------------------------------------------------------------------
@datgbot.on(events.NewMessage(pattern="/help"))
async def helpp(event):
    await event.reply(
        "**Help**\n\nThis bot will send all new posts in one channel to the other channel. (without forwarded tag)!\nIt can be used only in two channels at a time, so kindly deploy your own bot from [here](https://github.com/xditya/ChannelAutoForwarder).\n\nAdd me to both the channels and make me an admin in both, and all new messages would be autoposted on the linked channel!!\n\nLiked the bot? Drop a ♥ to @xditya_Bot :)"
    )


# ----------------------------------------------------------------------------------------------
# @datgbot.on(events.NewMessage(incoming=True, chats=frm))
@datgbot.on(events.NewMessage(incoming=True, chats=FROM))
async def _(event):
    for i in TO:

        try:
            if event.poll:
                return
            if event.photo:
                photo = event.media.photo
                log.info(f"Forwarded a message from {FROM} to {TO} (Media.Photo)")
                await datgbot.send_file(
                    i, photo, caption=event.text, link_preview=False
                )
            elif event.media:
                try:
                    if event.media.webpage:
                        log.info(f"Forwarded a message from {FROM} to {TO} (Media.Webpage)")
                        await datgbot.send_message(
                            i, event.text, link_preview=False
                        )
                except Exception:
                    media = event.media.document
                    log.info(f"Forwarded a message from {FROM} to {TO} (Media.Document)")
                    await datgbot.send_file(
                        i, media, caption=event.text, link_preview=False
                    )
                finally:
                    return
            else:
                log.info(f"Forwarded a message from {FROM} to {TO}")
                await datgbot.send_message(i, event.text, link_preview=False)
        except FloodWait as fw:
            await datgbot.send_message(sender, f'You have floodwaits of {fw.value} seconds, cancelling batch') 
        except Exception as exc:
            log.error(
                "TO_CHANNEL ID is wrong or I can't send messages there (make me admin).\nTraceback:\n%s",
                exc,
            )


# ----------------------------------------------------------------------------------------------

log.info("Bot has started.")

datgbot.run_until_disconnected()
