import discord
from discord import ui
from ..utils.event import Event

class Summary(ui.Modal):

    def __init__(self):
        super().__init__(title="Bilan de séance")

    message = ui.TextInput(
        label="Message",
        style=discord.TextStyle.long,
        required=False
    )

    async def on_submit(self, interaction: discord.Interaction):
        """
        Appelée lorsque l'utilisateur valide son entrée dans la modale

        Args:
            interaction : interaction
        """
        await Event.send_summary(
            interaction = interaction,
            message = self.message.value
        )