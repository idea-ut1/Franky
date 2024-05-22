import discord
from .members import Members
from ..config import config 


class Message:
    def __init__(self, content):
        self.content = content

    async def get_reactions(self):
        """
        Retourne un dictionnaire contenant en :
        clef : une reaction (un emoji)
        valeurs : un objets membres qui contient les utilisateurs ayant votés
        
        Returns:
            dict: utilisateurs par reaction
        """
        res = {}
        for reaction in self.content.reactions:
            users = [user async for user in reaction.users() if not user.bot]
            res[reaction.emoji] = Members(users=users)
        return res

    async def get_reactions_by_project(self):
        """
        Retourne un dictionnaire contenant en :
        clef : projet
        valeurs : compte des reactions par emoji
        
        Returns:
            dict: reactions par projet
        """
        reactions = await self.get_reactions()

        reactions_by_project = {
            project : {reaction_emoji : 0 for reaction_emoji in reactions.keys()}
            for project in config.projects
        }

        for emoji, members in reactions.items():
            for member in members:
                if member.project in config.projects:
                    reactions_by_project[member.project][emoji] += 1

        return reactions_by_project

    async def add_reaction(self, reaction):
        """
        Ajoute une reaction a un message

        Args:
            reaction : emoji
        """
        try:
            await self.content.add_reaction(reaction)
        except discord.errors.HTTPException as error:
            print(f"Echec lors de l'ajout de la reaction: {reaction} : erreur {error}")

    async def add_reactions(self, reactions):
        """
        Ajoute des reactions a un message

        Args:
            reactions : list emoji
        """
        for reaction in reactions:
            await self.add_reaction(reaction)