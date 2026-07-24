import json
import os
from openai import OpenAI
import config

# Import des fonctions de mémoire et outils
try:
    from memoire import charger_memoire, sauvegarder_memoire
except ImportError:
    def charger_memoire(): return {}
    def sauvegarder_memoire(data): pass

class JPIA:
    def __init__(self):
        # Utilisation de la clé définie dans config.py
        api_key = config.API_KEY
        
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        self.charger_contexte_systeme()

    def charger_contexte_systeme(self):
        memoire = charger_memoire()
        memoire_texte = ""
        if memoire:
            memoire_texte = f"\nInformations connues sur l'utilisateur : {json.dumps(memoire, ensure_ascii=False)}"

        self.messages = [
            {
                "role": "system",
                "content": getattr(config, 'SYSTEM_PROMPT', 'Tu es un assistant IA.') + memoire_texte
            }
        ]

    def demander(self, question):
        self.messages.append({"role": "user", "content": question})
        
        try:
            response = self.client.chat.completions.create(
                model=getattr(config, 'MODEL', 'llama-3.3-70b-versatile'),
                messages=self.messages
            )
            reponse_texte = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": reponse_texte})
            return reponse_texte
        except Exception as e:
            return f"Erreur lors de la génération : {str(e)}"
