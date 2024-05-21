import discord
from discord import ui
from ..config import config
from ..utils.event import Event
from ..utils.embed import Embed

class Question(ui.Modal):
    heading = ui.TextInput(
        label="Titre",
        style=discord.TextStyle.short,
        required=True
    )



    def __init__(self, reactions):
        super().__init__(title="Entrée")
        # Extrait les reactions de l'utilisateur ou met emoji par defaut
        self.reactions = config.extract_emojis(reactions) if reactions else config.reactions
        if reactions is not None:
            self.add_description()
        self.set_reaction()

    @property
    def default_description(self):
        """
        Retourne un template de description

        returns:
            str : description
        """
        return '\n'.join([f"{reaction} : " for reaction in self.reactions])

    def add_description(self):
        """
        Ajoute une description à la modal
        """
        self.description_field = ui.TextInput(
            label="Description",
            style=discord.TextStyle.long,
            required=False,
            default= self.default_description
        )

        self.add_item(self.description_field)
        
    def set_reaction(self):
        """
        Ajout Zone de saisie des reactions possible à la modal
        """
        self.reactions_field = ui.TextInput(
            label="Réactions",
            style=discord.TextStyle.short,
            required=False,
            default=' '.join(self.reactions)
        )
        self.add_item(self.reactions_field)



    async def on_submit(self, interaction: discord.Interaction):
        """
        Appelée lorsque l'utilisateur valide son entrée dans la modale

        Args:
            interaction : interaction
        """
        
        response_embed = Embed.get(
            title = self.heading.value,
            description = self.description_field.value if hasattr(self, 'description_field') else None
        )

        await Event.send_question_with_reactions(
            interaction = interaction,
            embed=response_embed,
            reactions=config.extract_emojis(self.reactions_field.value)
        )