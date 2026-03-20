"""
Aegis AI — Terminal-Based Cybersecurity & Coding Assistant
Powered by Groq API | Model: openai/gpt-oss-120b
"""

import os
import sys
from groq import Groq
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.text import Text
from rich import box

# ─── Init ────────────────────────────────────────────────────────────────────

console = Console()

SYSTEM_PROMPT = """You are Aegis AI, an elite terminal-based assistant specializing in:
- Cybersecurity (concepts, tools, techniques, CTF, pentesting, OSINT, networking)
- Programming (Python, Bash, C, JavaScript, and more)
- Linux commands and system administration
- Debugging errors and analyzing code
- Scripting and automation

Rules you MUST follow:
1. Keep responses SHORT, CLEAR, and PRACTICAL.
2. Always prefer real command examples when relevant.
3. Use code blocks for commands and code snippets.
4. Never execute commands yourself — only suggest them.
5. If user shares an error or code, debug it directly.
6. Be direct. Skip unnecessary fluff or long intros.
7. Use bullet points for multi-step answers.
"""

chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]


# ─── Banner ───────────────────────────────────────────────────────────────────

def show_banner():
    banner_text = Text()
    banner_text.append("  ▄▄▄       ▓█████   ▄████  ██▓  ██████ \n", style="bold cyan")
    banner_text.append(" ▒████▄     ▓█   ▀  ██▒ ▀█▒▓██▒▒██    ▒ \n", style="bold cyan")
    banner_text.append(" ▒██  ▀█▄   ▒███   ▒██░▄▄▄░▒██▒░ ▓██▄   \n", style="bold cyan")
    banner_text.append(" ░██▄▄▄▄██  ▒▓█  ▄ ░▓█  ██▓░██░  ▒   ██▒\n", style="bold cyan")
    banner_text.append("  ▓█   ▓██▒ ░▒████▒░▒▓███▀▒░██░▒██████▒▒\n", style="bold cyan")
    banner_text.append("  ▒▒   ▓▒█░ ░░ ▒░ ░ ░▒   ▒ ░▓  ▒ ▒▓▒ ▒ ░\n", style="dim cyan")
    banner_text.append("   ▒   ▒▒ ░  ░ ░  ░  ░   ░  ▒ ░░ ░▒  ░ ░\n", style="dim cyan")
    banner_text.append("   ░   ▒       ░   ░ ░   ░  ▒ ░░  ░  ░  \n", style="dim cyan")
    banner_text.append("       ░  ░    ░  ░      ░  ░        ░  \n", style="dim cyan")

    console.print(Panel(
        banner_text,
        title="[bold green]⚡ AEGIS AI[/bold green]",
        subtitle="[dim]Cybersecurity & Coding Terminal Assistant[/dim]",
        border_style="cyan",
        box=box.DOUBLE_EDGE,
        padding=(0, 2),
    ))

    console.print(
        "  [dim]Model:[/dim] [cyan]openai/gpt-oss-120b[/cyan]  "
        "[dim]|[/dim]  [dim]Type[/dim] [bold white]exit[/bold white] [dim]or[/dim] [bold white]quit[/bold white] [dim]to leave[/dim]  "
        "[dim]|[/dim]  [dim]Type[/dim] [bold white]clear[/bold white] [dim]to reset chat[/dim]\n"
    )


# ─── AI Engine ────────────────────────────────────────────────────────────────

def ask_ai(user_input: str) -> str:
    """Send user input to Groq API and return the assistant's response."""
    chat_history.append({"role": "user", "content": user_input})

    try:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            return "[red]Error:[/red] GROQ_API_KEY environment variable not set."

        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=chat_history,
            temperature=0.5,
            max_tokens=1024,
        )

        reply = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": reply})
        return reply

    except Exception as e:
        # Remove the user message if request failed
        chat_history.pop()
        return f"[red]API Error:[/red] {str(e)}"


# ─── Main Loop ────────────────────────────────────────────────────────────────

def main():
    show_banner()

    while True:
        try:
            # Prompt
            user_input = Prompt.ask("[bold green]┌─[You][/bold green]\n[bold green]└─>[/bold green]").strip()

            # Empty input guard
            if not user_input:
                continue

            # Exit commands
            if user_input.lower() in ("exit", "quit"):
                console.print("\n[bold cyan]Aegis AI:[/bold cyan] [dim]Stay sharp. Goodbye.[/dim]\n")
                sys.exit(0)

            # Clear chat history
            if user_input.lower() == "clear":
                global chat_history
                chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]
                console.clear()
                show_banner()
                console.print("[dim]Chat history cleared.[/dim]\n")
                continue

            # Show thinking indicator
            console.print("[bold cyan]┌─[Aegis AI][/bold cyan]")
            with console.status("[dim cyan]Thinking...[/dim cyan]", spinner="dots"):
                reply = ask_ai(user_input)

            # Render response as Markdown
            console.print("[bold cyan]└─>[/bold cyan]", end=" ")
            console.print(Markdown(reply))
            console.print()

        except KeyboardInterrupt:
            console.print("\n\n[bold cyan]Aegis AI:[/bold cyan] [dim]Interrupted. Use 'exit' to quit cleanly.[/dim]\n")
            continue


# ─── Entry Point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
