from ..extensions.message import Message
from discord import HTTPException
import discord
from ..config import config
from .embed import Embed
from ..extensions.member import Member
from datetime import datetime
import time


class Event:
    async def send_message(interaction, **kwargs):
        """
        Envoi un message

        Args:
            interaction : interaction
        """
        try:
            await interaction.response.send_message(**kwargs)
            message_content = await interaction.original_response()
            return Message(content=message_content)
        except HTTPException as e:
            print(e)

    async def send_question_with_reactions(interaction, embed, reactions):
        """
        Envoi un questionnaire et ajoute les possibilités (reactionss) de votes

        Args:
            interaction : interaction
            embed : modele de reponse
            reactions : liste des reactions
        """
        message = await Event.send_message(interaction=interaction, embed=embed, ephemeral=False)
        await message.add_reactions(reactions=reactions)
        return message 

    async def send_weather_results(interaction, message):
        """
        Envoi le resultat de la méteo dans chaque cannaux de projet

        Args:
            interaction : interaction
            message : questionnaire méteo
        """
        reactions_by_project = await message.get_reactions_by_project()
        for project_name, channel_name in config.map_projects_channels.items():
            channel = discord.utils.get(interaction.guild.text_channels, name=channel_name)
            if not channel:
                continue
            embed = Embed.get_weather(
                title=f"Résultat météo",
                reactions_count=reactions_by_project.get(project_name, None)
            )
            await channel.send(embed=embed)

    async def send_summary(interaction, message):
        """
        Stock le bilan de séance de l'utilisateur pour la session

        Args:
            interaction : interaction
            message : bilan de la séances
        """
        author = Member(user=interaction.user)        
        interaction.client.session.add_summary(author=author, message=message)

        embed = Embed.get(description='Le bilan a été transmis')
        await Event.send_message(interaction=interaction, embed=embed, ephemeral=True)

    async def send_summaries(interaction):
        """
        Distribues dans les cannaux de chaque projet
        le bilan global de la séance

        Args:
            interaction : interaction
            message : bilan de la séances
        """
        session_duration = (datetime.now() - interaction.client.session.start)
        session_duration_seconds = time.gmtime(session_duration.total_seconds())
        formated_session_duration = time.strftime('%H:%M', session_duration_seconds)
        
        summaries = interaction.client.session.summaries
        for project_name, channel_name in config.map_projects_channels.items():
            channel = discord.utils.get(interaction.guild.text_channels, name=channel_name)
            if not channel:
                continue

            embed = Embed.get(
                title=f"Séance du {interaction.client.session.start.strftime('%d-%m-%y %H:%M')} ({formated_session_duration}) | Bilan"
            )
            for summary in summaries:
                if project_name != summary.author.project:
                    continue

                if summary.author.function:
                    title = f"{summary.author.user.nick} - {summary.author.function}"
                else:
                    title = summary.author.user.nick
                embed.add_field(name=title, value=summary.message, inline=False)
            await channel.send(embed=embed)