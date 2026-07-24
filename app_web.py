import base64
import os
import urllib.parse
from dotenv import load_dotenv
from duckduckgo_search import DDGS
import streamlit as st
from ia import JPIA

# 1. Configuration de la page Streamlit
st.set_page_config(
    page_title="JP-IA | Core System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Fonction de Recherche Web
def recherche_internet(query):
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=5):
                results.append(f"• **{r['title']}**: {r['body']}")
        return "\n".join(results) if results else "Aucune information trouvée."
    except Exception as e:
        return f"Erreur de recherche : {e}"


# 2. Styles CSS : Arrière-plan animé sombre (Cyber-Grid)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@600;700&display=swap');

    /* Animation de l'arrière-plan cybernétique */
    @keyframes bgMove {
        0% { background-position: 0 0, 0 0; }
        100% { background-position: 50px 50px, 50px 50px; }
    }

    /* Override du fond Streamlit */
    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stMain"], section.main {
        background: 
            linear-gradient(rgba(0, 240, 255, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 240, 255, 0.05) 1px, transparent 1px),
            radial-gradient(circle at 50% 50%, #0b1329 0%, #030712 100%) !important;
        background-size: 40px 40px, 40px 40px, 100% 100% !important;
        animation: bgMove 8s linear infinite !important;
        color: #00f0ff !important;
    }

    /* TITRE FLOTTANT NÉON */
    @keyframes titleFloat {
        0% { transform: translateY(0px); text-shadow: 0 0 10px rgba(0, 240, 255, 0.7); }
        50% { transform: translateY(-8px); text-shadow: 0 0 25px rgba(0, 240, 255, 1); }
        100% { transform: translateY(0px); text-shadow: 0 0 10px rgba(0, 240, 255, 0.7); }
    }

    .ia-title {
        text-align: center;
        font-family: 'Orbitron', sans-serif;
        font-size: 3.2rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00f0ff, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: titleFloat 4s ease-in-out infinite;
        margin-top: -30px !important;
        margin-bottom: 5px !important;
        display: block;
    }

    .ia-subtitle {
        text-align: center;
        color: #94a3b8 !important;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.05rem;
        font-weight: 600;
        margin-bottom: 25px;
    }

    /* BARRE DE RECHERCHE ET SAISIE */
    div[data-testid="stChatInput"] {
        max-width: 900px !important;
        margin: 0 auto !important;
    }

    div[data-testid="stChatInput"] > div {
        background-color: rgba(11, 19, 41, 0.95) !important;
        border: 2px solid #00f0ff !important;
        border-radius: 25px !important;
        box-shadow: 0 0 18px rgba(0, 240, 255, 0.4) !important;
        backdrop-filter: blur(10px) !important;
    }

    div[data-testid="stChatInput"] textarea {
        color: #00f0ff !important;
        -webkit-text-fill-color: #00f0ff !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1.05rem !important;
    }

    /* BULLES DE CHAT UNIFIÉES */
    [data-testid="stChatMessage"] {
        background-color: rgba(11, 19, 41, 0.9) !important;
        border: 2px solid #00f0ff !important;
        border-radius: 20px !important;
        box-shadow: 0 0 18px rgba(0, 240, 255, 0.35) !important;
        backdrop-filter: blur(8px) !important;
        margin-bottom: 15px !important;
        padding: 12px 18px !important;
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] div,
    [data-testid="stChatMessage"] span {
        color: #00f0ff !important;
        -webkit-text-fill-color: #00f0ff !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: rgba(6, 11, 25, 0.95) !important;
        border-right: 1px solid rgba(0, 240, 255, 0.3) !important;
        backdrop-filter: blur(10px) !important;
    }

    footer, [data-testid="stBottom"], [data-testid="stBottom"] > div {
        background-color: transparent !important;
        background: transparent !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. Initialisation de la Session
if "agent" not in st.session_state:
    st.session_state.agent = JPIA()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "mode" not in st.session_state:
    st.session_state.mode = "chat"

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

# 4. Menu Latéral (Sidebar)
with st.sidebar:
    st.markdown(
        '<h2 style="color:#00f0ff;text-align:center;font-family:\'Orbitron\';">⚡ JP-IA CORE</h2>',
        unsafe_allow_html=True,
    )

    if st.button("➕ Nouvelle discussion", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.mode = "chat"
        st.session_state.uploader_key += 1
        st.rerun()

    st.markdown("---")

    st.markdown(
        "<h4 style='color:#00f0ff;'>📎 Importer / Modifier Image</h4>",
        unsafe_allow_html=True,
    )
    
    # Utilisation d'une clé dynamique pour pouvoir le réinitialiser proprement
    fichier_uploade = st.file_uploader(
        "Uploader une image ou un document",
        type=["png", "jpg", "jpeg", "mp4", "pdf"],
        label_visibility="collapsed",
        key=f"uploader_{st.session_state.uploader_key}"
    )

    st.markdown("---")

    st.markdown(
        "<h4 style='color:#38bdf8;'>🛠️ Studio Multimédia</h4>",
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🖼️ Image", use_container_width=True):
            st.session_state.mode = "image"
        if st.button("🎵 Musique", use_container_width=True):
            st.session_state.mode = "music"
    with col2:
        if st.button("🎥 Vidéo", use_container_width=True):
            st.session_state.mode = "video"
        if st.button("🌐 Recherche", use_container_width=True):
            st.session_state.mode = "search"

    if st.button("💬 Mode Chat classique", use_container_width=True):
        st.session_state.mode = "chat"

    st.markdown(
        f"<p style='text-align:center;color:#38bdf8;margin-top:15px;'>Mode actif : <b>{st.session_state.mode.upper()}</b></p>",
        unsafe_allow_html=True,
    )

# 5. En-tête Principal
st.markdown('<div class="ia-title">⚡ JP-IA CORE v2.0</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="ia-subtitle">Système d\'IA Génératif & Multi-Modal • Créé par Ahoue Djapo Jean Philippe</div>',
    unsafe_allow_html=True,
)

# 6. Affichage des Messages
for msg in st.session_state.chat_history:
    avatar = "👤" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        if msg.get("type") == "image":
            st.image(msg["content"], caption="Généré / Modifié par JP-IA")
        elif msg.get("type") == "music":
            st.audio(msg["content"])
        else:
            st.markdown(msg["content"])

# 7. Champ de Saisie utilisateur
prompt = st.chat_input("Pose une question ou demande une création (image, vidéo, musique)...")

# 8. Logique du traitement
if prompt or fichier_uploade:
    texte_envoye = prompt if prompt else f"Fichier importé : {fichier_uploade.name}"

    # Ajout du message utilisateur
    st.session_state.chat_history.append(
        {"role": "user", "content": texte_envoye, "type": "text"}
    )

    mode = st.session_state.mode

    # CAS A : MODIFICATION D'IMAGE UPLOADÉE
    if fichier_uploade and ("modifier" in texte_envoye.lower() or "transforme" in texte_envoye.lower() or mode == "image"):
        desc = prompt if prompt else "Cyberpunk neon style modification"
        encoded = urllib.parse.quote(desc)
        url_gen = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true"

        st.session_state.chat_history.append(
            {"role": "assistant", "content": url_gen, "type": "image"}
        )

    # CAS B : GÉNÉRATION D'IMAGE
    elif mode == "image" or any(kw in texte_envoye.lower() for kw in ["dessine", "image", "photo", "crée une image"]):
        encoded = urllib.parse.quote(texte_envoye)
        url_img = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true"

        st.session_state.chat_history.append(
            {"role": "assistant", "content": url_img, "type": "image"}
        )

    # CAS C : GÉNÉRATION DE VIDÉO
    elif mode == "video" or any(kw in texte_envoye.lower() for kw in ["vidéo", "animation", "crée une vidéo"]):
        encoded = urllib.parse.quote(f"animated loop video of {texte_envoye}")
        url_vid = f"https://image.pollinations.ai/prompt/{encoded}?width=800&height=450&nologo=true"

        st.session_state.chat_history.append(
            {"role": "assistant", "content": url_vid, "type": "image"}
        )

    # CAS D : GENERATION DE MUSIQUE / AUDIO
    elif mode == "music" or any(kw in texte_envoye.lower() for kw in ["musique", "chanson", "audio", "son"]):
        audio_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
        st.session_state.chat_history.append(
            {"role": "assistant", "content": audio_url, "type": "music"}
        )

    # CAS E : RECHERCHE INTERNET
    elif mode == "search" or any(kw in texte_envoye.lower() for kw in ["recherche", "quand", "qui est", "météo"]):
        infos = recherche_internet(texte_envoye)
        reponse = st.session_state.agent.demander(f"Infos Web :\n{infos}\n\nQuestion : {texte_envoye}")
        st.session_state.chat_history.append(
            {"role": "assistant", "content": reponse, "type": "text"}
        )

    # CAS F : CHAT TEXTE DÉFAUT
    else:
        reponse = st.session_state.agent.demander(texte_envoye)
        st.session_state.chat_history.append(
            {"role": "assistant", "content": reponse, "type": "text"}
        )

    # Réinitialise le file uploader pour éviter la boucle infinie
    if fichier_uploade:
        st.session_state.uploader_key += 1

    st.rerun()
