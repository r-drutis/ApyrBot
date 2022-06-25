import hikari
import lightbulb
import miru
import os
from dotenv import load_dotenv

# Load discord environment into bot
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
ENABLED_GUILD = int(os.getenv('ENABLED_GUILD'))

bot = lightbulb.BotApp(
    token=DISCORD_TOKEN,
    default_enabled_guilds=ENABLED_GUILD
)
miru.load(bot)

@bot.listen(hikari.StartedEvent)
async def on_started(event):
    print('Bot has started!')

# Ping command to check if the bot is running
@bot.command
@lightbulb.command('ping', 'Says ribbit!')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context):
    await ctx.respond('Ribbit!')

# Load journal related commands and functions into bot
bot.load_extensions_from("./extensions/")
bot.run()