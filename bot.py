import json
import logging
import os
import platform
import random
import sys

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context
from dotenv import load_dotenv

if not os.path.isfile(f"{os.path.realpath(os.path.dirname(__file__))}/config.json"):
    sys.exit("'config.json' introuvable ! Veuillez l'ajouter et réessayer.")
else:
    with open(f"{os.path.realpath(os.path.dirname(__file__))}/config.json") as file:
        config = json.load(file)

"""	
Configurer les intents du bot (restrictions des événements)
Pour plus d'informations sur les intents, veuillez consulter les sites suivants :
https://discordpy.readthedocs.io/en/latest/intents.html
https://discordpy.readthedocs.io/en/latest/intents.html#privileged-intents

Intents par défaut :
intents.bans = True
intents.dm_messages = True
intents.dm_reactions = True
intents.dm_typing = True
intents.emojis = True
intents.emojis_and_stickers = True
intents.guild_messages = True
intents.guild_reactions = True
intents.guild_scheduled_events = True
intents.guild_typing = True
intents.guilds = True
intents.integrations = True
intents.invites = True
intents.messages = True # `message_content` est requis pour obtenir le contenu des messages
intents.reactions = True
intents.typing = True
intents.voice_states = True
intents.webhooks = True

Intents privilégiés (doivent être activés sur le portail des développeurs Discord), veuillez les utiliser uniquement si vous en avez besoin :
intents.members = True
intents.message_content = True
intents.presences = True
"""

intents = discord.Intents.all()

"""
Décommentez ceci si vous souhaitez utiliser des commandes préfixées (normales).
Il est recommandé d'utiliser des commandes slash et de ne pas utiliser de commandes préfixées.

Si vous souhaitez utiliser des commandes préfixées, assurez-vous également d'activer l'intent ci-dessous dans le portail des développeurs de Discord.
"""
# intents.message_content = True

# Configuration des deux enregistreurs


class LoggingFormatter(logging.Formatter):
    # Couleurs
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    # Styles
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    def format(self, record):
        log_color = self.COLORS[record.levelno]
        format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format = format.replace("(black)", self.black + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)

# Gestionnaire de console
console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())
# Gestionnaire de fichier
file_handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
file_handler_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-d %H:%M:%S", style="{"
)
file_handler.setFormatter(file_handler_formatter)

# Ajout des gestionnaires
logger.addHandler(console_handler)
logger.addHandler(file_handler)


class DiscordBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or(config["prefix"]),
            intents=intents,
            help_command=None,
        )
        """
        Cela crée des variables de bot personnalisées pour que nous puissions accéder plus facilement à ces variables dans les cogs.

        Par exemple, la configuration est disponible en utilisant le code suivant :
        - self.config # Dans cette classe
        - bot.config # Dans ce fichier
        - self.bot.config # Dans les cogs
        """
        self.logger = logger
        self.config = config

    async def load_cogs(self) -> None:
        """
        Le code de cette fonction est exécuté chaque fois que le bot démarre.
        """
        for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await self.load_extension(f"cogs.{extension}")
                    self.logger.info(f"Extension chargée : '{extension}'")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    self.logger.error(
                        f"Échec du chargement de l'extension {extension}\n{exception}"
                    )

    @tasks.loop(minutes=1.0)
    async def status_task(self) -> None:
        """
        Configuration de la tâche de statut du jeu du bot.
        """
        statuses = ["avec vous!", "avec IDeA!", "avec la MIAGE!"]
        await self.change_presence(activity=discord.Game(random.choice(statuses)))

    @status_task.before_loop
    async def before_status_task(self) -> None:
        """
        Avant de commencer la tâche de modification du statut, nous nous assurons que le bot est prêt.
        """
        await self.wait_until_ready()

    async def setup_hook(self) -> None:
        """
        Ceci sera exécuté uniquement lorsque le bot démarre pour la première fois.
        """
        self.logger.info(f"Connecté en tant que {self.user.name}")
        self.logger.info(f"Version de l'API discord.py : {discord.__version__}")
        self.logger.info(f"Version de Python : {platform.python_version()}")
        self.logger.info(
            f"Exécuté sur : {platform.system()} {platform.release()} ({os.name})"
        )
        self.logger.info("-------------------")
        await self.load_cogs()
        self.status_task.start()

    async def on_message(self, message: discord.Message) -> None:
        """
        Le code de cet événement est exécuté à chaque fois que quelqu'un envoie un message, avec ou sans préfixe.

        :param message: Le message qui a été envoyé.
        """
        if message.author == self.user or message.author.bot:
            return
        await self.process_commands(message)

    async def on_command_completion(self, context: Context) -> None:
        """
        Le code de cet événement est exécuté chaque fois qu'une commande normale a été exécutée avec succès.

        :param context: Le contexte de la commande qui a été exécutée.
        """
        full_command_name = context.command.qualified_name
        split = full_command_name.split(" ")
        executed_command = str(split[0])
        if context.guild is not None:
            self.logger.info(
                f"Commande {executed_command} exécutée dans {context.guild.name} (ID : {context.guild.id}) par {context.author} (ID : {context.author.id})"
            )
        else:
            self.logger.info(
                f"Commande {executed_command} exécutée par {context.author} (ID : {context.author.id}) en messages privés"
            )

    async def on_command_error(self, context: Context, error) -> None:
        """
        Le code de cet événement est exécuté chaque fois qu'une commande normale valide génère une erreur.

        :param context: Le contexte de la commande normale qui n'a pas réussi à s'exécuter.
        :param error: L'erreur qui a été rencontrée.
        """
        if isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            embed = discord.Embed(
                description=f"**Veuillez ralentir** - Vous pouvez réutiliser cette commande dans {f'{round(hours)} heures' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} secondes' if round(seconds) > 0 else ''}.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                description="Vous n'êtes pas le propriétaire du bot !", color=0xE02B2B
            )
            await context.send(embed=embed)
            if context.guild:
                self.logger.warning(
                    f"{context.author} (ID : {context.author.id}) a essayé d'exécuter une commande réservée aux propriétaires dans la guilde {context.guild.name} (ID : {context.guild.id}), mais l'utilisateur n'est pas propriétaire du bot."
                )
            else:
                self.logger.warning(
                    f"{context.author} (ID : {context.author.id}) a essayé d'exécuter une commande réservée aux propriétaires dans les messages privés du bot, mais l'utilisateur n'est pas propriétaire du bot."
                )
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description="Vous n'avez pas la (les) permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` pour exécuter cette commande !",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                description="Je n'ai pas la (les) permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` pour exécuter pleinement cette commande !",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Erreur !",
                # Nous devons mettre en majuscule car les arguments de la commande n'ont pas de lettre majuscule dans le code et ce sont les premiers mots dans le message d'erreur.
                description=str(error).capitalize(),
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        else:
            raise error


load_dotenv()

bot = DiscordBot()
bot.run(os.getenv("TOKEN"))
print('a')
