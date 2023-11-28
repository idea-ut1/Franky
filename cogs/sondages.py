# test zaefef

import platform
import random

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class Sondages(commands.Cog, name="sondages"):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.hybrid_command(
        name="weather",
        description="Obtenez la météo avec des réactions emoji prédéfinies.",
    )
    async def weather(self, context: Context, groupe: str = "everyone") -> None:
        """
        Obtenez la météo avec des réactions emoji prédéfinies.
        En mentionnant le groupe d'utilsateur que vous voulez notifier, par défaut c'est @everyone

        :param context: Le contexte de la commande hybride.
        """
        # Envoyer la demande de météo
        message = await context.send(f'Quelle est votre météo du jour ? {groupe}! \n\n ☀️ : Je suis de très bonne humeur\n ⛅ : Je suis de bonne humeur\n ☁️ : Je suis neutre\n 🌧️ : Je suis de mauvaise humeur\n ⚡ : Je suis de très mauvaise humeur\n\n')

        # Ajouter des réactions emoji au message
        emojis = ['☀️', '⛅', '☁️', '🌧️', '⚡']

        for emoji in emojis:
            await message.add_reaction(emoji)


async def setup(bot) -> None:
    await bot.add_cog(Sondages(bot))
