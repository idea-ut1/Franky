from ..extensions.message import Message

class Server:
    async def find_message_by_message_id(interaction, message_id):
        """
        Trouve un message avec son id

        Args:
            interaction : interaction
            message_id : id du message
        Returns:
            Message : message
        """
        for channel in interaction.guild.text_channels:
            try:
                message = await channel.fetch_message(message_id)
                return Message(content=message)
            except Exception as e:
                continue
        else:
            return None