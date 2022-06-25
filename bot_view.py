import hikari
import miru
from miru.ext import nav


class TestButton(miru.View):

    @miru.button(label="Test Button", emoji=chr(129704), style=hikari.ButtonStyle.PRIMARY)
    async def test_button(self, button: miru.Button, ctx: miru.Context) -> None:
        await ctx.respond("Success!")

class JournalNavButton(nav.NavButton):
    def __init__(self):
        super().__init__(label="Page: 1", row=1)

    async def callback(self, ctx: miru.Context) -> None:
        await ctx.respond("You clicked me!", flags=hikari.MessageFlag.EPHEMERAL)

    async def before_page_change(self) -> None:
        # This function is called before the new page is sent by
        # NavigatorView.send_page()
        self.label = f"Page: {self.view.current_page+1}"

class FrogNavButton(nav.NavButton):
    def __init__(self):
        super().__init__(emoji=chr(128056), row=0)

    async def callback(self, ctx: miru.Context) -> None:
        await ctx.respond("Ribbit!", flags=hikari.MessageFlag.EPHEMERAL)

