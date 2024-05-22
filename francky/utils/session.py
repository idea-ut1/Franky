from datetime import datetime

class Session:
    def __init__(self):
        self.start = datetime.now()
        self.summaries = []


    def get_summary_message_with_author(self, author):
        for summary in self.summaries[:]:
            if summary.author.id == author.id:
                return summary.message
       

    def add_summary(self, author, message):
        """
        Ajoute un bilan d'un membre à la session

        Args:
            author : (objet Member) auteur du bilan
            message : (objet Message) bilan
        """
        for summary in self.summaries[:]:
            if summary.author.id == author.id:
                self.summaries.remove(summary)
    
        self.summaries.append(Summary(author=author, message=message))


class Summary:
    def __init__(self, author, message) -> None:
        self.author = author
        self.message = message