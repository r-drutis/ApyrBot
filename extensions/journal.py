import hikari
import lightbulb
from webscraper import retrieve_query_from_journal
from lightbulb.utils.pag import StringPaginator
from journal_view import FrogNavButton
from miru.ext import nav

journal_plugin = lightbulb.Plugin("Journal")

@journal_plugin.command
@lightbulb.command("apyr", "Tell me what you want to know, and I will see what I can find...")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def apyr_group(ctx: lightbulb.Context) -> None:
    pass  # as slash commands cannot have their top-level command ran, we simply pass here

"""
Search Roll20 External Journal

This command accepts a search term and then navigates to the roll20 external journal and retrieves the journal entry 
for that search term.

The journal entry is returned as a paginated discord embed with page navigation buttons and thumbnail image.

If no entry is found, it responds and tells the user nothing was found.
"""

@apyr_group.child
@lightbulb.option('term', 'The term you want me to search for')
@lightbulb.command("what-is", "Search for something in the roll20 journal")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def whatis_subcommand(ctx: lightbulb.Context) -> None:
    await ctx.respond("You want to know what \"{0}\" is? Let me check the archives for you...".format(ctx.options.term))
    info = retrieve_query_from_journal(ctx.options.term)
    if info:
        await ctx.respond("Here is what I found:\n")
        # Build the embed and navigator view
        pages = build_embed_list(info, ctx)
        buttons = [nav.FirstButton(), nav.PrevButton(), FrogNavButton(), nav.NextButton(),nav.LastButton(), nav.IndicatorButton()]
        navigator = nav.NavigatorView(pages=pages, buttons=buttons)
        # Send the navigator view to the discord channel
        await navigator.send(ctx.channel_id)
    else:
        await ctx.respond("I wasn't able to find anything by that name. Ribbit.")

def build_embed_list(info, ctx):
    desc = "".join(info["text"])
    pag = StringPaginator(max_lines=6)
    embed_list = []
    for line in desc.splitlines():
        pag.add_line(f"{line}")
    for page in pag.build_pages():
        embed = hikari.Embed(
            title=info["title"],
            description=page,
            colour=0x3B9DFF
        ).set_footer(
            text=f"Requested by {ctx.member.display_name}",
            icon=ctx.member.avatar_url or ctx.member.default_avatar_url,
        ).set_thumbnail(info["avatar"])
        embed_list.append(embed)
    return embed_list

def build_embed(info, ctx):
    embed = hikari.Embed(
        title=info["title"],
        description="".join(info["text"]),
        colour=0x3B9DFF
    ).set_footer(
        text=f"Requested by {ctx.member.display_name}",
        icon=ctx.member.avatar_url or ctx.member.default_avatar_url,
    ).set_thumbnail(info["avatar"])
    return embed

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(journal_plugin)