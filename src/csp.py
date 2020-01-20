import json

from minizinc import Instance, Model, Solver


def modelize_seaux(nb_seaux=3, max_etapes=10, contenance_max=None, contenu=None, fin=None):
    if contenu is None:
        contenu = [8, 0, 0]
    if fin is None:
        fin = [4, 4, 0]
    if contenance_max is None:
        contenance_max = [8, 5, 3]
    seaux = Model("./seaux.mzn")
    gecode = Solver.lookup("gecode")
    instance = Instance(gecode, seaux)
    instance["nb_seaux"] = nb_seaux
    instance["max_etapes"] = max_etapes
    instance["contenance_max"] = contenance_max
    instance["contenu"] = contenu
    instance["fin"] = fin
    return instance.solve()


def modelize_riviere(nb_bison=3, max_etapes=10):
    seaux = Model("./riviere.mzn")
    gecode = Solver.lookup("gecode")
    instance = Instance(gecode, seaux)
    instance["nb_bison"] = nb_bison
    instance["max_etapes"] = max_etapes
    return instance.solve()


def create_config_seaux(num_config=1, nb_seaux=3, max_etapes=10, contenance_max=None, contenu=None, fin=None):
    if contenu is None:
        contenu = [8, 0, 0]
    if fin is None:
        fin = [4, 4, 0]
    if contenance_max is None:
        contenance_max = [8, 5, 3]

    solution = modelize_seaux(nb_seaux=nb_seaux, max_etapes=max_etapes, contenance_max=contenance_max, contenu=contenu,
                              fin=fin)

    if solution:
        config = {
            'nb seaux': nb_seaux,
            'nb etapes': solution['n_etape_fin'],
            'initial': contenu,
            'final': fin,
            'contenance max': contenance_max,
            'solution': solution['etat'][:solution['n_etape_fin']],
        }
        with open('seaux' + str(num_config) + '.json', 'w') as conf:
            json.dump(config, conf)
    else:
        print('Le modele ne possede aucune solution')


def create_config_riviere(num_config=1, nb_bison=3, max_etapes=10):
    solution = modelize_riviere(nb_bison=nb_bison, max_etapes=max_etapes)

    if solution:
        config = {
            'nb bisons': nb_bison,
            'nb etapes': solution['total_steps'],
            'solution': solution['actions'][:solution['total_steps']],
            'transferts': list(map(list, solution['transfered'])),
        }
        with open('riviere' + str(num_config) + '.json', 'w') as conf:
            json.dump(config, conf)
    else:
        print('Le modele ne possede aucune solution')
