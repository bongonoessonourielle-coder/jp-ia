from tavily import TavilyClient
from config import TAVILY_API_KEY

client = TavilyClient(api_key=TAVILY_API_KEY)

def rechercher(question):
    # --- FILTRE DES SALUTATIONS ET MOTS SIMPLES ---
    mots_ignores = [
        "bonjour", "salut", "coucou", "hello",
        "ça va", "ca va", "comment vas-tu", "comment tu vas",
        "qui es-tu", "tu es qui", "c'est quoi ton nom",
        "merci", "super", "ok", "d'accord", "au revoir", "bye"
    ]

    q_propre = question.lower().strip()

    # Si c'est une salutation ou une question trop courte, pas de recherche Tavily
    if q_propre in mots_ignores or len(q_propre) < 4:
        return "Aucune recherche nécessaire."

    # --- RECHERCHE TAVILY ---
    try:
        resultat = client.search(
            query=question,
            search_depth="advanced",
            max_results=5
        )

        texte = ""
        for r in resultat["results"]:
            texte += f"{r['title']}\n"
            texte += f"{r['content']}\n"
            texte += f"Source : {r['url']}\n\n"

        return texte

    except Exception as e:
        return f"Erreur de recherche : {e}"
