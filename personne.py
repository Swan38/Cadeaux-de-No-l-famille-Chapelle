from dataclasses import dataclass
from typing import Dict, Iterable, List
from numbers import Number

from historique import Historique, PersonneHistorique, Offert, Annee


# Could be comparable to other personne or str
@dataclass  # (frozen=True)
class Personne:
    name: str
    already_offered_score: Dict["Personne", int]
    black_list: List[str]

    # def __eq__(self, other):
    #     if isinstance(other, Personne):
    #         return self.name == other.name
    #     elif isinstance(other, str):
    #         return self.name == other
    #     elif isinstance(other, dict):
    #         return self.name == other["nom"]
    #     return NotImplemented
    # def __hash__(self):
    #     return hash(self.name)


def evaluate_score(offert: Offert, annee: Annee) -> Number:
    if "année" in offert:
        return 1 / (annee - offert["année"])
    else:
        return .1  # Equivalent to ten year


def get_already_offered_score(personne_hist: PersonneHistorique, participants: Iterable[str], annee: int) -> Dict["Personne", int]:
    already_offered_score = {participant: 0 for participant in participants if participant != personne_hist["nom"]}
    if "offerts" in personne_hist:
        for offert in personne_hist["offerts"]:
            if offert["nom"] not in participants:
                continue
            already_offered_score[offert["nom"]] += evaluate_score(offert, annee)
    return already_offered_score


def get_black_list(personne_hist: PersonneHistorique, participants: Iterable[str]) -> List[str]:
    if "black_list" in personne_hist:
        return list(set(personne_hist["black_list"]) & set(participants))
    else:
        return []


def get_participant_personne_from_historique(participants: Iterable[str], historique: Historique, annee: Annee) -> List[Personne]:
    personnes = []
    for participant in participants:
        for personne_hist in historique:
            if personne_hist["nom"] == participant:
                personnes.append(Personne(
                    participant,
                    get_already_offered_score(personne_hist, participants, annee),
                    get_black_list(personne_hist, participants)
                    ))
                break
        else:
            personnes.append(Personne(
                participant,
                get_already_offered_score({"nom": participant}, participants, annee),
                get_black_list({"nom": participant}, participants)
                ))
    return personnes
