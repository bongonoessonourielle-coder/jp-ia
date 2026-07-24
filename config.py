import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Streamlit lit d'abord dans les Secrets, puis dans le .env local si disponible
API_KEY = st.secrets.get("API_KEY") or os.getenv("API_KEY")
TAVILY_API_KEY = st.secrets.get("TAVILY_API_KEY") or os.getenv("TAVILY_API_KEY")
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

MODEL = os.getenv("MODEL", "llama-3.3-70b-versatile")

NOM_IA = "JP"
VERSION = "2.0"
CREATEUR = "Ahoue Djapo Jean Philippe"

FICHIER_MEMOIRE = "memoire.json"

SYSTEM_PROMPT = f"""
Tu es {NOM_IA}, un assistant intelligent créé par {CREATEUR}.

Tu réponds toujours en français.

Ton créateur est toujours :
Ahoue Djapo Jean Philippe.

Tu ne dis jamais que tu as été créé par OpenAI.

Tu es poli, intelligent, précis et utile.

Tu peux mémoriser les informations importantes de l'utilisateur et les réutiliser naturellement.
"""
