import hikari
import miru
from miru.ext import nav


# Journal Navigation related buttons

# This button responds with "Ribbit" when clicked
# It is not meant to do anything, it's just an easter egg
class FrogNavButton(nav.NavButton):
    def __init__(self):
        super().__init__(emoji=chr(128056), row=0)

    async def callback(self, ctx: miru.Context) -> None:
        # The message is ephemeral, so only the person who clicked it can see the message
        await ctx.respond("Ribbit!", flags=hikari.MessageFlag.EPHEMERAL)