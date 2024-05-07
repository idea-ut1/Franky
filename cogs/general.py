# test zaefef

import platform
import random

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class General(commands.Cog, name="general"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.context_menu_user = app_commands.ContextMenu(
            name="Obtenir l'ID", callback=self.grab_id
        )
        self.bot.tree.add_command(self.context_menu_user)
        self.context_menu_message = app_commands.ContextMenu(
            name="Supprimer les spoilers", callback=self.remove_spoilers
        )
        self.bot.tree.add_command(self.context_menu_message)

    # Message context menu command
    async def remove_spoilers(
        self, interaction: discord.Interaction, message: discord.Message
    ) -> None:
        """
        Supprime les spoilers du message. Cette commande nécessite l'intention MESSAGE_CONTENT pour fonctionner correctement.

        :param interaction: L'interaction de la commande d'application.
        :param message: Le message avec lequel il y a une interaction.
        """
        spoiler_attachment = None
        for attachment in message.attachments:
            if attachment.is_spoiler():
                spoiler_attachment = attachment
                break
        embed = discord.Embed(
            title="Message sans spoilers",
            description=message.content.replace("||", ""),
            color=0xBEBEFE,
        )
        if spoiler_attachment is not None:
            embed.set_image(url=attachment.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # User context menu command
    async def grab_id(
        self, interaction: discord.Interaction, user: discord.User
    ) -> None:
        """
        Récupère l'ID de l'utilisateur.

        :param interaction: L'interaction de la commande d'application.
        :param user: L'utilisateur avec lequel il y a une interaction.
        """
        embed = discord.Embed(
            description=f"L'ID de {user.mention} est `{user.id}`.",
            color=0xBEBEFE,
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.hybrid_command(
        name="aide", description="Liste toutes les commandes chargées du bot."
    )
    async def aide(self, context: Context) -> None:
        prefix = self.bot.config["prefix"]
        embed = discord.Embed(
            title="Aide", description="Liste des commandes disponibles :", color=0xBEBEFE
        )
        for i in self.bot.cogs:
            if i == "owner" and not (await self.bot.is_owner(context.author)):
                continue
            cog = self.bot.get_cog(i.lower())
            commands = cog.get_commands()
            data = []
            for command in commands:
                description = command.description.partition("\n")[0]
                data.append(f"{prefix}{command.name} - {description}")
            help_text = "\n".join(data)
            embed.add_field(
                name=i.capitalize(), value=f"```{help_text}```", inline=False
            )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="informations",
        description="Obtenez des informations utiles (ou non) sur le bot.",
    )
    async def informations_bot(self, context: Context) -> None:
        """
        Obtenez des informations utiles (ou non) sur le bot.

        :param context: Le contexte de la commande hybride.
        """
        embed = discord.Embed(
            description="Aides les étudiants en MIAGE de IDeA à ne pas faire de la merde.",
            color=0xBEBEFE,
        )
        embed.set_author(name="Informations sur le bot")
        embed.add_field(name="Propriétaire:", value="dey_bite_heure", inline=True)
        embed.add_field(
            name="Version de Python:", value=f"{platform.python_version()}", inline=True
        )
        embed.add_field(
            name="Préfixe:",
            value=f"{self.bot.config['prefix']} pour les commandes normales",
            inline=False,
        )
        embed.set_footer(text=f"Demandé par {context.author}")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="infosserveur",
        description="Obtenez des informations utiles (ou non) sur le serveur.",
    )
    async def informations_serveur(self, context: Context) -> None:
        """
        Obtenez des informations utiles (ou non) sur le serveur.

        :param context: Le contexte de la commande hybride.
        """
        roles = [role.name for role in context.guild.roles]
        if len(roles) > 50:
            roles = roles[:50]
            roles.append(f">>>> Affichage [50/{len(roles)}] Rôles")
        roles = ", ".join(roles)

        embed = discord.Embed(
            title="**Nom du serveur :**", description=f"{context.guild}", color=0xBEBEFE
        )
        if context.guild.icon is not None:
            embed.set_thumbnail(url=context.guild.icon.url)
        embed.add_field(name="ID du serveur", value=context.guild.id)
        embed.add_field(name="Nombre de membres", value=context.guild.member_count)
        embed.add_field(
            name="Salons textuels/voix", value=f"{len(context.guild.channels)}"
        )
        embed.add_field(name=f"Rôles ({len(context.guild.roles)})", value=roles)
        embed.set_footer(text=f"Créé le : {context.guild.created_at}")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="ping",
        description="Vérifiez si le bot est en ligne.",
    )
    async def ping(self, context: Context) -> None:
        """
        Vérifiez si le bot est en ligne.

        :param context: Le contexte de la commande hybride.
        """
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"La latence du bot est de {round(self.bot.latency * 1000)} ms.",
            color=0xBEBEFE,
        )
        await context.send(embed=embed)


    @commands.hybrid_command(
        name="invitation",
        description="Obtenez le lien d'invitation du bot pour pouvoir l'inviter.",
    )
    async def invitation(self, context: Context) -> None:
        """
        Obtenez le lien d'invitation du bot pour pouvoir l'inviter.

        :param context: Le contexte de la commande hybride.
        """
        embed = discord.Embed(
            description=f"Invitez-moi en cliquant [ici]({self.bot.config['invite_link']}).",
            color=0xD75BF4,
        )
        try:
            await context.author.send(embed=embed)
            await context.send("Je vous ai envoyé un message privé !")
        except discord.Forbidden:
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="serveur",
        description="Obtenez le lien d'invitation du serveur Discord du bot pour obtenir de l'aide.",
    )
    async def serveur(self, context: Context) -> None:
        """
        Obtenez le lien d'invitation du serveur Discord du bot pour obtenir de l'aide.

        :param context: Le contexte de la commande hybride.
        """
        embed = discord.Embed(
            description=f"Rejoignez le serveur de support du bot en cliquant [ici](https://discord.gg/mTBrXyWxAF).",
            color=0xD75BF4,
        )
        try:
            await context.author.send(embed=embed)
            await context.send("Je vous ai envoyé un message privé !")
        except discord.Forbidden:
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="8ball",
        description="Posez n'importe quelle question au bot.",
    )
    @app_commands.describe(question="La question que vous voulez poser.")
    async def huit_ball(self, context: Context, *, question: str) -> None:
        """
        Posez n'importe quelle question au bot.

        :param context: Le contexte de la commande hybride.
        :param question: La question que l'utilisateur souhaite poser.
        """
        reponses = [
            "C'est certain.",
            "C'est décidément le cas.",
            "Vous pouvez vous y fier.",
            "Sans aucun doute.",
            "Oui - certainement.",
            "D'après ce que je vois, oui.",
            "Très probablement.",
            "Les perspectives sont bonnes.",
            "Oui.",
            "Les signes le montrent.",
            "La réponse est floue, essayez à nouveau.",
            "Demandez plus tard.",
            "Mieux vaut ne pas vous le dire maintenant.",
            "Je ne peux pas prédire maintenant.",
            "Concentrez-vous et demandez plus tard.",
            "Ne comptez pas là-dessus.",
            "Ma réponse est non.",
            "Mes sources disent non.",
            "Les perspectives ne sont pas si bonnes.",
            "Très douteux.",
        ]
        embed = discord.Embed(
            title="**Ma réponse :**",
            description=f"{random.choice(reponses)}",
            color=0xBEBEFE,
        )
        embed.set_footer(text=f"La question était : {question}")
        await context.send(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(General(bot))
