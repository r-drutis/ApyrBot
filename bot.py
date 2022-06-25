import hikari
import lightbulb
import miru
from bot_view import TestButton, JournalNavButton
from miru.ext import nav



bot = lightbulb.BotApp(
    token='OTQyNTc0OTQyNjk0ODE3ODYy.YgmfUg.s06VGMvPGoQkjQM_B_gJdw5ddrE',
    default_enabled_guilds=(942572518903009341)
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
@lightbulb.command('button', 'Test Button!')
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_sus_button(ctx: lightbulb.Context) -> None:
    view = TestButton()
    message = await ctx.respond("Test button", components=view.build())
    msg = await message.message()
    view.start(msg)
    await view.wait()

@bot.command
@lightbulb.command('pag', 'test paginate')
@lightbulb.implements(lightbulb.SlashCommand)
async def navigator(ctx: lightbulb.Context) -> None:
    view = JournalNavButton()
    embed = hikari.Embed(title="I'm the second page!", description="Also an embed!")
    pages = ["I'm a customized navigator!", embed, "I'm the last page!"]
    # Define our custom buttons for this navigator, keep in mind the order
    # All navigator buttons MUST subclass nav.NavButton
    buttons = [nav.PrevButton(), nav.StopButton(), nav.NextButton(), JournalNavButton()]
    # Pass our list of NavButton to the navigator
    navigator = nav.NavigatorView(pages=pages, buttons=buttons)

    await navigator.send(ctx.channel_id)

@bot.command
@lightbulb.command('embed-test', 'prints an embed')
@lightbulb.implements(lightbulb.SlashCommand)
async def embed_test(ctx: lightbulb.Context):
    ipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris ultrices felis vel leo venenatis tempor. Nunc imperdiet neque sed neque pharetra rhoncus. Nulla arcu neque, tincidunt ut justo a, eleifend venenatis sem. Donec finibus metus a neque pretium, aliquet pulvinar ante gravida. Aliquam laoreet nunc nisl, id iaculis massa tempus et. Donec sodales lorem id lorem sagittis dictum. Aenean molestie convallis lorem quis ultricies. Ut sit amet imperdiet massa. Nulla euismod bibendum leo, in imperdiet nunc porttitor eget. Praesent in neque nec mauris interdum blandit. Praesent finibus dictum lorem, non consequat augue vulputate eu. Donec semper, lorem quis tempor euismod, dui lacus convallis libero, in lacinia nisi libero eu magna. Vestibulum ultrices eros nec luctus euismod. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean hendrerit ut mi ac venenatis. "

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