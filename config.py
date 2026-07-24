import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Clés API (Priorité aux Secrets Streamlit, puis au .env local)
API_KEY = st.secrets.get("API_KEY") or st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY") or os.getenv("API_KEY")
TAVILY_API_KEY = st.secrets.get("TAVILY_API_KEY") or os.getenv("TAVILY_API_KEY")

MODEL = os.getenv("MODEL", "llama-3.3-70b-versatile")

NOM_IA = "JP"
VERSION = "2.0"
CREATEUR = "Ahoue Djapo Jean Philippe"

FICHIER_MEMOIRE = "memoire.json"

SYSTEM_PROMPT = f"""
Tu es {NOM_IA}, un assistant intelligent créé par {CREATEUR}.
"""
