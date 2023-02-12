import json
from typing import Iterable, Tuple, Dict, Union, List
from copy import deepcopy


Annee = int
Name = str
Offert = Dict[str, Union[Name, Annee]]
Offerts = List[Offert]
BlackList = List[Name]
PersonneHistorique = Dict[str, Union[Name, Offerts, BlackList]]
Historique = List[PersonneHistorique]


def ask_year() -> Annee:
    """
    Console asking to type the year to compute present repartition.

    Return
    ------
    : Annee
        The year to compute persent repartition
    """
    while True:
        année = input("Pour quelle année voulez vous générer les attributions de cadeaux à faire ? ")
        try:
            return int(année)
        except:
            print(f"Ecrivez une année, vous aviez écris \"{année}\"")
            continue


def get_historique_for_year(annee: Annee) -> Historique:
    """
    Load the history from json file.

    Parameters
    ----------
    annee: Annee
        The year from wich we need the previous one history

    reutrn
    ------
    : Historique
        The raw history object
    """
    file_path = f"historique/historique_{annee - 1}.json"
    print(f"Chargement de : {file_path}")
    with open(file_path, "r", encoding='utf-8') as file:
        historique: Historique = json.load(file)
    return historique


def update_historique(historique: Historique, exchanges: Iterable[Tuple[Name, Name]],
                      annee: Annee) -> Historique:
    """
    Parameters
    ----------
    historique: Historique
        A previous history object to append from
    exchanges: Iterable[Tuple[Name, Name]]
        The list of new exchanges this year, as a tuple of giver and reciver in that order
    annee: Annee
        The current year to register exchanges at

    Return
    ------
    : Historique
        The new history and previous information and the new one
    """
    new_historique: Historique = deepcopy(historique)

    for donneur, receveur in exchanges:
        gift_obj: Offert = {
            "nom": receveur,
            "année": annee,
        }

        for per_his in new_historique:
            if per_his["nom"] == donneur:
                per_his["offerts"].append(gift_obj)
                break
        else:
            historique.append({
                "nom": donneur,
                "offerts": [gift_obj],
            })

    return new_historique


def set_historique_for_year(historique: Historique, annee: Annee):
    """
    Write the history in a json file

    Parameters
    ----------
    historique: Historique
        The history object to save
    annee: Annee
        The year until this history extend (for the file's name)
    """
    file_path = f"historique/historique_{annee}.json"
    print(f"Ecriture de : {file_path}")
    with open(file_path, "w", encoding='utf-8') as file:
        historique = json.dump(historique, file, indent=4, ensure_ascii=False)
