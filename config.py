# ------------------------------------------------------------------------------------------------------------
# Directly filled with needed infos
# ------------------------------------------------------------------------------------------------------------

from os import getenv

# @EmilySweetyBabe
# API_ID = int(getenv("API_ID", "20586238"))
API_ID = getenv("API_ID", "20586238")
API_HASH = getenv("API_HASH", "5accd362e03a50741b7d0c5623acfcb9")

# ForwarderBot
# @ForwarderTimBot
BOT_TOKEN = getenv("BOT_TOKEN", "6025839502:AAFgHIWJ_E3K4Xg5qsqwoYqE-GcuSwWBz_4")

# The IDs of the main channel from where posts have to be copied
# eg: `-100xxxx -100yyyy -100abcd ...`
FROM_CHANNEL = getenv("FROM_CHANNEL", "")

# The ID of the channel to which the posts are to be sent, split by space. 
# eg: `-100xxxx -100yyyy -100abcd ...`
TO_CHANNEL = getenv("TO_CHANNEL", "")