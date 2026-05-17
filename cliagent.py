

import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.rule import Rule
from rich import print as rprint

from agents.dr_pal import DrPal

console = Console()


def print_banner():
    banner = Text()
    banner.append("\n  ██████╗  █████╗ ██╗      █████╗ ██╗\n", style="bold green")
    banner.append("  ██╔══██╗██╔══██╗██║     ██╔══██╗██║\n", style="bold green")
    banner.append("  ██████╔╝███████║██║     ███████║██║\n", style="bold cyan")
    banner.append("  ██╔═══╝ ██╔══██║██║     ██╔══██║██║\n", style="bold cyan")
    banner.append("  ██║     ██║  ██║███████╗██║  ██║██║\n", style="bold blue")
    banner.append("  ╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝\n", style="bold blue")
    banner.append("\n  Your AI Health Advisor — Daily Check-in\n", style="dim")
    console.print(banner)


def print_welcome(session_id: str):
    today = datetime.now().strftime("%A, %B %d %Y")
    console.print(Panel(
        f"[bold white]Session started for[/bold white] [cyan]{session_id}[/cyan]\n"
        f"[dim]{today}[/dim]\n\n"
        "[dim]Type [/dim][yellow]'report'[/yellow][dim] to generate your daily report\n"
        "Type [/dim][yellow]'history'[/yellow][dim] to see conversation\n"
        "Type [/dim][yellow]'clear'[/yellow][dim] to start fresh\n"
        "Type [/dim][yellow]'quit'[/yellow][dim] to exit[/dim]",
        "Type [/dim][yellow]'ask'[/yellow][dim] to buit-in questioning[/dim]",
        "Type [/dim][yellow]'fixes'[/yellow][dim] to know the improvment area [/dim]",
        title="[bold green]Dr. Pal[/bold green]",
        border_style="green",
        padding=(1, 2),
    ))
