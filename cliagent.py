

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
        "[dim]Type '[/dim][yellow]report[/yellow][dim]' to generate your daily report[/dim]\n"
        "[dim]Type '[/dim][yellow]history[/yellow][dim]' to see conversation[/dim]\n"
        "[dim]Type '[/dim][yellow]clear[/yellow][dim]' to start fresh[/dim]\n"
        "[dim]Type '[/dim][yellow]quit[/yellow][dim]' to exit[/dim]\n"
        "[dim]Type '[/dim][yellow]ask[/yellow][dim]' for built-in questioning[/dim]\n"
        "[dim]Type '[/dim][yellow]fixes[/yellow][dim]' to know the improvement area[/dim]",
        title="[bold green]Dr. Pal[/bold green]",
        border_style="green",
        padding=(1, 2),
    ))



def print_dr_pal(response: str):
    """Print Dr. Pal's response in a styled panel."""
    console.print()
    console.print(Panel(
        Markdown(response),
        title="[bold green]🩺 Dr. Pal[/bold green]",
        border_style="green",
        padding=(1, 2),
    ))
    console.print()


def print_user(message: str):
    """Echo the user message styled."""
    console.print(
        f"[dim]You:[/dim] [bold white]{message}[/bold white]",
        style="white"
    )


def run_cli():
    """Main CLI loop."""
    print_banner()

    # Get or default session ID
    session_id = Prompt.ask(
        "[dim]Enter your name / session ID[/dim]",
        default="user_1"
    )

    print_welcome(session_id)

    # Initialise agent
    agent = DrPal(session_id=session_id)

    # Opening message from Dr. Pal
    opening = agent.chat(
        "Hello, please greet the user warmly and start the daily check-in. "
        "Ask about their night first — how they slept."
    )
    print_dr_pal(opening)

    # ── Main conversation loop ──────────────────────────────────────
    while True:
        try:
            user_input = Prompt.ask("[bold cyan]You[/bold cyan]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Goodbye! Stay healthy. 👋[/dim]")
            break

        if not user_input:
            continue

        # ── Special commands ────────────────────────────────────────
        if user_input.lower() == "quit":
            console.print("\n[dim]Session ended. See you tomorrow! 👋[/dim]")
            break

        elif user_input.lower() == "clear":
            agent.clear_session()
            console.print("[yellow]Session cleared.[/yellow]")
            continue

        elif user_input.lower() == "history":
            history = agent.get_history()
            if not history:
                console.print("[dim]No history yet.[/dim]")
            for msg in history:
                role = "🩺 Dr. Pal" if msg["role"] == "ai" else "👤 You"
                console.print(Rule(f"[dim]{role}[/dim]", style="dim"))
                console.print(Markdown(msg["content"]))
            continue

        elif user_input.lower() == "report":
            console.print("[yellow]Generating your full daily report...[/yellow]")
            report_prompt = (
                "Based on everything I have told you so far today, please generate "
                "my complete Daily Health Report in your full structured format. "
                "Include all sections: nutrition analysis, physical performance, "
                "mental assessment, sleep analysis, cross-domain insights, and "
                "tomorrow's top 3 priority actions."
            )
            response = agent.chat(report_prompt)
            print_dr_pal(response)
            continue

        elif user_input.lower()=="fixes":
            console.print("[yellow]Generating fixes for your lifestyle...[/yellow]")
            report_prompt = (
                "Based on everything I have told you so far today, please generate "
                "What fixes can be done to improve the current scene "
                "Include all sections: nutrition analysis, physical performance, "
                "mental assessment, sleep analysis, cross-domain insights, study and "
                "tomorrow's top 3 priority actions."
            )
            response = agent.chat(report_prompt)
            print_dr_pal(response)
            continue

        elif user_input.lower()=="ask":
            console.print("[yellow]...[/yellow]")
            report_prompt = (
               "Act a Pro who can explain anything soo ask question about"
               "whole day activities what person do whole day "
               "include all sections : breakfast , lunch , dinner , snack , timings ,workout, study , tech learn "
               "ask one by one not the whole summary in on "
               "ask further details if required for better understanding "
               
            )
            response = agent.chat(report_prompt)
            print_dr_pal(response)
            continue


        with console.status("[dim]Dr. Pal is thinking...[/dim]", spinner="dots"):
            response = agent.chat(user_input)

        print_dr_pal(response)


if __name__ == "__main__":
    run_cli()
