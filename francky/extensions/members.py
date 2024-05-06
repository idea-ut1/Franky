from .member import Member 
import discord

class Members:
    """
    Une classe pour gérer une collection d'instances de Member.

    Attributs :
        users : Une liste d'instances de Member.
    """
    def __init__(self, users : list):
        self.users = [Member(user=user) for user in users]

    def __iter__(self):
        """
        Rend la classe itérable, permettant de parcourir ses membres.
        
        Returns :
            Un itérateur sur les instances de Member.
        """
        return iter(self.users)

    def filter_by(self, **kwargs):
        """
        Filtre les membres en fonction de critères fournis sous forme de mots-clés.

        Args :
            **kwargs: Des critères de filtrage sous forme de mots-clés.

        Returns :
            Une liste d'instances de Member qui correspondent aux critères de filtrage.
        """
        return [member for member in self.users if member.filters_pass(**kwargs)]

    def find_with_user_id(self, id : int):
        """
        Trouve un membre en utilisant son identifiant.

        Args :
            id : L'identifiant de l'utilisateur.

        Returns :
            L'instance de Member correspondante, ou None si aucun membre n'est trouvé.
        """
        member = self.filter_by(id=id)
        if not member:
            return None
        return member[0]
    
    def add(self, user : discord.Member):
        """
        Ajoute un nouveau membre à la collection.

        Args :
            user : Un membre discord.
        """
        self.users.append(Member(user=user))

    def remove_with_user_id(self, id : int):
        """
        Supprime un membre en utilisant son identifiant.

        Args :
            id : L'identifiant de l'utilisateur.

        Returns :
            True si le membre a été supprimé avec succès, False sinon.
        """
        member = self.find_with_user_id(id)
        if member:
            self.users.remove(member)
            return True
        return False
    
    def remove_with_user_id(self, id : int):
        """
        Supprime un membre en utilisant son identifiant.

        Args :
            id : L'identifiant de l'utilisateur.

        Returns :
            True si le membre a été supprimé avec succès, False sinon.
        """
        member = self.filter_by(id=id)
        if not member:
            return False
        member = member[0]
        self.users.remove(member)
    
    @property
    def projects(self):
        """
        Retourne la liste des projets auxquels les membres participent.

        Returns :
            Une liste de projets uniques.
        """
        return list(set(member.project for member in self.users if member.project))