## Commandes discord par roles
- ### Chapo 
    - `/session start` : 
      - Demmarre une séance de cours
      - Ne peut pas être lancé consécutivement (doit lancer `/session stop` avant de pouvoir lancer un nouveau `/session start`)

    - `/session stop` : 
      - Termine une séance de cours
      - Les bilans agrégés des utilisateurs (`/summary`) sont envoyés dans chacun des canaux correspondant aux projets actifs
      - Ne fonctionne pas si `/seance start` n'a pas été lancée en amont

    - `/weather` : 
      - Lance une méteo du bonheur (peut uniquement être utilisée dans `#general`)
      - Les resultats sont envoyés (par projet) dans chacun des cannaux des projets actifs

- ### @everyone
    - `/summary` : 
      - Déclanche la saisie du bilan pour la séance 
      - Tant qu'un chapo n'a pas lancé `/session stop` le bilan peut être modifié (Relancer la commande)

    - `/question` : 
      - Démarre un questionnaire 
      - Les questions envoyés ne peuvent pas être supprimés par l'utilisateur non admin (Attention à ce que vous écrivez !)

---

## Configurations 

### Ajouter/supprimer des fonctions utilisateurs 

Dans `francky/config.py`

```
    @property
    def functions(self):
        """
        fonctions possibles des membres

        returns:
            list : fonctions
        """
        return [
            'Chapo',
            'Manager',
            'Développeur'
        ]
```

Les fonctions de cette liste correspondent aux roles discord qui ont été attribués. Ce sont  uniquement les fonctions clés (donc non annexe ex : tech-lead n'y figure pas)

### Ajouter/supprimer des projets actifs


Dans `francky/config.py`

```
    @property
    def map_projects_channels(self):
        """
        liens entre les projets (roles) et cannaux
        
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
```

Fais le lien entre les projets actifs (qui sont des roles discords) et les cannaux associés. Exemple : les bilans des séances sont envoyés uniquement dans ces cannaux (valeurs) pour les utilisateurs ayant un role d'un projet (clef)

---


### Annexe

 - cogs (commandes discord)
   - poll.py (commandes liés aux sondages)
   - session.py (commandes liés aux cours)
 
 - extensions (extensions des fonctionnalités discord.py)
   - member.py (+ fonctionnalités d'un membre du serveur)
   - members.py ( + fonctionnalités des membres du serveurs)
   - message.py (+ fonctionnalités des messages)

 - modals (fenetres de saisies)
   - question.py (fenetre pour la saisie des sondages)
   - summary.py (fenetre pour la saisie des bilans)

 - utils (package utilitaire)
   - embed.py (modeles des messages envoyés)
   - event.py (actions des utilisateurs)
   - server.py (fonctionnalité etendu pour server)
   - session.py (class de cours (ajout/recherche bilan etc ...))

- bot.py (programme principale)
- config.py (fichier de configuration)