import json

from personne import Personne


def ask_year() -> int:
    while True:
        année = input("Pour quelle année voulez vous générer les attributions de cadeaux à faire ? ")
        try:
            return int(année)
        except:
            print(f"Ecrivez une année, vous aviez écris \"{année}\"")
            continue


def hard_coded_year() -> int:
    return 2023


def get_historique_for_year(année: int):
    file_path = f"historique/historique_{année - 1}.json"
    print(f"Chargement de : {file_path}")
    historique = json.load(open(file_path, "r", encoding='utf-8'))
    return historique
