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


# This function queries the Roll20 external journal and returns the journal info in a discord navigator view embed
# term: The journal entry name that is being queried
# Sends a navigator view with roll20 journal info and navigation buttons to discord channel

@apyr_group.child
@lightbulb.option('term', 'The term you want me to search for')
@lightbulb.command("what-is", "Search for something in the roll20 journal")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def whatis_subcommand(ctx: lightbulb.Context) -> None:
    await ctx.respond("You want to know what \"{0}\" is? Let me check the archives for you...".format(ctx.options.term))
    info = retrieve_query_from_journal(ctx.options.term)
    # The journal entry is returned as a paginated discord embed with page navigation buttons and thumbnail image.
    if info:
        await ctx.respond("Here is what I found:\n")
        # Build the embed pages and navigator view
        pages = build_embed_list(info, ctx)
        buttons = [nav.FirstButton(), nav.PrevButton(), FrogNavButton(), nav.NextButton(),nav.LastButton(), nav.IndicatorButton()]
        navigator = nav.NavigatorView(pages=pages, buttons=buttons)
        # Send the navigator view to the discord channel
        await navigator.send(ctx.channel_id)
    # If no entry is found, it responds and tells the user nothing was found.
    else:
        await ctx.respond("I wasn't able to find anything by that name. Ribbit.")


# This function builds a list of embed pages which contain the Roll20 Journal search results.
# info: The journal text, title, and avatar scraped from the roll20 external journal entry
# Returns a list of discord embed pages containing roll20 journal info

def build_embed_list(info, ctx):
    # Paginate text retrieved from roll20 entry
    desc = "".join(info["text"])
    pag = StringPaginator(max_lines=6)
    embed_list = []
    for line in desc.splitlines():
        pag.add_line(f"{line}")
    # Create an embed with title, footer, and thumbnail for each page
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

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(journal_plugin)