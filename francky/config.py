import emoji

class Config():

    def extract_emojis(self, string):
        """
        Extrait des emojis d'une chaine de charactere

        args:
            string : chaine de caractere contenant les emojis a extraire
        returns:
            list : Liste des emojis extrait
        """
        return emoji.distinct_emoji_list(string)

    @property
    def reactions(self):
        """
        Reactions par defaut
        returns:
            list : Reactions
        """
        return ['✅', '❌']

    @property
    def map_projects_channels(self):
        """
        mapping des projets (roles) et les cannaux
        returns:
            dict : projet : cannal
        """
        return {
            'Site idea' : '🛠│site-idea',
            'AEG' : '💾│aeg',
            'Canceropole' : '⚙│deep-cancer',
            'Catching Spirits' : '🔥│catching-spirit',
            'Occitanie' : '🥐│projet-occitanie'
        }

    @property
    def projects(self):
        """
        Liste des projets du serveur
        returns:
            list : projets
        """
        return list(self.map_projects_channels.keys())

    @property
    def channels(self):
        """
        Liste des cannaux des projets du serveur
        returns:
            list : cannaux
        """
        return list(self.map_projects_channels.values())

    @property
    def functions(self):
        """
        fonctions des membres possibles
        returns:
            list : fonctions
        """
        return [
            'Chapo',
            'Manager',
            'Tech Lead',
            'Développeur'
        ]

config = Config()