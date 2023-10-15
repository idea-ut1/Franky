import random

import discord
from discord.ext import commands
from discord.ext.commands import Context


class Choice(discord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.value = None

    @discord.ui.button(label="Face", style=discord.ButtonStyle.blurple)
    async def confirm(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ) -> None:
        self.value = "face"
        self.stop()

    @discord.ui.button(label="Pile", style=discord.ButtonStyle.blurple)
    async def cancel(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ) -> None:
        self.value = "pile"
        self.stop()


class RockPaperScissors(discord.ui.Select):
    def __init__(self) -> None:
        options = [
            discord.SelectOption(
                label="Ciseaux", description="Vous choisissez les ciseaux.", emoji="✂️"
            ),
            discord.SelectOption(
                label="Pierre", description="Vous choisissez la pierre.", emoji="🪨"
            ),
            discord.SelectOption(
                label="Papier", description="Vous choisissez le papier.", emoji="🧻"
            ),
        ]
        super().__init__(
            placeholder="Choisissez...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        choices = {
            "pierre": 0,
            "papier": 1,
            "ciseaux": 2,
        }
        user_choice = self.values[0].lower()
        user_choice_index = choices[user_choice]

        bot_choice = random.choice(list(choices.keys()))
        bot_choice_index = choices[bot_choice]

        result_embed = discord.Embed(color=0xBEBEFE)
        result_embed.set_author(
            name=interaction.user.name, icon_url=interaction.user.display_avatar.url
        )

        winner = (3 + user_choice_index - bot_choice_index) % 3
        if winner == 0:
            result_embed.description = f"**C'est un match nul !**\nVous avez choisi {user_choice} et j'ai choisi {bot_choice}."
            result_embed.colour = 0xF59E42
        elif winner == 1:
            result_embed.description = f"**Vous avez gagné !**\nVous avez choisi {user_choice} et j'ai choisi {bot_choice}."
            result_embed.colour = 0x57F287
        else:
            result_embed.description = f"**Vous avez perdu !**\nVous avez choisi {user_choice} et j'ai choisi {bot_choice}."
            result_embed.colour = 0xE02B2B

        await interaction.response.edit_message(
            embed=result_embed, content=None, view=None
        )


class RockPaperScissorsView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.add_item(RockPaperScissors())


class Fun(commands.Cog, name="fun"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="pileface", description="Faites un pile ou face, mais donnez votre pari avant."
    )
    async def coinflip(self, context: Context) -> None:
        """
        Faites un pile ou face, mais donnez votre pari avant.

        :param context: Le contexte de la commande hybride.
        """
        buttons = Choice()
        embed = discord.Embed(description="Quel est votre pari ?", color=0xBEBEFE)
        message = await context.send(embed=embed, view=buttons)
        await buttons.wait()  # Nous attendons que l'utilisateur clique sur un bouton.
        result = random.choice(["face", "pile"])
        if buttons.value == result:
            embed = discord.Embed(
                description=f"Correct ! Vous avez deviné `{buttons.value}` et j'ai lancé la pièce à `{result}`.",
                color=0xBEBEFE,
            )
        else:
            embed = discord.Embed(
                description=f"Oops ! Vous avez deviné `{buttons.value}` et j'ai lancé la pièce à `{result}`, mieux la chance la prochaine fois !",
                color=0xE02B2B,
            )
        await message.edit(embed=embed, view=None, content=None)

    @commands.hybrid_command(
        name="pfc", description="Jouez au jeu pierre-papier-ciseaux contre le bot."
    )
    async def rock_paper_scissors(self, context: Context) -> None:
        """
        Jouez au jeu pierre-papier-ciseaux contre le bot.

        :param context: Le contexte de la commande hybride.
        """
        view = RockPaperScissorsView()
        await context.send("Faites votre choix", view=view)


async def setup(bot) -> None:
    await bot.add_cog(Fun(bot))
