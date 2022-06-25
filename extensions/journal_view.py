import hikari
import miru
from miru.ext import nav

"""
Journal Navigation related buttons
"""

class FrogNavButton(nav.NavButton):
    def __init__(self):
        super().__init__(emoji=chr(128056), row=0)

    async def callback(self, ctx: miru.Context) -> None:
        await ctx.respond("Ribbit!", flags=hikari.MessageFlag.EPHEMERAL)

