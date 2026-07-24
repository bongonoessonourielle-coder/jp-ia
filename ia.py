import json
import os
from openai import OpenAI
import config

client = OpenAI(
    api_key=config.API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

class JPIA:
    def __init__(self):
        self.charger_contexte_systeme()

    def charger_contexte_systeme(self):
        memoire = charger_memoire()
        memoire_texte = ""
        if memoire:
            memoire_texte = f"\nInformations connues sur l'utilisateur : {json.dumps(memoire, ensure_ascii=False)}"

        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT + memoire_texte
            }
        ]

    def analyser_et_memoriser(self, question):
        prompt_memoire = [
            {
                "role": "system",
                "content": (
                    "Tu es un module de mémoire. Analyse la phrase. "
                    "Si l'utilisateur indique une information personnelle importante à retenir "
                    "(ex: ville, plat préféré, projet, prénom, métier), "
                    "réponds STRICTEMENT au format JSON : {\"cle\": \"nom_de_la_cle\", \"valeur\": \"la_valeur\"}. "
                    "Sinon réponds 'RIEN'."
                )
            },
            {"role": "user", "content": question}
        ]

        try:
            resp = client.chat.completions.create(model=MODEL, messages=prompt_memoire)
            txt = resp.choices[0].message.content.strip()
            if txt.startswith("{") and txt.endswith("}"):
                data = json.loads(txt)
                if "cle" in data and "valeur" in data:
                    sauvegarder_cle(data["cle"], data["valeur"])
                    self.charger_contexte_systeme()
        except Exception:
            pass

    def demander(self, question):
        # 1. Analyse et enregistrement en mémoire
        self.analyser_et_memoriser(question)

        # 2. Classification de la question
        prompt_decision = [
            {
                "role": "system",
                "content": (
                    "Analyse la question et réponds par un seul mot :\n"
                    "- 'FICHIER' si l'utilisateur demande de lire, résumer ou analyser un fichier (ex: .txt, .pdf, .py).\n"
                    "- 'RECHERCHE' si la question demande des infos récentes/temps réel (météo, sport, actu).\n"
                    "- 'CALCUL' si la question demande un calcul mathématique ou du code à exécuter.\n"
                    "- 'DISCUTER' pour les salutations, bavardages et culture générale."
                )
            },
            {"role": "user", "content": f"Question : {question}"}
        ]

        decision_resp = client.chat.completions.create(model=MODEL, messages=prompt_decision)
        decision = decision_resp.choices[0].message.content.strip().upper()

        question_finale = question

        # 3. Traitement selon la décision
        if "FICHIER" in decision:
            prompt_nom_fichier = [
                {
                    "role": "system", 
                    "content": "Extrais UNIQUEMENT le nom exact du fichier mentionné avec son extension (ex: test.txt). Ne mets aucun autre mot."
                },
                {"role": "user", "content": question}
            ]
            f_resp = client.chat.completions.create(model=MODEL, messages=prompt_nom_fichier)
            nom_fichier = f_resp.choices[0].message.content.strip().replace("`", "").replace("'", "").replace('"', '')
            
            contenu_fichier = lire_fichier(nom_fichier)
            question_finale = f"Question : {question}\n\nContenu extrait du fichier '{nom_fichier}' :\n{contenu_fichier}"

        elif "RECHERCHE" in decision:
            infos = rechercher(question)
            if "Aucune recherche" not in infos:
                question_finale = f"Question : {question}\n\nInformations Internet :\n{infos}\n\nConsigne : Réponds en français clair."

        elif "CALCUL" in decision:
            prompt_code = [
                {"role": "system", "content": "Écris UNIQUEMENT du code Python exécutable qui fait le calcul et fait un print() du résultat. Aucun autre texte."},
                {"role": "user", "content": question}
            ]
            code_resp = client.chat.completions.create(model=MODEL, messages=prompt_code)
            code_python = code_resp.choices[0].message.content.replace("```python", "").replace("```", "").strip()
            
            res_exec = executer_code(code_python)
            question_finale = f"Question : {question}\n\nRésultat exact du calcul : {res_exec}"

        # 4. Génération de la réponse
        self.messages.append({"role": "user", "content": question_finale})

        reponse = client.chat.completions.create(
            model=MODEL,
            messages=self.messages
        )

        texte = reponse.choices[0].message.content
        self.messages.append({"role": "assistant", "content": texte})

        return texte
