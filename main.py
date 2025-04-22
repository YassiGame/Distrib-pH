from libs.excel_lib import create_xlsx
from libs.terminal_lib import select_multiple_options, save_file_explorer, select_option
from libs.utils import is_float

import matplotlib.pyplot as plt
from numpy import arange

from rich.padding import Padding
from rich.prompt import Prompt
from rich.panel import Panel
from rich import print

# Une liste de pH de 0 a 14 avec un saut de 0,1
LIST_PH: list = list(arange(0, 14.1, 0.1))

# -----> CODE :

print(Panel("😀 Bienvenue dans le diagramme de distribution theoriques 2000",
            subtitle="Créer par Yassi",
            title_align="center",
            subtitle_align="right"))
print()

while True:
    # Partie input
    name_acid = Prompt.ask("〉Nom de [bold]l'acide[/bold]", default="acid", show_default=False)
    name_base = Prompt.ask("〉Nom de [bold]la base[/bold]", default="base", show_default=False)

    while True:
        pKA = Prompt.ask("〉Le pKA [italic](float)[/italic]")
        if is_float(pKA):
            pKA = float(pKA)
            break
        print(Padding(" [underline red]⌦  stp veuillez entrer un nombre valide", (1, 2)))

    # Calcul absorbance de l'acide
    ind_acid = []
    for i in LIST_PH:
        calcul = 100 / (1 + 10 ** (i - pKA))
        ind_acid.append(calcul)

    # Calcul absorbance de la base
    ind_base = []
    for i in ind_acid:
        calcul = 100 - i
        ind_base.append(calcul)

    # ----> Générer le graphique
    plt.title(f"Diagramme de distribution de l'acide ({name_acid}) et de la base ({name_base})", loc='left')

    # Plot acide
    line_acid, = plt.plot(LIST_PH, ind_acid, label=name_acid)
    # Plot base
    line_base, = plt.plot(LIST_PH, ind_base, label=name_base)

    plt.legend(loc="center right")
    plt.ylabel('% indicateurs')
    plt.xlabel('pH')

    # Créer une annotation et la rendre invisible par défaut
    annot = plt.annotate("", xy=(0, 0), xytext=(-20, 20),
                         textcoords="offset points",
                         bbox=dict(boxstyle="round", fc="yellow", alpha=0.5),
                         arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)


    # Créer l'événement de mouvement (Pour le rectangle avec les infos x et y comme dans logger pro)
    def update_annot(event):
        if event.inaxes is not None:
            # Vérifier si le pointeur est sur l'une des lignes
            contained_acid, ind_acid = line_acid.contains(event)
            contained_base, ind_base = line_base.contains(event)

            if contained_acid:
                x, y = line_acid.get_data()
                annot.xy = (x[ind_acid["ind"][0]], y[ind_acid["ind"][0]])
                text = f"pH: {x[ind_acid['ind'][0]]:.1f}\n{name_acid}: {y[ind_acid['ind'][0]]:.2f}%"
            elif contained_base:
                x, y = line_base.get_data()
                annot.xy = (x[ind_base["ind"][0]], y[ind_base["ind"][0]])
                text = f"pH: {x[ind_base['ind'][0]]:.1f}\n{name_base}: {y[ind_base['ind'][0]]:.2f}%"
            else:
                if hasattr(annot, 'get_visible'):
                    annot.set_visible(False)
                    plt.draw()
                return

            annot.set_text(text)
            annot.get_bbox_patch().set_alpha(0.5)
            annot.set_visible(True)
            plt.draw()

    # Connecter l'événement de mouvement de la souris à la fonction update_annot
    plt.connect('motion_notify_event', update_annot)

    # Afficher le graphique
    print("\n[green bold]✓ Graphique generée\n")

    menu = ["Montrer le graphique", "Sauvegarder le graphique", "Exporter en fichier excel"]
    choix = select_multiple_options(menu)

    if "Sauvegarder le graphique" in choix:
        result = save_file_explorer(default_name="diagrame_de_distribution.png")
        plt.savefig(result)
        print("\n[green bold]✓ Fichier sauvegardé")
    if "Exporter en fichier excel":
        result = save_file_explorer(default_name="diagrame_de_distribution.xlsx")
        create_xlsx(file_name=result, acid_name=name_acid, base_name=name_base, ph_list=LIST_PH, pKA=pKA)
        print("\n[green bold]✓ Fichier xlsx créer")
    if "Montrer le graphique" in choix:
        print("\n[green bold]✓ Ouverture du graphique")
        plt.show()

    print()

    menu = ["🧪 Continuer", "🚪 Quitter"]
    choix = select_option(menu)
    print()
    if choix == "🚪 Quitter":
        print("🙌 Au revoir")
        exit()