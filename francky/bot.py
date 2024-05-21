import discord
from discord.ext import commands
from . import PROJECT_NAME, COGS_NAME
from .extensions.members import Members


class Bot(commands.Bot):
    def __init__(self, command_prefix, intents, guild_id):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.guild_id = guild_id
        self.guild_members = None
        self.session = None

    async def on_ready(self):
        """
        Appelé au demarrage du bot
        """
        print(f'Connecté en tant que {self.user.name} (ID: {self.user.id})')
        guild = discord.Object(id=self.guild_id)
        await self.tree.sync(guild=guild)
        self.guild_members = await self.fetch_members()
        print('------')


    async def on_member_remove(self, member):
        """
        Appelé lorsque un membre quitte le serveur 

        args:
            member : (object discord.member) membre
        """
        self.guild_members.remove_with_user_id(
            id = member.id
        )
        
    async def on_member_join(self, member): 
        """
        Appelé lorsque un membre rejoint le serveur 
        
        args:
            member : (object discord.member) membre
        """
        self.guild_members.add(user=member)

    async def on_member_update(self, before, after):
        """
        Appelé lorsque un membre est mis à jour 
        
        args : 
            before : (object discord.member) membre
            after : (object discord.member) membre
        """
        self.guild_members.remove_with_user_id(
            id = before.id
        )
        self.guild_members.add(user=after)

    async def setup_hook(self):
        """
        Appelé au setup (connecte les commandes)
        """
        files = ["poll", "session"]
        for file in files:
            cog = f'{PROJECT_NAME}.{COGS_NAME}.{file}'

            await self.load_extension(cog)

    async def fetch_members(self):
        """
        Retrouve l'ensemble des membres du serveur

        returns:
            Members : objet contenant l'ensemble des membres du serveur
        """
        try:
            guild = await self.fetch_guild(self.guild_id)
            members = [
                member async for member in guild.fetch_members()
                if not member.bot
            ]
        except Exception as e:
            print(f"Erreurs lors de la recherche des membres : {e}")
            members = []
        finally:
            return Members(users=members)