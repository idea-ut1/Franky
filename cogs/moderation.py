import os
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class Modération(commands.Cog, name="modération"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="expulser",
        description="Expulsez un utilisateur du serveur.",
    )
    @commands.has_permissions(expulser_des_membres=True)
    @commands.bot_has_permissions(expulser_des_membres=True)
    @app_commands.describe(
        utilisateur="L'utilisateur à expulser.",
        raison="La raison pour laquelle l'utilisateur doit être expulsé.",
    )
    async def expulser(
        self, context: Context, utilisateur: discord.User, *, raison: str = "Non spécifiée"
    ) -> None:
        """
        Expulsez un utilisateur du serveur.

        :param context: Le contexte de la commande hybride.
        :param utilisateur: L'utilisateur à expulser du serveur.
        :param raison: La raison de l'expulsion. Par défaut, "Non spécifiée".
        """
        membre = context.guild.get_member(utilisateur.id) or await context.guild.fetch_member(
            utilisateur.id
        )
        if membre.guild_permissions.administrator:
            embed = discord.Embed(
                description="L'utilisateur a des permissions d'administrateur.", color=0xE02B2B
            )
            await context.send(embed=embed)
        else:
            try:
                embed = discord.Embed(
                    description=f"**{membre}** a été expulsé par **{context.author}**!",
                    color=0xBEBEFE,
                )
                embed.add_field(name="Raison :", value=raison)
                await context.send(embed=embed)
                try:
                    await membre.send(
                        f"Vous avez été expulsé par **{context.author}** de **{context.guild.name}**!\nRaison : {raison}"
                    )
                except:
                    # Impossible d'envoyer un message dans les messages privés de l'utilisateur
                    pass
                await membre.kick(reason=raison)
            except:
                embed = discord.Embed(
                    description="Une erreur s'est produite lors de la tentative d'expulsion de l'utilisateur. Assurez-vous que mon rôle est au-dessus du rôle de l'utilisateur que vous souhaitez expulser.",
                    color=0xE02B2B,
                )
                await context.send(embed=embed)

    @commands.hybrid_command(
        name="surnom",
        description="Changer le surnom d'un utilisateur sur un serveur.",
    )
    @commands.has_permissions(gérer_les_surnoms=True)
    @commands.bot_has_permissions(gérer_les_surnoms=True)
    @app_commands.describe(
        utilisateur="L'utilisateur dont le surnom doit être changé.",
        surnom="Le nouveau surnom qui doit être défini.",
    )
    async def surnom(
        self, context: Context, utilisateur: discord.User, *, surnom: str = None
    ) -> None:
        """
        Change le surnom d'un utilisateur sur un serveur.

        :param context: Le contexte de la commande hybride.
        :param utilisateur: L'utilisateur dont le surnom doit être changé.
        :param surnom: Le nouveau surnom de l'utilisateur. Par défaut, None, ce qui réinitialisera le surnom.
        """
        membre = context.guild.get_member(utilisateur.id) or await context.guild.fetch_member(
            utilisateur.id
        )
        try:
            await membre.edit(nick=surnom)
            embed = discord.Embed(
                description=f"Le nouveau surnom de **{membre}** est **{surnom}**!",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
        except:
            embed = discord.Embed(
                description="Une erreur s'est produite lors de la tentative de changement du surnom de l'utilisateur. Assurez-vous que mon rôle est au-dessus du rôle de l'utilisateur que vous souhaitez modifier le surnom.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="bannir",
        description="Bannir un utilisateur du serveur.",
    )
    @commands.has_permissions(bannir_des_membres=True)
    @commands.bot_has_permissions(bannir_des_membres=True)
    @app_commands.describe(
        utilisateur="L'utilisateur à bannir.",
        raison="La raison pour laquelle l'utilisateur doit être banni.",
    )
    async def bannir(
        self, context: Context, utilisateur: discord.User, *, raison: str = "Non spécifiée"
    ) -> None:
        """
        Bannir un utilisateur du serveur.

        :param context: Le contexte de la commande hybride.
        :param utilisateur: L'utilisateur à bannir du serveur.
        :param raison: La raison du bannissement. Par défaut, "Non spécifiée".
        """
        membre = context.guild.get_member(utilisateur.id) or await context.guild.fetch_member(
            utilisateur.id
        )
        try:
            if membre.guild_permissions.administrator:
                embed = discord.Embed(
                    description="L'utilisateur a des permissions d'administrateur.", color=0xE02B2B
                )
                await context.send(embed=embed)
            else:
                embed = discord.Embed(
                    description=f"**{membre}** a été banni par **{context.author}**!",
                    color=0xBEBEFE,
                )
                embed.add_field(name="Raison :", value=raison)
                await context.send(embed=embed)
                try:
                    await membre.send(
                        f"Vous avez été banni par **{context.author}** de **{context.guild.name}**!\nRaison : {raison}"
                    )
                except:
                    # Impossible d'envoyer un message dans les messages privés de l'utilisateur
                    pass
                await membre.ban(reason=raison)
        except:
            embed = discord.Embed(
                title="Erreur !",
                description="Une erreur s'est produite lors de la tentative de bannissement de l'utilisateur. Assurez-vous que mon rôle est au-dessus du rôle de l'utilisateur que vous souhaitez bannir.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)

    @commands.hybrid_group(
        name="avertissement",
        description="Gérez les avertissements d'un utilisateur sur un serveur.",
    )
    @commands.has_permissions(gérer_les_messages=True)
    async def avertissement(self, context: Context) -> None:
        """
        Gérez les avertissements d'un utilisateur sur un serveur.

        :param context: Le contexte de la commande hybride.
        """
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="Veuillez spécifier une sous-commande.\n\n**Sous-commandes :**\n`ajouter` - Ajouter un avertissement à un utilisateur.\n`retirer` - Retirer un avertissement à un utilisateur.\n`liste` - Liste de tous les avertissements d'un utilisateur.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)

    @avertissement.command(
        name="ajouter",
        description="Ajoute un avertissement à un utilisateur sur le serveur.",
    )
    @commands.has_permissions(gérer_les_messages=True)
    @app_commands.describe(
        utilisateur="L'utilisateur à avertir.",
        raison="La raison pour laquelle l'utilisateur doit être averti.",
    )
    async def avertissement_ajouter(
        self, context: Context, utilisateur: discord.User, *, raison: str = "Non spécifiée"
    ) -> None:
        """
        Avertissez un utilisateur dans ses messages privés.

        :param context: Le contexte de la commande hybride.
        :param utilisateur: L'utilisateur à avertir.
        :param raison: La raison de l'avertissement. Par défaut, "Non spécifiée".
        """
        membre = context.guild.get_member(utilisateur.id) or await context.guild.fetch_member(
            utilisateur.id
        )
        total = await self.bot.database.add_warn(
            utilisateur.id, context.guild.id, context.author.id, raison
        )
        embed = discord.Embed(
            description=f"**{membre}** a été averti par **{context.author}**!\nTotal des avertissements pour cet utilisateur : {total}",
            color=0xBEBEFE,
        )
        embed.add_field(name="Raison :", value=raison)
        await context.send(embed=embed)
        try:
            await membre.send(
                f"Vous avez été averti par **{context.author}** dans **{context.guild.name}**!\nRaison : {raison}"
            )
        except:
            # Impossible d'envoyer un message dans les messages privés de l'utilisateur
            await context.send(
                f"{membre.mention}, vous avez été averti par **{context.author}**!\nRaison : {raison}"
            )

    @avertissement.command(
        name="retirer",
        description="Retire un avertissement à un utilisateur sur le serveur.",
    )
    @commands.has_permissions(gérer_les_messages=True)
    @app_commands.describe(
        utilisateur="L'utilisateur dont l'avertissement doit être retiré.",
        avertissement_id="L'ID de l'avertissement à retirer.",
    )
    async def avertissement_retirer(
        self, context: Context, utilisateur: discord.User, avertissement_id: int
    ) -> None:
        """
        Avertissez un utilisateur dans ses messages privés.

        :param context: Le contexte de la commande hybride.
        :param utilisateur: L'utilisateur dont l'avertissement doit être retiré.
        :param avertissement_id: L'ID de l'avertissement à retirer.
        """
        membre = context.guild.get_member(utilisateur.id) or await context.guild.fetch_member(
            utilisateur.id
        )
        total = await self.bot.database.remove_warn(avertissement_id, utilisateur.id, context.guild.id)
        embed = discord.Embed(
            description=f"J'ai retiré l'avertissement **#{avertissement_id}** de **{membre}**!\nTotal des avertissements pour cet utilisateur : {total}",
            color=0xBEBEFE,
        )
        await context.send(embed=embed)

    @avertissement.command(
        name="liste",
        description="Affiche les avertissements d'un utilisateur sur le serveur.",
    )
    @commands.has_guild_permissions(gérer_les_messages=True)
    @app_commands.describe(user="L'utilisateur dont vous souhaitez obtenir les avertissements.")
    async def avertissement_liste(self, context: Context, utilisateur: discord.User) -> None:
        """
        Affiche les avertissements d'un utilisateur sur le serveur.

        :param context: Le contexte de la commande hybride.
        :param utilisateur: L'utilisateur dont vous souhaitez obtenir les avertissements.
        """
        liste_des_avertissements = await self.bot.database.get_warnings(utilisateur.id, context.guild.id)
        embed = discord.Embed(title=f"Avertissements de {utilisateur}", color=0xBEBEFE)
        description = ""
        if len(liste_des_avertissements) == 0:
            description = "Cet utilisateur n'a aucun avertissement."
        else:
            for avertissement in liste_des_avertissements:
                description += f"• Averti par <@{avertissement[2]}> : **{avertissement[3]}** (<t:{avertissement[4]}>) - ID de l'avertissement #{avertissement[5]}\n"
        embed.description = description
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="purge",
        description="Supprime un nombre de messages.",
    )
    @commands.has_guild_permissions(gérer_les_messages=True)
    @commands.bot_has_permissions(gérer_les_messages=True)
    @app_commands.describe(quantité="Le nombre de messages à supprimer.")
    async def purge(self, context: Context, quantité: int) -> None:
        """
        Supprime un nombre de messages.

        :param context: Le contexte de la commande hybride.
        :param quantité: Le nombre de messages à supprimer.
        """
        await context.send(
            "Suppression des messages..."
        )  # Une façon un peu astucieuse de s'assurer que le bot réponde à l'interaction et ne reçoive pas une réponse "Interaction inconnue"
        messages_purgés = await context.channel.purge(limit=quantité + 1)
        embed = discord.Embed(
            description=f"**{context.author}** a supprimé **{len(messages_purgés)-1}** messages!",
            color=0xBEBEFE,
        )
        await context.channel.send(embed=embed)

    @commands.hybrid_command(
        name="ban_hack",
        description="Bannir un utilisateur sans que l'utilisateur ait besoin d'être sur le serveur.",
    )
    @commands.has_permissions(bannir_des_membres=True)
    @commands.bot_has_permissions(bannir_des_membres=True)
    @app_commands.describe(
        id_utilisateur="L'ID de l'utilisateur à bannir.",
        raison="La raison pour laquelle l'utilisateur doit être banni.",
    )
    async def ban_hack(
        self, context: Context, id_utilisateur: str, *, raison: str = "Non spécifiée"
    ) -> None:
        """
        Bannir un utilisateur sans que l'utilisateur ait besoin d'être sur le serveur.

        :param context: Le contexte de la commande hybride.
        :param id_utilisateur: L'ID de l'utilisateur à bannir.
        :param raison: La raison du bannissement. Par défaut, "Non spécifiée".
        """
        try:
            await self.bot.http.ban(id_utilisateur, context.guild.id, reason=raison)
            utilisateur = self.bot.get_user(int(id_utilisateur)) or await self.bot.fetch_user(
                int(id_utilisateur)
            )
            embed = discord.Embed(
                description=f"**{utilisateur}** (ID : {id_utilisateur}) a été banni par **{context.author}**!",
                color=0xBEBEFE,
            )
            embed.add_field(name="Raison :", value=raison)
            await context.send(embed=embed)
        except Exception:
            embed = discord.Embed(
                description="Une erreur s'est produite lors de la tentative de bannissement de l'utilisateur. Assurez-vous que l'ID est un ID existant appartenant à un utilisateur.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="archiver",
        description="Archive dans un fichier texte les derniers messages avec une limite de messages choisie.",
    )
    @commands.has_permissions(gérer_les_messages=True)
    @app_commands.describe(
        limite="La limite de messages à archiver.",
    )
    async def archiver(self, context: Context, limite: int = 10) -> None:
        """
        Archive dans un fichier texte les derniers messages avec une limite de messages choisie. Cette commande nécessite l'intention MESSAGE_CONTENT pour fonctionner correctement.

        :param limite: La limite de messages à archiver. Par défaut, 10.
        """
        fichier_journal = f"{context.channel.id}.log"
        with open(fichier_journal, "w", encoding="UTF-8") as f:
            f.write(
                f'Messages archivés depuis : #{context.channel} ({context.channel.id}) dans la guilde "{context.guild}" ({context.guild.id}) à {datetime.now().strftime("%d.%m.%Y %H:%M:%S")}\n'
            )
            async for message in context.channel.history(
                limit=limite, before=context.message
            ):
                pièces_jointes = []
                for pièce_jointe in message.attachments:
                    pièces_jointes.append(pièce_jointe.url)
                texte_des_pièces_jointes = (
                    f"[Fichier{'s' if len(pièces_jointes) >= 2 else ''} joint{'s' if len(pièces_jointes) >= 2 else ''} : {', '.join(pièces_jointes)}]"
                    if len(pièces_jointes) >= 1
                    else ""
                )
                f.write(
                    f"{message.created_at.strftime('%d.%m.%Y %H:%M:%S')} {message.author} {message.id} : {message.clean_content} {texte_des_pièces_jointes}\n"
                )
        f = discord.File(fichier_journal)
        await context.send(file=f)
        os.remove(fichier_journal)


async def configuration(bot) -> None:
    await bot.add_cog(Modération(bot))