# Agent CLI IA 🤖

Un agent IA en ligne de commande capable de comprendre des instructions en langage naturel et d'agir sur le système de fichiers.

## Fonctionnalités

- 📖 Lire des fichiers
- ✏️ Créer et modifier des fichiers
- ⚡ Exécuter des commandes terminal (avec confirmation)
- 💬 Historique de conversation pendant la session

## Stack technique

- **Python 3.11**
- **Groq API** (llama-3.3-70b-versatile)
- **Rich** — interface terminal colorée
- **Docker** — containerisation

## Lancer l'agent
```bash
docker build -t ai-agent .
docker run -it --rm -e GROQ_API_KEY=votre_clé ai-agent
```

## Exemple
```
Vous > Crée un fichier hello.txt avec le contenu "Bonjour le monde"
Outil : write_file
→ Fichier écrit : hello.txt
Agent : J'ai créé le fichier hello.txt avec succès.
```

## Sécurité

L'agent tourne dans un container Docker isolé. Toute commande terminal nécessite une confirmation explicite de l'utilisateur.
