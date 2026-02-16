import streamlit as st
import urllib.parse
import pandas as pd
import base64 

# Configuración de la página
st.set_page_config(page_title="EL TACO LOCO", page_icon="🌮", layout="wide")

# --- FUNCIÓN DE CALLBACK ---
def agregar_al_carrito(producto, tipo):
    if 'carrito' not in st.session_state:
        st.session_state.carrito = {}
    
    if producto in st.session_state.carrito:
        st.session_state.carrito[producto] += 1
    else:
        st.session_state.carrito[producto] = 1
        
    icono = "🔥" if tipo == "taco" else "🧊"
    st.toast(f"¡{producto} agregado!", icon=icono)

# --- FUNCIÓN PARA LEER EL LOGO ---
def get_img_as_base64(file):
    try:
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

img_path = "imagenes/logo.png" 
logo_base64 = get_img_as_base64(img_path)

# --- ESTILOS CSS ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700;900&display=swap" rel="stylesheet">

<style>
:root {
    --color-naranja: #FF6B00;
    --color-rojo: #D32F2F;
    --color-verde: #2E7D32;
    --color-crema: #FFF8E1;
}

.stApp { background-color: var(--color-crema); font-family: 'Poppins', sans-serif; }
h1, h2, h3, h4, p, div, span, label, li { color: #212121 !important; }

/* ========================= */
/* OCULTAR HEADER STREAMLIT  */
/* ========================= */

/* Oculta menú de tres puntos */
#MainMenu { visibility: hidden; }

/* Oculta footer */
footer { visibility: hidden; }

/* Oculta barra superior completa (logo GitHub / Deploy) */
header[data-testid="stHeader"] { display: none; }

/* Quita espacio vacío superior */
.block-container { padding-top: 1rem; }

/* ========================= */
/* TU DISEÑO ORIGINAL        */
/* ========================= */

/* HEADER */
.header-container {
    background: linear-gradient(135deg, var(--color-naranja), var(--color-rojo));
    padding: 2rem;
    border-radius: 0 0 20px 20px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 4px 15px rgba(255, 107, 0, 0.3);
    position: relative;
}
.logo-esquina {
    position: absolute; top: 15px; left: 20px; width: 80px;
    border-radius: 50%; border: 3px solid white;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
}
.header-frase-peque { color: white !important; font-weight: 700; font-size: 1.2rem; margin: 0; }
.header-frase-grande { color: white !important; font-weight: 900; font-size: 3rem; line-height: 1.1; margin: 0; }

/* SIDEBAR */
[data-testid="stSidebar"] { background-color: white; border-right: 1px solid #ddd; }
.sidebar-header {
    background: linear-gradient(45deg, var(--color-naranja), var(--color-rojo));
    padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.sidebar-header h1 { color: white !important; font-size: 1.8rem; margin: 0; text-transform: uppercase; }

/* TABS */
.stTabs [data-baseweb="tab-list"] { background-color: white; padding: 10px; border-radius: 15px; gap: 10px; }
.stTabs [data-baseweb="tab"] {
    background-color: white; color: var(--color-naranja) !important;
    border: 2px solid var(--color-naranja); border-radius: 10px; font-weight: 700; padding: 0 20px; height: 50px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(45deg, var(--color-naranja), var(--color-rojo)) !important;
    color: white !important; border: none;
}

/* BOTONES */
.stButton>button {
    color: white !important;
    background: linear-gradient(45deg, var(--color-naranja), var(--color-rojo));
    border-radius: 25px; border: none; width: 100%; padding: 0.7rem; font-weight: 900;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.1s;
}
.stButton>button:active { transform: scale(0.95); }

/* NOTIFICACIONES */
div[data-baseweb="toast"] {
    background-color: var(--color-naranja) !important; color: white !important;
    font-weight: bold; border: 2px solid white;
}

/* INPUTS */
.stTextInput input, .stTextArea textarea, div[data-baseweb="select"] > div {
    border: 2px solid var(--color-naranja) !important; background-color: white !important;
    color: black !important; border-radius: 10px;
}
label { color: var(--color-naranja) !important; font-weight: 700 !important; }

/* TARJETAS */
[data-testid="column"] { 
    background: white; padding: 15px; border-radius: 15px; 
    border-bottom: 4px solid var(--color-naranja); margin-bottom: 10px; 
}
.precio-tag { color: var(--color-verde) !important; font-weight: 900; font-size: 1.5rem; }
.nombre-prod { font-size: 1.2rem; font-weight: 800; }

</style>
""", unsafe_allow_html=True)



