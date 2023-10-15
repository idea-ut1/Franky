import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

class Owner(commands.Cog, name="propriétaire"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(
        name="sync",
        description="Synchronise les commandes slash.",
    )
    @app_commands.describe(scope="La portée de la synchronisation. Peut être `globale` ou `serveur`")
    @commands.is_owner()
    async def sync(self, context: Context, scope: str) -> None:
        """
        Synchronise les commandes slash.

        :param context: Le contexte de la commande.
        :param scope: La portée de la synchronisation. Peut être `globale` ou `serveur`.
        """

        if scope == "globale":
            await context.bot.tree.sync()
            embed = discord.Embed(
                description="Les commandes slash ont été synchronisées globalement.",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        elif scope == "serveur":
            context.bot.tree.copy_global_to(guild=context.guild)
            await context.bot.tree.sync(guild=context.guild)
            embed = discord.Embed(
                description="Les commandes slash ont été synchronisées dans ce serveur.",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description="La portée doit être `globale` ou `serveur`.", color=0xE02B2B
        )
        await context.send(embed=embed)

    @commands.command(
        name="unsync",
        description="Désynchronise les commandes slash.",
    )
    @app_commands.describe(
        scope="La portée de la synchronisation. Peut être `globale`, `serveur_actuel` ou `serveur`"
    )
    @commands.is_owner()
    async def unsync(self, context: Context, scope: str) -> None:
        """
        Désynchronise les commandes slash.

        :param context: Le contexte de la commande.
        :param scope: La portée de la synchronisation. Peut être `globale`, `serveur_actuel` ou `serveur`.
        """

        if scope == "globale":
            context.bot.tree.clear_commands(guild=None)
            await context.bot.tree.sync()
            embed = discord.Embed(
                description="Les commandes slash ont été désynchronisées globalement.",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        elif scope == "serveur":
            context.bot.tree.clear_commands(guild=context.guild)
            await context.bot.tree.sync(guild=context.guild)
            embed = discord.Embed(
                description="Les commandes slash ont été désynchronisées dans ce serveur.",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description="La portée doit être `globale` ou `serveur`.", color=0xE02B2B
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="load",
        description="Charge un module",
    )
    @app_commands.describe(cog="Le nom du module à charger")
    @commands.is_owner()
    async def load(self, context: Context, cog: str) -> None:
        """
        Le bot chargera le module donné.

        :param context: Le contexte de la commande hybride.
        :param cog: Le nom du module à charger.
        """
        try:
            await self.bot.load_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                description=f"Impossible de charger le module `{cog}`.", color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description=f"Le module `{cog}` a été chargé avec succès.", color=0xBEBEFE
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="unload",
        description="Décharge un module.",
    )
    @app_commands.describe(cog="Le nom du module à décharger")
    @commands.is_owner()
    async def unload(self, context: Context, cog: str) -> None:
        """
        Le bot déchargera le module donné.

        :param context: Le contexte de la commande hybride.
        :param cog: Le nom du module à décharger.
        """
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                description=f"Impossible de décharger le module `{cog}`.", color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description=f"Le module `{cog}` a été déchargé avec succès.", color=0xBEBEFE
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="reload",
        description="Recharge un module.",
    )
    @app_commands.describe(cog="Le nom du module à recharger")
    @commands.is_owner()
    async def reload(self, context: Context, cog: str) -> None:
        """
        Le bot rechargera le module donné.

        :param context: Le contexte de la commande hybride.
        :param cog: Le nom du module à recharger.
        """
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                description=f"Impossible de recharger le module `{cog}`.", color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description=f"Le module `{cog}` a été rechargé avec succès.", color=0xBEBEFE
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="shutdown",
        description="Fait redémarrer le bot.",
    )
    @commands.is_owner()
    async def shutdown(self, context: Context) -> None:
        """
        Éteint le bot.

        :param context: Le contexte de la commande hybride.
        """
        embed = discord.Embed(description="Arrêt en cours. Au revoir ! :wave:", color=0xBEBEFE)
        await context.send(embed=embed)
        await self.bot.close()

    @commands.hybrid_command(
        name="say",
        description="Le bot répétera ce que vous voulez.",
    )
    @app_commands.describe(message="Le message que le bot doit répéter")
    @commands.is_owner()
    async def say(self, context: Context, *, message: str) -> None:
        """
        Le bot répétera ce que vous voulez.

        :param context: Le contexte de la commande hybride.
        :param message: Le message que le bot doit répéter.
        """
        await context.send(message)

    @commands.hybrid_command(
        name="embed",
        description="Le bot répétera ce que vous voulez, mais dans des embeddings.",
    )
    @app_commands.describe(message="Le message que le bot doit répéter")
    @commands.is_owner()
    async def embed(self, context: Context, *, message: str) -> None:
        """
        Le bot répétera ce que vous voulez, mais en utilisant des embeddings.

        :param context: Le contexte de la commande hybride.
        :param message: Le message que le bot doit répéter.
        """
        embed = discord.Embed(description=message, color=0xBEBEFE)
        await context.send(embed=embed)

    @commands.hybrid_group(
        name="liste_noire",
        description="Obtenez la liste de tous les utilisateurs en liste noire.",
    )
    @commands.is_owner()
    async def blacklist(self, context: Context) -> None:
        """
        Vous permet d'ajouter ou de supprimer un utilisateur qui ne peut pas utiliser le bot.

        :param context: Le contexte de la commande hybride.
        """
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="Vous devez spécifier une sous-commande.\n\n**Sous-commandes:**\n`ajouter` - Ajouter un utilisateur à la liste noire.\n`supprimer` - Supprimer un utilisateur de la liste noire.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)

    @blacklist.command(
        base="liste_noire",
        name="afficher",
        description="Affiche la liste de tous les utilisateurs en liste noire.",
    )
    @commands.is_owner()
    async def blacklist_show(self, context: Context) -> None:
        """
        Affiche la liste de tous les utilisateurs en liste noire.

        :param context: Le contexte de la commande hybride.
        """
        blacklisted_users = await self.bot.database.get_blacklisted_users()
        if len(blacklisted_users) == 0:
            embed = discord.Embed(
                description="Il n'y a actuellement aucun utilisateur en liste noire.", color=0xE02B2B
            )
            await context.send(embed=embed)
            return

        embed = discord.Embed(title="Utilisateurs en liste noire", color=0xBEBEFE)
        users = []
        for bluser in blacklisted_users:
            user = self.bot.get_user(int(bluser[0])) or await self.bot.fetch_user(
                int(bluser[0])
            )
            users.append(f"• {user.mention} ({user}) - En liste noire <t:{bluser[1]}>")
        embed.description = "\n".join(users)
        await context.send(embed=embed)

    @blacklist.command(
        base="liste_noire",
        name="ajouter",
        description="Vous permet d'ajouter un utilisateur à la liste noire.",
    )
    @app_commands.describe(user="L'utilisateur à ajouter à la liste noire")
    @commands.is_owner()
    async def blacklist_add(self, context: Context, user: discord.User) -> None:
        """
        Vous permet d'ajouter un utilisateur qui ne peut pas utiliser le bot.

        :param context: Le contexte de la commande hybride.
        :param user: L'utilisateur à ajouter à la liste noire.
        """
        user_id = user.id
        if await self.bot.database.is_blacklisted(user_id):
            embed = discord.Embed(
                description=f"**{user.name}** est déjà dans la liste noire.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return
        total = await self.bot.database.add_user_to_blacklist(user_id)
        embed = discord.Embed(
            description=f"**{user.name}** a été ajouté avec succès à la liste noire",
            color=0xBEBEFE,
        )
        embed.set_footer(
            text=f"Il {'y a' if total == 1 else 'y a'} maintenant {total} {'utilisateur' if total == 1 else 'utilisateurs'} dans la liste noire"
        )
        await context.send(embed=embed)

    @blacklist.command(
        base="liste_noire",
        name="supprimer",
        description="Vous permet de supprimer un utilisateur de la liste noire.",
    )
    @app_commands.describe(user="L'utilisateur à supprimer de la liste noire.")
    @commands.is_owner()
    async def blacklist_remove(self, context: Context, user: discord.User) -> None:
        """
        Vous permet de supprimer un utilisateur de la liste noire.

        :param context: Le contexte de la commande hybride.
        :param user: L'utilisateur à supprimer de la liste noire.
        """
        user_id = user.id
        if not await self.bot.database.is_blacklisted(user_id):
            embed = discord.Embed(
                description=f"**{user.name}** n'est pas dans la liste noire.", color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        total = await self.bot.database.remove_user_from_blacklist(user_id)
        embed = discord.Embed(
            description=f"**{user.name}** a été supprimé avec succès de la liste noire",
            color=0xBEBEFE,
        )
        embed.set_footer(
            text=f"Il {'y a' if total == 1 else 'y a'} maintenant {total} {'utilisateur' if total == 1 else 'utilisateurs'} dans la liste noire"
        )
        await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Owner(bot))
