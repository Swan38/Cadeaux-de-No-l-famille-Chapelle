from pprint import pprint
from typing import Dict, List, Tuple

from historique import *
from participation import *
from personne import *


# annee = 2023
annee = ask_year()
historique = get_historique_for_year(annee)
# participants = hard_coded_participants_2023()  # [:10]
participants = ask_participants(historique)

participants_personnes = get_participant_personne_from_historique(participants, historique, annee)
participants_personnes.sort(key=lambda personne: len(personne.black_list), reverse=True)

# pprint(participants_personnes)

possible_loop: Dict[int, List[Personne]] = {}
exploring_memory: Dict[int, Tuple[List[Personne], List[Personne]]] = {
    (min_score := 0): [
        ([participants_personnes[0]], participants_personnes[1:])
    ]}

# While a better solution can steel be found
while all(map(lambda possible_score: possible_score > min_score, possible_loop)):
    if len(exploring_memory[min_score]) == 0:
        del exploring_memory[min_score]
        min_score = min(exploring_memory)
        continue

    fixed: List[Personne]
    left: List[Personne]
    fixed, left = exploring_memory[min_score].pop()
    donneur = fixed[-1]
    for i, receveur in enumerate(left):
        if receveur.name in donneur.black_list:
            continue
        current_gift_score = donneur.already_offered_score[receveur.name]
        if len(left) == 1:
            if fixed[0].name in receveur.black_list:
                continue
            closing_loop_gift_score = receveur.already_offered_score[fixed[0].name]
            possible_loop[min_score + current_gift_score + closing_loop_gift_score] = fixed + [receveur]
        else:
            if min_score + current_gift_score not in exploring_memory:
                exploring_memory[min_score + current_gift_score] = []
            exploring_memory[min_score + current_gift_score].append((fixed + [receveur], left[:i] + left[i + 1:]))

choosen_score = min(possible_loop)
choosen_loop = possible_loop[choosen_score]

print(
    f"The optimal order (score={choosen_score}) is:",
    list(map(lambda personne: personne.name, choosen_loop))
    )

print("Adding theses results to the history...")

new_historique = update_historique(
    historique,
    zip(choosen_loop, choosen_loop[1:] + choosen_loop[:1]),
    annee
    )
set_historique_for_year(new_historique, annee)
