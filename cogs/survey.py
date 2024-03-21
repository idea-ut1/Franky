import discord
from discord.ext import commands
from discord.ext.commands import Context

class Survey(commands.Cog, name="survey"):
    def __init__(self, bot):
        self.bot = bot
        self.survey_data = {}
        self.users_reacted = set()

    async def update_survey_message_with_reactions(self, ctx: Context, question_index: int):
        guild_id = ctx.guild.id

        # Vérifier si des questions ont été ajoutées
        if guild_id not in self.survey_data:
            await ctx.send('Aucune question de sondage ajoutée. Utilisez /question d\'abord.')
            return

        questions = self.survey_data[guild_id]['questions']

        # Vérifier si des questions existent
        if not questions:
            await ctx.send('Aucune question de sondage ajoutée. Utilisez /question d\'abord.')
            return

        current_question = questions[question_index]
        question = current_question['question']
        responses = current_question['responses']

        
        # Construire le message de sondage avec des réactions aux réponses possibles
        survey_message = f"\n**\nQuestion {question_index + 1}:**\n\n{question}\n\n**Réponses :\n\n**\n"
        

        # Envoyer le message de sondage avec des réactions
        
        message = await ctx.send(survey_message)
        for response in responses.keys():
            await message.add_reaction(response)

        # Mettre à jour l'ID du message dans les données de la question
        current_question['message_id'] = message.id


    @commands.hybrid_command(name="clean")
    async def delete_survey(self, ctx):
        # Check if the command invoker has the necessary permissions
        if ctx.author.guild_permissions.administrator:
            self.survey_data = {}  # Clear survey data
            self.users_reacted = set()  # Clear reacted users set
            await ctx.message.delete()


    @commands.hybrid_command(name='question')
    async def add_question(self, ctx: Context, *, question):
        guild_id = ctx.guild.id
        possible_responses = ['👍', '👎']  # OK, Pas OK, Je suis excité, Je ne sais pas
        
        # Vérifier si des questions ont été ajoutées
        if guild_id not in self.survey_data:
            self.survey_data[guild_id] = {'questions': []}
            await ctx.message.delete()
        # Initialiser les données de la nouvelle question
        question_data = {'question': question, 'responses': {}}
        for emoji in possible_responses:
            question_data['responses'][emoji] = 0

        # Ajouter la nouvelle question aux données de sondage
        self.survey_data[guild_id]['questions'].append(question_data)
        await ctx.message.delete()
        # Commenter la ligne suivante pour éviter d'afficher la question immédiatement
        # await self.update_survey_message_with_reactions(ctx, len(self.survey_data[guild_id]['questions']) - 1)

    @commands.hybrid_command(name='add_response')
    async def add_response(self, ctx: Context, response):
        guild_id = ctx.guild.id

        # Vérifier si des questions ont été ajoutées
        if guild_id not in self.survey_data:
            await ctx.send('Aucune question de sondage ajoutée. Utilisez /question d\'abord.')
            return

        # Récupérer la dernière question ajoutée
        current_question = self.survey_data[guild_id]['questions'][-1]

        # Vérifier si la réponse est valide
        if response not in current_question['responses']:
            await ctx.send('Réponse invalide. Utilisez /add_question pour voir les réponses disponibles.')
            return

        # Ajouter la réponse à la question
        current_question['responses'][response] += 1

        # Mettre à jour le message de sondage avec les réactions
        await self.update_survey_message_with_reactions(ctx, len(self.survey_data[guild_id]['questions']) - 1)


    ## Weather
        
    @commands.hybrid_command(
        name="weather",
        description="Obtenez la météo avec des réactions emoji prédéfinies.",
    )
    async def weather(self, context: Context, groupe: str = "everyone") -> None:
        """
        Obtenez la météo avec des réactions emoji prédéfinies.
        En mentionnant le groupe d'utilsateur que vous voulez notifier, par défaut c'est @everyone

        :param context: Le contexte de la commande hybride.
        """
        # Envoyer la demande de météo
        message = await context.send(f'Quelle est votre météo du jour ? {groupe}! \n\n ☀️ : Je suis de très bonne humeur\n ⛅ : Je suis de bonne humeur\n ☁️ : Je suis neutre\n 🌧️ : Je suis de mauvaise humeur\n ⚡ : Je suis de très mauvaise humeur\n\n')

        # Ajouter des réactions emoji au message
        emojis = ['☀️', '⛅', '☁️', '🌧️', '⚡']

        for emoji in emojis:
            await message.add_reaction(emoji)

        # Supprimer le message de l'utilisateur qui a déclenché la commande
        await context.message.delete()
    @commands.hybrid_command(name='survey')
    async def show_survey(self, ctx: Context):
        guild_id = ctx.guild.id

        # Vérifier si des questions ont été ajoutées
        if guild_id not in self.survey_data:
            await ctx.send('Aucune question de sondage ajoutée. Utilisez /question d\'abord.')
            await ctx.message.delete()
            return

        questions = self.survey_data[guild_id]['questions']

        # Vérifier si des questions existent
        if not questions:
            await ctx.send('Aucune question de sondage ajoutée. Utilisez /question d\'abord.')
            await ctx.message.delete()
            return
        await ctx.message.delete()
        # Construire le message de sondage avec toutes les questions et réponses
        await ctx.send("\nVeuillez répondre à ce questionnaire s'il vous plait\n")
        for index, question_data in enumerate(questions):
            await self.update_survey_message_with_reactions(ctx, index)
            

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
       if user.id not in self.users_reacted:
            await self.handle_reaction(reaction)
            self.users_reacted.add(user.id)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        # Gérer la réaction (retrait)
        await self.handle_reaction(reaction)

    async def handle_reaction(self, reaction):
        guild_id = reaction.message.guild.id

        # Vérifier si des questions ont été ajoutées
        if guild_id in self.survey_data:
            response = str(reaction.emoji)

            # Vérifier si la réponse est dans les réponses possibles
            if response in self.survey_data[guild_id]['responses']:
                self.survey_data[guild_id]['responses'][response] += 1

                # Trouver l'index de la question en fonction de l'ID du message de la réaction
                message_id = reaction.message.id
                for index, question_data in enumerate(self.survey_data[guild_id]['questions']):
                    if message_id == question_data.get('message_id'):
                        await self.update_survey_message_with_reactions(reaction.message.channel, index)

                # Actualiser le message du sondage pour afficher les nouveaux compteurs de réponse
                await self.update_survey_message_with_reactions(reaction.message.channel, index)
    @commands.hybrid_command(name="help")
    async def help(self,ctx):
        """Show all available commands"""
        help_message = "Available commands:\n"
        for command in self.commands:
            help_message += f"{command.name}: {command.help}\n"
        await ctx.send(help_message)

async def setup(bot):
    await bot.add_cog(Survey(bot))
