import discord

class Embed:

    def get(title=None, description=None):
        """
        Modèle de message génerique

        Args:
            title : titre
            description : description
        """
        return discord.Embed(
            title=title,
            description=description,  
            color=discord.Color.blue()
        )

    def get_weather(title, reactions_count):
        """
        Modèle de message pour le resultat de la méteo

        Args:
            title : titre
            reactions_count : nombre de votes par réaction
        """
        embed = Embed.get(
            title=title
        )
        for reaction, count in reactions_count.items():
            embed.add_field(name=reaction, value=count, inline=True)
        return embed 