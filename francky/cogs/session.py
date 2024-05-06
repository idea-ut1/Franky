import discord
from discord.ext import commands
from discord import app_commands
from ..modals.summary import Summary as SummaryView
from..utils.session import Session as DataSession
from ..utils.event import Event

class Session(commands.Cog):
    """
    Un cog Discord pour gérer les séances de cours

    Attributes:
        bot (commands.Bot): L'instance du bot qui exécute ce cog.
    """
    group = discord.app_commands.Group(name="session", description="Commande liée à la séance")
    
    def __init__(self, bot):
        self.bot = bot  

    async def _check_if_session_exist(self, interaction: discord.Interaction):
        """
        Vérifie si une séance est en cours.

        Args:
            interaction : L'interaction Discord qui a déclenché la vérification.

        Returns:
            bool: True si une séance est en cours, False sinon.
        """
        if not self.bot.session:
            await interaction.response.send_message("Aucune séance n'est en cours.", ephemeral=True)
            return False
        else:
            return True

    @group.command(name='start', description='Démarre une séance')
    async def start(self, interaction: discord.Interaction):
        """
        Démarre une nouvelle séance et de permet de stocker
        les informations de la séance (les bilans de chacun par exemple).

        Args:
            interaction : L'interaction Discord qui a déclenché la commande.
        """
        self.bot.session = DataSession()
        await interaction.response.send_message("La séance démarre.", ephemeral=True)

    @group.command(name='stop', description='Clos une séance')
    async def stop(self, interaction: discord.Interaction):
        """
        Termine la séance en cours si elle existe
        et envoie les résumés des séances par projets.

        Args:
            interaction : L'interaction Discord qui a déclenché la commande.
        """
        is_session = await self._check_if_session_exist(interaction=interaction)
        if not is_session:
            return
        await Event.send_summaries(interaction=interaction)        
        self.bot.session = None
        await interaction.response.send_message("La session est terminé", ephemeral=True)

    @app_commands.command(name='summary', description='Bilan de la séance')
    async def summary(self, interaction: discord.Interaction):
        """
        Lance un bilan de la séance en cours à travers une interface modale si une séance est active.

        Args:
            interaction (discord.Interaction): L'interaction Discord qui a déclenché la commande.
        """
        is_session = await self._check_if_session_exist(interaction=interaction)
        if not is_session:
            return
        await interaction.response.send_modal(SummaryView())

async def setup(bot):
    cog = Session(bot)
    await bot.add_cog(cog)
    bot.tree.add_command(cog.group, guild=discord.Object(id=bot.guild_id))
    bot.tree.add_command(cog.summary, guild=discord.Object(id=bot.guild_id))