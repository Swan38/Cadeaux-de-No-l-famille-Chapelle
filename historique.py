import json
from typing import Iterable, Tuple
from copy import deepcopy

from personne import Personne


def ask_year() -> int:
    while True:
        année = input("Pour quelle année voulez vous générer les attributions de cadeaux à faire ? ")
        try:
            return int(année)
        except:
            print(f"Ecrivez une année, vous aviez écris \"{année}\"")
            continue


def get_historique_for_year(année: int):
    file_path = f"historique/historique_{année - 1}.json"
    print(f"Chargement de : {file_path}")
    with open(file_path, "r", encoding='utf-8') as file:
        historique = json.load(file)
    return historique


def update_historique(historique, exchanges: Iterable[Tuple[Personne, Personne]], annee: int) -> object:
    new_historique = deepcopy(historique)

    for donneur, receveur in exchanges:
        gift_obj = {
            "nom": receveur.name,
            "année": annee,
        }

        for per_his in new_historique:
            if per_his["nom"] == donneur.name:
                per_his["offerts"].append(gift_obj)
                break
        else:
            historique.append({
                "nom": donneur.name,
                "black_list": donneur.black_list,
                "offerts": [gift_obj]
            })

    return new_historique


def set_historique_for_year(historique, annee: int):
    file_path = f"historique/historique_{annee}.json"
    print(f"Ecriture de : {file_path}")
    with open(file_path, "w", encoding='utf-8') as file:
        historique = json.dump(historique, file, indent=4, ensure_ascii=False)
