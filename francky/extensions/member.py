import discord 
from ..config import config

class Member:
    """
    Représente un membre du serveur Discord, encapsulant certaines fonctionnalités et propriétés spécifiques.

    Attributes:
        user : L'objet membre Discord associé.
    """
    def __init__(self, user : discord.Member):
        self.user = user

    async def send(self, **kwargs):
        """
        Envoie un message privé au membre avec les options fournies.

        Args:
            **kwargs: Arguments clés variables passés à la méthode `send` de l'objet membre.
        """
        try:
            await self.user.send(**kwargs)
        except Exception as e:
            print(f"Une erreur : {e}")

    @property
    def roles(self):
        """
        Obtient une liste des rôles du membre, excluant le rôle @everyone.

        Returns:
            List[discord.Role]: Une liste des objets discord.Role associés au membre.
        """
        return [role for role in self.user.roles if role.name != "@everyone"]

    @property
    def role(self):
        """
        Extrait le projet et la fonction du membre basés sur ses rôles dans le serveur.

        Cette propriété examine les rôles du membre pour déterminer son projet et sa fonction
        basés sur les noms de rôles pré-définis dans les configurations.

        Returns:
            dict: Un dictionnaire avec les clés 'project' et 'function', représentant respectivement
            le projet et la fonction du membre. Les valeurs sont None si non applicables.
        """
        res = {}
        for role in self.roles:
            if role.name in config.projects:
                res['project'] = role.name
            elif role.name in config.functions:
                res['function'] = role.name
        return res

    @property
    def id(self):
        """
        L'ID Discord unique du membre.

        Returns:
            int: L'ID Discord du membre.
        """
        return self.user.id

    @property
    def project(self):
        """
        Le projet associé au membre.

        Returns:
            str or None: Le nom du projet si déterminé, sinon None.
        """
        return self.role.get('project', None)

    @property
    def function(self):
        """
        La fonction du membre au sein de son projet.

        Returns:
            str or None: La fonction du membre si déterminée, sinon None.
        """
        return self.role.get('function', None)

    def filters_pass(self, **kwargs):
        """
        Détermine si le membre correspond à un ensemble de critères spécifiés.

        Args:
            **kwargs: Un ensemble de paires clé-valeur définissant les attributs et leurs valeurs attendues.

        Returns:
            bool: True si le membre satisfait tous les critères, False autrement.
        """
        for key, expected_value in kwargs.items():
            value = getattr(self, key, None)
            if isinstance(expected_value, list):
                if value not in expected_value:
                    return False
            elif expected_value != value:
                return False
        return True