# ───── Menu à explorateur de fichiers ─────────────────────────────────────────────────
import sys
from pathlib import Path

from readchar import readkey, key
from rich.align import Align
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.console import Console


def render_browse_table(
    current: Path,
    children: list[Path],
    idx: int,
    page_size: int
) -> Table:
    """
    Prépare une table paginée des dossiers pour Live display.
    """
    # calcul de la fenêtre visible
    start = max(0, idx - page_size // 2)
    end = min(len(children), start + page_size)
    if end - start < page_size:
        start = max(0, end - page_size)
    visible = children[start:end]

    table = Table(show_header=False, padding=(0, 1))
    table.add_row(f":open_file_folder: [bold cyan]{current}[/]")
    table.add_row("")  # espacement
    for i, child in enumerate(visible, start):
        prefix = "→" if i == idx else "  "
        style = "reverse bold" if i == idx else ""
        row = Text(f"{prefix} {child.name}", style=style)
        table.add_row(row)
    return table


def browse_directory_for_save(start_path: Path = None, page_size: int = 10) -> Path | None:
    """
    Explorateur interactif optimisé pour la sauvegarde :
    - Affiche une page de `page_size` dossiers
    - ↑/↓ : naviguer
    - → ou Entrée : entrer
    - ← ou Backspace : remonter
    - s : sélectionner
    - q : annuler
    Retourne le dossier sélectionné, ou None.
    """
    console = Console()
    if start_path is None:
        start_path = Path.home() / "Documents"
    current = start_path.resolve()

    # boucle principale, Live wrapping
    idx = 0
    checked_dir = None
    while True:
        # lister uniquement les répertoires
        children = sorted([p for p in current.iterdir() if p.is_dir()], key=lambda p: p.name.lower())
        # gestion dossier vide
        if not children:
            console.clear()
            console.print(f"[red]Le dossier {current} est vide.[/]")
            console.print("Appuyez sur ← (Backspace) pour revenir ou q pour quitter.")
            k = readkey()
            if k in (key.LEFT, key.BACKSPACE) and current.parent != current:
                current = current.parent
                idx = 0
                continue
            elif k.lower() == 'q':
                return None
            else:
                continue

        # reset idx si hors borne
        idx %= len(children)

        # instructions, on ajoute en footer
        console.print("\n[bold]↑[/] [bold]↓[/] naviguer   [bold]→[/] entrer   [bold]←[/] remonter   [bold]s[/] sélectionner   [bold]q[/] quitter")

        # Live context for this directory
        with Live(console=console, refresh_per_second=10) as live:
            while True:
                # mise à jour du panneau
                table = render_browse_table(current, children, idx, page_size)
                panel = Panel(table, title="Sélecteur de dossier", border_style="magenta", padding=(1, 2))
                live.update(panel)

                k = readkey()
                if k == key.UP and children:
                    idx = (idx - 1) % len(children)
                elif k == key.DOWN and children:
                    idx = (idx + 1) % len(children)
                elif k in (key.RIGHT, key.ENTER) and children:
                    current = children[idx]
                    idx = 0
                    break  # entrer dans le dossier
                elif k in (key.LEFT, key.BACKSPACE):
                    if current.parent != current:
                        current = current.parent
                        idx = 0
                    break
                elif k.lower() == 's':
                    checked_dir = current
                    break
                elif k.lower() == 'q':
                    return None
        # fin Live context
        if checked_dir:
            return checked_dir
        # sinon, on boucle dans nouveau dossier


def save_file_explorer(default_name: str = "nouveau_fichier.txt") -> Path | None:
    console = Console()
    target_dir = browse_directory_for_save()
    if target_dir is None:
        console.print("\n[red]Sauvegarde annulée.[/]")
        return None

    console.clear()
    console.print(f"Sauvegarde dans : [bold green]{target_dir}[/]\n")
    console.print(f"Entrez le nom du fichier (par défaut: [italic]{default_name}[/]) :", end=" ")
    name = sys.stdin.readline().strip() or default_name
    file_path = target_dir / name
    console.print(f"\n[bold green]Fichier prêt à être sauvegardé :[/] {file_path}")
    return file_path

# ───── Menu à choix ─────────────────────────────────────────────────

def render_menu(options: list[str], selected: int, prompt: str | None) -> Panel:
    table = Table.grid(padding=(0, 1))
    for i, opt in enumerate(options):
        style = "reverse bold" if i == selected else ""
        row = Text(opt, style=style) if style else Text(opt)
        table.add_row(row)
    title = Text(prompt, style="bold white on blue", justify="center") if prompt else None
    return Panel(Align.center(table), title=title, border_style="cyan", padding=(1, 2))

def select_option(
    options: list[str],
    prompt: str | None = "→ ↑/↓ naviguer — Entrée valider"
) -> str:
    console = Console()
    selected = 0
    with Live(render_menu(options, selected, prompt), console=console, refresh_per_second=10) as live:
        while True:
            k = readkey()
            if k == key.UP:
                selected = (selected - 1) % len(options)
            elif k == key.DOWN:
                selected = (selected + 1) % len(options)
            elif k == key.ENTER:
                return options[selected]
            live.update(render_menu(options, selected, prompt))


# ───── Menu à cases à cocher ─────────────────────────────────────────────────

def render_check_menu(
    options: list[str],
    selected: int,
    checked: set[int],
    prompt: str | None
) -> Panel:
    table = Table.grid(padding=(0, 1))
    for i, opt in enumerate(options):
        mark = "[X]" if i in checked else "[ ]"
        text = f"{mark} {opt}"
        style = "reverse bold" if i == selected else ""
        row = Text(text, style=style) if style else Text(text)
        table.add_row(row)
    title = Text(prompt, style="bold white on green", justify="center") if prompt else None
    return Panel(Align.center(table), title=title, border_style="green", padding=(1, 2))

def select_multiple_options(
    options: list[str],
    prompt: str | None = "→ ↑↓ naviguer — Espace cocher — Entrée valider"
) -> list[str]:
    console = Console()
    selected = 0
    checked: set[int] = set()
    with Live(render_check_menu(options, selected, checked, prompt), console=console, refresh_per_second=10) as live:
        while True:
            k = readkey()
            if k == key.UP:
                selected = (selected - 1) % len(options)
            elif k == key.DOWN:
                selected = (selected + 1) % len(options)
            elif k == key.SPACE:
                if selected in checked:
                    checked.remove(selected)
                else:
                    checked.add(selected)
            elif k == key.ENTER:
                return [options[i] for i in sorted(checked)]
            live.update(render_check_menu(options, selected, checked, prompt))