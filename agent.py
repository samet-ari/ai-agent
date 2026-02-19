from groq import Groq
import os
import json
from rich.console import Console
from rich.panel import Panel
from tools import read_file, write_file, run_command, TOOLS

console = Console()
model = "llama-3.3-70b-versatile"
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = "Tu es un agent CLI IA. Tu aides l'utilisateur avec des outils pour lire, ecrire des fichiers et executer des commandes. Reponds en francais."

def run_tool(name, inputs):
    console.print(f"[yellow]Outil : {name}[/yellow]")
    if name == "read_file":
        return read_file(inputs["path"])
    elif name == "write_file":
        return write_file(inputs["path"], inputs["content"])
    elif name == "run_command":
        cmd = inputs["command"]
        console.print(f"[red]Commande : {cmd}[/red]")
        confirm = input("Confirmer ? (o/n) : ")
        if confirm.lower() != "o":
            return "Commande refusee."
        return run_command(cmd)
    return "Outil inconnu"

def chat(user_message, history):
    history.append({"role": "user", "content": user_message})
    while True:
        response = client.chat.completions.create(
            model=model,
            max_tokens=4096,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history,
            tools=TOOLS,
            tool_choice="auto"
        )
        message = response.choices[0].message
        if message.tool_calls:
            history.append({
                "role": "assistant",
                "content": message.content or "",
                "tool_calls": [{"id": tc.id, "type": "function", "function": {"name": tc.function.name, "arguments": tc.function.arguments}} for tc in message.tool_calls]
            })
            for tc in message.tool_calls:
                try:
                    inputs = json.loads(tc.function.arguments)
                except json.JSONDecodeError:
                    console.print("[red]Erreur parsing.[/red]")
                    continue
                result = run_tool(tc.function.name, inputs)
                console.print(f"[dim]-> {result[:300]}[/dim]")
                history.append({"role": "tool", "tool_call_id": tc.id, "content": result})
        else:
            history.append({"role": "assistant", "content": message.content or ""})
            if message.content:
                console.print(Panel(message.content, title="[green]Agent[/green]", border_style="green"))
            break
    return history

def main():
    console.print(Panel(f"[bold]Agent CLI IA[/bold]\nModele : {model}\nTaper 'exit' pour quitter", border_style="cyan"))
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
