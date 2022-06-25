import hikari
import lightbulb
import miru
from bot_view import TestButton, JournalNavButton
from miru.ext import nav
import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
ENABLED_GUILD = int(os.getenv('ENABLED_GUILD'))

bot = lightbulb.BotApp(
    token=DISCORD_TOKEN,
    default_enabled_guilds=ENABLED_GUILD
)

miru.load(bot)

"""
Sample bot functions
"""

@bot.listen(hikari.StartedEvent)
async def on_started(event):
    print('Bot has started!')

@bot.command
@lightbulb.command('ping', 'Says ribbit!')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context):
    message = await ctx.respond('Ribbit!')

@bot.command
@lightbulb.command('pag', 'test paginate')
@lightbulb.implements(lightbulb.SlashCommand)
async def navigator(ctx: lightbulb.Context) -> None:
    embed = hikari.Embed(title="I'm the second page!", description="Also an embed!")
    pages = ["I'm a customized navigator!", embed, "I'm the last page!"]
    # Define our custom buttons for this navigator, keep in mind the order
    # All navigator buttons MUST subclass nav.NavButton
    buttons = [nav.PrevButton(), nav.StopButton(), nav.NextButton(), JournalNavButton()]
    # Pass our list of NavButton to the navigator
    navigator = nav.NavigatorView(pages=pages, buttons=buttons)

    await navigator.send(ctx.channel_id)

@bot.command
@lightbulb.command('group', 'This is a group')
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def my_group(ctx: lightbulb.Context):
    pass

@my_group.child
@lightbulb.command('subcommand', 'This is a subcommand')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def subcommand(ctx: lightbulb.Context):
    await ctx.respond('I am a subcommand!')

@bot.command
@lightbulb.option('num1', 'The first number', type=int)
@lightbulb.option('num2', 'The second number', type=int)
@lightbulb.command('add', 'Add two numbers together')
@lightbulb.implements(lightbulb.SlashCommand)
async def add(ctx: lightbulb.Context):
    await ctx.respond(ctx.options.num1 + ctx.options.num2)

@bot.listen()
async def on_starting(event: hikari.StartingEvent) -> None:
    pass

@bot.listen()
async def on_stopping(event: hikari.StoppingEvent) -> None:
    pass

bot.load_extensions_from("./extensions/")

bot.run()