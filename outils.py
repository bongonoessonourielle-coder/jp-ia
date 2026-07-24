import sys
import io
import os
from pypdf import PdfReader

def executer_code(code_python):
    """Exécute du code Python et renvoie le résultat imprimé."""
    buffer = io.StringIO()
    sys.stdout = buffer
    variables_locales = {}
    
    try:
        exec(code_python, {}, variables_locales)
        sys.stdout = sys.__stdout__
        resultat = buffer.getvalue().strip()
        if not resultat:
            return "Code exécuté avec succès (aucun résultat affiché)."
        return resultat
    except Exception as e:
        sys.stdout = sys.__stdout__
        return f"Erreur d'exécution : {e}"

def lire_fichier(chemin_fichier):
    """Lit le contenu d'un fichier texte ou PDF."""
    if not os.path.exists(chemin_fichier):
        return f"Erreur : Le fichier '{chemin_fichier}' n'existe pas."

    ext = os.path.splitext(chemin_fichier)[1].lower()

    try:
        # Fichier PDF
        if ext == ".pdf":
            reader = PdfReader(chemin_fichier)
            texte = ""
            for page in reader.pages:
                texte += page.extract_text() + "\n"
            return texte[:4000] # Limite à 4000 caractères pour ne pas tout dépasser

        # Fichier Texte / Code / Markdown
        else:
            with open(chemin_fichier, "r", encoding="utf-8") as f:
                return f.read()[:4000]

    except Exception as e:
        return f"Erreur lors de la lecture du fichier : {e}"
