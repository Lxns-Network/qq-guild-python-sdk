from qq_guild.application import GuildBot
from qq_guild.models.ws import Intents

import os

bot = GuildBot(
    app_id=os.environ.get("BOT_ID"),
    token=os.environ.get("BOT_TOKEN"),
    sandbox=False,
    intents=Intents(
        atMessages=True,
        directMessage=True
    )
)

@bot.receiver("READY")
async def on_ready(bot: GuildBot, data):
    print(await bot.get_me())

@bot.receiver("AT_MESSAGE_CREATE")
async def on_message(bot: GuildBot, data):
    await bot.send_message(data.channel_id, message_id=data.id, content=f"<@{data.author.id}> 你好~")

@bot.receiver("DIRECT_MESSAGE_CREATE")
async def on_message(bot: GuildBot, data):
    await bot.send_direct_message(data.guild_id, message_id=data.id, content="你好~")

bot.run()