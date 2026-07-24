import json
import os

FICHIER_MEMOIRE = "memoire.json"

def charger_memoire():
    if os.path.exists(FICHIER_MEMOIRE):
        try:
            with open(FICHIER_MEMOIRE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def sauvegarder_cle(cle, valeur):
    memoire = charger_memoire()
    memoire[cle] = valeur
    try:
        with open(FICHIER_MEMOIRE, "w", encoding="utf-8") as f:
            json.dump(memoire, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Erreur de sauvegarde : {e}")
        return False
