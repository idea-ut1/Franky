import discord
from discord.ext import commands
from discord import app_commands
from ..modals.question import Question
from ..utils.event import Event
from ..utils.embed import Embed
from ..utils.server import Server
import asyncio

class Poll(commands.Cog):
    """
    Un cog Discord afin de créer et gérer des sondages interactifs.
    
    Attributes:
        bot: Instance du bot Discord.
    """

    def __init__(self, bot):
        self.bot = bot  


    @app_commands.command(name='question', description='Crée une question et ajoute des réactions personnalisées')
    @app_commands.describe(reactions='(optionnal)')
    async def question(self, interaction: discord.Interaction, reactions: str = None):
        """
        Crée une question interactive et envoie un modal pour recueillir la réponse de l'utilisateur.
        Les réactions personnalisées peuvent être spécifiées comme une chaîne de caractères optionnelle.
        
        Args:
            interaction: L'interaction Discord qui déclenche la commande.
            reactions: Une chaîne de caractères spécifiant les réactions à ajouter à la question (optionnel).
        """
        await interaction.response.send_modal(Question(reactions))

    @app_commands.command(name='weather', description='Crée un sondage météo')
    @app_commands.describe(delay="Delais d'envoi du resultat en seconde, par défaut 600s (10 min)")
    async def weather(self, interaction: discord.Interaction, delay: int = 600):
        """
        Lance un sondage interactif avec un délai avant d'envoyer le résultat.
        
        Args:
            interaction: L'interaction Discord qui déclenche la commande.
            delay: Le délai en secondes avant d'envoyer le résultat du sondage (par défaut 600 secondes soit 10 minutes).
        """
        response_embed = Embed.get(
            title = 'Quel est la météo du jour ?',
            description = '''
            🌞 : soleil
            🌥️ : moyen
            ☁️ : nuageux
            🌩️ : eclair
            '''
        )
        reactions = ['🌞', '🌥️', '☁️', '🌩️']

        # envoi du sondage
        message = await Event.send_question_with_reactions(
            interaction = interaction,
            embed=response_embed,
            reactions=reactions
        )

        await asyncio.sleep(delay)

        # recuperation du message rafraichit (pour les nouvelles reactions)
        message = await Server.find_message_by_message_id(
            interaction=interaction,
            message_id=message.content.id
        )
        # envoi des resultats 
        await Event.send_weather_results(
            interaction=interaction,
            message=message
        )


async def setup(bot):
    cog = Poll(bot)
    await bot.add_cog(cog)
    bot.tree.add_command(cog.question, guild=discord.Object(id=bot.guild_id))
    bot.tree.add_command(cog.weather, guild=discord.Object(id=bot.guild_id))