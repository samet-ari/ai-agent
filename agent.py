import anthropic
import os
import sys
from rich.console import Console
from rich.panel import Panel
from tools import read_file, write_file, run_command, TOOLS

console = Console()

PREMIUM_MODEL = "claude-opus-4-5"
MINI_MODEL = "claude-haiku-4-5"

use_premium = "--premium" in sys.argv
model = PREMIUM_MODEL if use_premium else MINI_MODEL

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """Tu es un agent CLI IA. Tu aides l'utilisateur en utilisant 
des outils pour lire, écrire des fichiers et exécuter des commandes terminal.
Explique brièvement ce que tu fais à chaque étape. Réponds en français."""

def run_tool(name, inputs):
    console.print(f"[yellow]⚙ Outil : {name}[/yellow]")
    if name == "read_file":
        return read_file(inputs["path"])
    elif name == "write_file":
        return write_file(inputs["path"], inputs["content"])
    elif name == "run_command":
        cmd = inputs["command"]
        console.print(f"[red]⚠ Commande à exécuter : {cmd}[/red]")
        confirm = input("Confirmer ? (o/n) : ")
        if confirm.lower() != "o":
            return "Commande refusée par l'utilisateur."
        return run_command(cmd)
    return "Outil inconnu"

def chat(user_message, history):
    history.append({"role": "user", "content": user_message})

    while True:
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=history
        )

        history.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    console.print(Panel(block.text, title="[green]Agent[/green]", border_style="green"))
            break

        elif response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = run_tool(block.name, block.input)
                    console.print(f"[dim]→ {result[:300]}[/dim]")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })
            history.append({"role": "user", "content": tool_results})
        else:
            break

    return history

def main():
    model_label = f"[magenta]{PREMIUM_MODEL}[/magenta]" if use_premium else f"[cyan]{MINI_MODEL}[/cyan]"
    console.print(Panel(
        f"[bold]Agent CLI IA[/bold]\nModèle : {model_label}\nTaper 'exit' pour quitter",
        border_style="cyan"
    ))

    history = []
    while True:
        try:
            user_input = console.input("[bold blue]Vous > [/bold blue]")
            if user_input.lower() in ["exit", "quit"]:
                console.print("[dim]Au revoir ![/dim]")
                break
            if not user_input.strip():
                continue
            history = chat(user_input, history)
        except KeyboardInterrupt:
            console.print("\n[dim]Interruption.[/dim]")
            break

if __name__ == "__main__":
    main()
