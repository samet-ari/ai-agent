import subprocess
import os

def read_file(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        return f"ERREUR: {e}"

def write_file(path, content):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
        with open(path, "w") as f:
            f.write(content)
        return f"Fichier écrit : {path}"
    except Exception as e:
        return f"ERREUR: {e}"

def run_command(command):
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=30
        )
        output = result.stdout or result.stderr
        return output if output else "(pas de sortie)"
    except Exception as e:
        return f"ERREUR: {e}"

TOOLS = [
    {
        "name": "read_file",
        "description": "Lit le contenu d'un fichier",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Chemin du fichier"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "write_file",
        "description": "Crée ou écrit dans un fichier",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Chemin du fichier"},
                "content": {"type": "string", "description": "Contenu à écrire"}
            },
            "required": ["path", "content"]
        }
    },
    {
        "name": "run_command",
        "description": "Exécute une commande terminal",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "Commande à exécuter"}
            },
            "required": ["command"]
        }
    }
]
