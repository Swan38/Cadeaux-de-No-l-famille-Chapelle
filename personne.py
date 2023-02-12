from dataclasses import dataclass
from typing import Dict, Iterable, List
from numbers import Number

from historique import Historique, PersonneHistorique, Offert, Annee


# Could be comparable to other personne or str
@dataclass  # (frozen=True)
class Personne:
    """
    This class is intended to condense information from
    the PersonneHistorique type to speed-up computation.
    """
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
    """
    A key methode that define the cost of making the same gift again from a person to another.
    Necessarry to avoid reapeating the same people again.

    Parameters
    ----------
    offert: Offert
        represent an individual present in the history
    annee: Annee
        the current year, to know how old the present is

    Return
    ------
    : Number
        A positive number that represent the impact of making the same gift again.
    """
    if "année" in offert:
        return 1 / (annee - offert["année"])
    else:
        return .1  # Equivalent to ten year


def get_already_offered_score(personne_hist: PersonneHistorique, participants: Iterable[str],
                              annee: Annee) -> Dict["Personne", int]:
    """
    Compute a look-up table to know the "cost" of making a gift from the given person to every given participant.

    Parameters
    ----------
    personne_hist: PersonneHistorique
        The raw data representing someone in the history
    participants: Iterable[str]
        An iterable of every participant this year.
    annee: Annee
        The current year to evaluate_score.

    Return
    ------
    : Dict["Personne", int]
        A dictionnary used as a look-up table with participant's names as keys
        and the cost for the given people to make them a gift as values.
    """
    already_offered_score = {participant: 0 for participant in participants if participant != personne_hist["nom"]}
    if "offerts" in personne_hist:
        for offert in personne_hist["offerts"]:
            if offert["nom"] not in participants:
                continue
            already_offered_score[offert["nom"]] += evaluate_score(offert, annee)
    return already_offered_score


def get_black_list(personne_hist: PersonneHistorique, participants: Iterable[str]) -> List[str]:
    """
    Get the black list of the given personne filtered with only participants for faster computation.

    Parameters
    ----------
    personne_hist: PersonneHistorique
        The given personne
    participants: Iterable[str]
        The list of participants this year

    Return
    ------
    : List[str]
        The list of black listed participant's names
    """
    if "black_list" in personne_hist:
        return list(set(personne_hist["black_list"]) & set(participants))
    else:
        return []


def get_participant_personne_from_historique(participants: Iterable[str], historique: Historique,
                                             annee: Annee) -> List[Personne]:
    """
    Convert people to Personne object from raw history data for faster computation and greater readability.

    Parameters
    ----------
    participants: Iterable[str]
        The list of every participant this year
    historique: Historique
        History data (freshly loaded json file)
    annee: Annee
        The current year for evaluate_score

    Return
    ------
    : List[Personne]
        A List of Personne objects for each participant
    """
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
