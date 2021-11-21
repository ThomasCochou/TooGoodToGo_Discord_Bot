from tgtg import TgtgClient
from decouple import config

import discordClient
import discordCog

TGTG_TOKEN = config('TGTG_TOKEN')
TGTG_REFRESH_TOKEN = config('TGTG_REFRESH_TOKEN')
USER_ID = config('USER_ID')

DISCORD_TOKEN = config('DISCORD_TOKEN')

tgtg_client = TgtgClient(access_token=TGTG_TOKEN, refresh_token=TGTG_REFRESH_TOKEN, user_id=USER_ID)

discord_client = discordClient.discordClient()

discord_client.create_tgtg_client(tgtg_client)

discord_cog = discordCog.discordCog(discord_client)

discord_client.run(DISCORD_TOKEN)