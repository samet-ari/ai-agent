# COPILOT.md — Spécification de l'Agent CLI IA

## 1. Objectif du projet
Un agent CLI IA qui permet à l'utilisateur de donner des instructions
en langage naturel depuis le terminal. L'agent peut lire et écrire des
fichiers, et exécuter des commandes terminal.

---

## 2. Stack technique

- **Langage :** Python 3.11
- **SDK IA :** anthropic (Tool Use API)
- **UI :** rich (interface terminal colorée)
- **Container :** Docker (python:3.11-slim)
- **Versioning :** Git

---

## 3. Architecture
```
input utilisateur
      ↓
  agent.py (orchestrateur)
      ↓
  Anthropic API (claude-haiku-4-5)
      ↓
  décision tool call ?
    ├── read_file  → tools.py
    ├── write_file → tools.py
    └── run_command → tools.py (confirmation requise)
      ↓
  résultat renvoyé à l'API
      ↓
  réponse finale affichée à l'utilisateur
```

---

## 4. Stratégie de tokens

- **Modèle par défaut :** `claude-haiku-4-5` (mini, économique)
- **Modèle premium :** `claude-opus-4-5` (max 1 fois/jour, flag `--premium`)

---

## 5. Outils disponibles (Tools)

| Outil | Description | Sécurité |
|-------|-------------|----------|
| `read_file` | Lit le contenu d'un fichier | Aucune |
| `write_file` | Crée ou écrit un fichier | Aucune |
| `run_command` | Exécute une commande terminal | Confirmation utilisateur obligatoire |

---

## 6. Structure des fichiers
```
ai-agent/
├── agent.py          # Orchestrateur principal, boucle CLI
├── tools.py          # Fonctions et définitions des outils
├── Dockerfile        # Configuration du container
├── requirements.txt  # Dépendances Python
├── COPILOT.md        # Ce fichier (spécification)
└── SESSION.md        # Résumé de fin de session (créé à la fin)
```

---

## 7. Critères de succès

- [ ] L'utilisateur peut donner des instructions en langage naturel
- [ ] L'agent peut lire des fichiers
- [ ] L'agent peut créer et modifier des fichiers
- [ ] L'agent peut exécuter des commandes terminal (avec confirmation)
- [ ] Fonctionne dans un container Docker
- [ ] L'historique de conversation est conservé pendant la session
- [ ] Le modèle premium est utilisable via le flag `--premium`

---

## 8. Sécurité

- `run_command` demande une confirmation `o/n` à chaque exécution
- L'agent tourne dans un container Docker isolé
- La clé API est passée via variable d'environnement, jamais dans le code
