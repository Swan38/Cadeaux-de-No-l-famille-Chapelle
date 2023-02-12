from typing import List

from historique import Historique


def ask_participants(historique: Historique) -> List[str]:
    while True:
        print("Qui participe cette année ?")
        participants = []
        while True:
            participant = input("Saisissez un nom (\"quit\" pour arrêter) : ")

            if participant == "quit":
                break
            elif participant not in list(map(lambda personne: personne["nom"], historique)):
                print("Soit cette personne est une nouvelle personne dans l'historique, soit son nom n'a pas été tapé de la même manière.")
                while True:
                    print("Saisissez \"nouveau\" pour une nouvelle personne, \"liste\" pour afficher les noms ou le nom correcte directement :")
                    reponse = input()
                    if reponse == "nouveau":
                        break
                    elif reponse == "liste":
                        print(set(map(lambda personne: personne["nom"], historique)))
                    elif reponse in list(map(lambda personne: personne["nom"], historique)):
                        participant = reponse
                        break

            participants.append(participant)

        print(f"Les participants seront :", participants)

        while True:
            reponse = input("Validez vous les participants cette année (oui/non) ? ")
            if reponse in ["oui", "non"]:
                break
        if reponse == "oui":
            break

    return participants

def hard_coded_participants_2023() -> List[str]:
    return [
        "Valérie",
        "Aurore",
        "Sidonie",
        "Jean-Paul",
        "Cyprien",
        "Antonin",
        "Jérôme",
        "Agathe",
        "Julien",
        "Geneviève",
        "Léonie",
        "Sylvain",
        "Jean-Luc",
        "Bruno",
        "Perine",
    ]
