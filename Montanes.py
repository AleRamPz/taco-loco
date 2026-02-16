import streamlit as st
import urllib.parse
import pandas as pd
import base64 

# --- 1. CONFIGURACIÓN: FORZAR QUE EL MENÚ APAREZCA ABIERTO ---
st.set_page_config(
    page_title="EL TACO LOCO", 
    page_icon="🌮", 
    layout="wide", 
    initial_sidebar_state="expanded" 
)

# --- 2. FUNCIONES LÓGICAS ---
def agregar_al_carrito(producto, tipo):
    if 'carrito' not in st.session_state:
        st.session_state.carrito = {}
    
    if producto in st.session_state.carrito:
        st.session_state.carrito[producto] += 1
    else:
        st.session_state.carrito[producto] = 1
        
    icono = "🔥" if tipo == "taco" else "🧊"
    st.toast(f"¡{producto} agregado!", icon=icono)

def get_img_as_base64(file):
    try:
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

img_path = "imagenes/logo.png" 
logo_base64 = get_img_as_base64(img_path)

# --- 3. ESTILOS CSS ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700;900&display=swap" rel="stylesheet">

    <style>
    /* --- ARREGLO DEL MENÚ --- */
    
    /* 1. El Header de Streamlit debe estar ENCIMA de todo (z-index alto) */
    header { 
        background-color: transparent !important;
        z-index: 1000000 !important;
        height: 60px !important;
    }
    
    /* 2. Ocultamos SOLO los botones internos del toolbar, NO el toolbar completo */
    [data-testid="stToolbarActions"] { display: none !important; }
    [data-testid="stDecoration"] { display: none !important; }
    footer { display: none !important; }
    .stAppDeployButton { display: none !important; }
    /* Ocultar íconos de Github y deploy por si usan otras clases */
    [data-testid="stToolbar"] button { display: none !important; }

    /* 3. ✅ FIX REAL: El botón del menú lateral se muestra explícitamente */
    [data-testid="collapsedControl"] { 
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        color: white !important;
        z-index: 1000001 !important;
    }
    [data-testid="collapsedControl"] button {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    /* --- ESTILOS GENERALES --- */
    :root {
        --color-naranja: #FF6B00;
        --color-rojo: #D32F2F;
        --color-verde: #2E7D32;
        --color-crema: #FFF8E1;
    }

    .stApp { 
        background-color: var(--color-crema); 
        font-family: 'Poppins', sans-serif;
        margin-top: -60px; 
    }
    h1, h2, h3, h4, p, div, span, label, li { color: #212121 !important; }

    /* ENCABEZADO */
    .header-container {
        background: linear-gradient(135deg, var(--color-naranja), var(--color-rojo));
        padding: 2rem;
        padding-top: 3rem;
        border-radius: 0 0 20px 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(255, 107, 0, 0.3);
        position: relative;
        z-index: 1;
    }
    .logo-esquina {
        position: absolute; top: 15px; left: 60px;
        width: 80px;
        border-radius: 50%; border: 3px solid white;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    .header-frase-peque { color: white !important; font-weight: 700; font-size: 1.2rem; margin: 0; }
    .header-frase-grande { color: white !important; font-weight: 900; font-size: 3rem; line-height: 1.1; margin: 0; }

    /* SIDEBAR */
    [data-testid="stSidebar"] { 
        background-color: white; 
        border-right: 1px solid #ddd;
        z-index: 1000002 !important;
    }
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
    [data-testid="column"] { background: white; padding: 15px; border-radius: 15px; border-bottom: 4px solid var(--color-naranja); margin-bottom: 10px; }
    .precio-tag { color: var(--color-verde) !important; font-weight: 900; font-size: 1.5rem; }
    .nombre-prod { font-size: 1.2rem; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATOS DEL MENÚ ---
menu_tacos = {
    "Taco de Res": {"precio": 14, "img": "imagenes/taco 1.jpg", "desc": "Suave bistec de res."},
    "Taco de Puerco": {"precio": 14, "img": "imagenes/taco 2.jpg", "desc": "Adobado especial."},
    "Taco de Tripa": {"precio": 14, "img": "imagenes/taco 3.jpg", "desc": "Doradita y crujiente."},
    "Taco de Suadero": {"precio": 14, "img": "imagenes/taco 4.jpg", "desc": "Cocido en su jugo."}
}
menu_bebidas = {
    "Agua de Horchata": {"precio": 20, "img": "imagenes/horchata.png", "desc": "Arroz y canela."},
    "Agua de Jamaica": {"precio": 20, "img": "imagenes/jamaica.png", "desc": "Natural y fresca."},
    "Zensao": {"precio": 25, "img": "imagenes/senzao.png", "desc": "Tradicional de Coita."}
}
menu_completo = {**menu_tacos, **menu_bebidas}

# --- 5. INTERFAZ: ENCABEZADO ---
logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="logo-esquina">' if logo_base64 else ''
st.markdown(f"""
    <div class="header-container">
        {logo_html}
        <p class="header-frase-peque">¿CON HAMBRE?</p>
        <p class="header-frase-grande">REVISA NUESTRO MENÚ</p>
    </div>
    """, unsafe_allow_html=True)

# --- 6. INTERFAZ: BARRA LATERAL (CARRITO) ---
with st.sidebar:
    st.markdown("""<div class="sidebar-header"><h1>🛒 TU PEDIDO</h1></div>""", unsafe_allow_html=True)
    
    st.markdown("### 📍 Datos de Envío")
    cliente_nombre = st.text_input("Tu Nombre:")
    cliente_direccion = st.text_area("Dirección exacta:")
    cliente_ref = st.text_input("Referencia:")
    metodo_pago = st.selectbox("Forma de Pago", ["Efectivo 💵", "Transferencia 📱"])
    
    st.divider()
    
    if 'carrito' not in st.session_state:
        st.session_state.carrito = {}

    if not st.session_state.carrito:
        st.info("Carrito vacío.")
    else:
        total_venta = 0
        texto_pedido = f"Hola Taco Loco 🌮, soy *{cliente_nombre}*.\n\n*MI PEDIDO:*\n"
        for item, cant in st.session_state.carrito.items():
            precio_u = menu_completo[item]["precio"]
            subtotal = cant * precio_u
            total_venta += subtotal
            st.markdown(f"**{cant}x** {item} (${subtotal})")
            texto_pedido += f"• {cant}x {item} (${subtotal})\n"
        
        st.divider()
        st.markdown(f"<h3 style='color: var(--color-rojo) !important;'>Total: ${total_venta} MXN</h3>", unsafe_allow_html=True)
        
        texto_pedido += f"\n💰 Total a pagar: ${total_venta}"
        texto_pedido += f"\n📍 *Dirección:* {cliente_direccion}"
        texto_pedido += f"\n🏠 *Ref:* {cliente_ref}"
        texto_pedido += f"\n💸 *Pago con:* {metodo_pago}"

        if cliente_direccion and cliente_nombre:
            mensaje_codificado = urllib.parse.quote(texto_pedido)
            numero_whatsapp = "9681171392"
            link_whatsapp = f"https://wa.me/{numero_whatsapp}?text={mensaje_codificado}"
            st.link_button("📲 Enviar Pedido", link_whatsapp, type="primary")
        else:
            st.warning("Completa tus datos.")
            
        if st.button("🗑️ Borrar Carrito"):
            st.session_state.carrito = {}
            st.rerun()

# --- 7. INTERFAZ: PRODUCTOS ---
tabs = st.tabs(["🌮 TACOS", "🥤 BEBIDAS", "📍 UBICACIÓN"])

with tabs[0]:
    st.subheader("🔥 Nuestros Tacos")
    cols = st.columns(2)
    for i, (nombre, info) in enumerate(menu_tacos.items()):
        with cols[i % 2]:
            try: st.image(info["img"], use_container_width=True)
            except: st.error("Falta imagen")
            st.markdown(f"<div class='nombre-prod'>{nombre}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='desc-prod'>{info['desc']}</div>", unsafe_allow_html=True)
            st.markdown(f"<span class='precio-tag'>${info['precio']}</span>", unsafe_allow_html=True)
            
            st.button(f"AGREGAR 🛒", key=f"taco_{nombre}", on_click=agregar_al_carrito, args=(nombre, "taco"))

with tabs[1]:
    st.subheader("🧊 Bebidas Frías")
    cols_b = st.columns(3)
    for i, (nombre, info) in enumerate(menu_bebidas.items()):
        with cols_b[i % 3]:
            try: st.image(info["img"], use_container_width=True)
            except: st.info("Falta imagen")
            st.markdown(f"<div class='nombre-prod'>{nombre}</div>", unsafe_allow_html=True)
            st.markdown(f"<span class='precio-tag'>${info['precio']}</span>", unsafe_allow_html=True)
            
            st.button(f"AGREGAR 🥤", key=f"bebida_{nombre}", on_click=agregar_al_carrito, args=(nombre, "bebida"))

with tabs[2]:
    st.subheader("🗺️ Encuéntranos")
    latitud_coita = 16.753554732500405
    longitud_coita = -93.37373160552643
    st.map(pd.DataFrame({'lat': [latitud_coita], 'lon': [longitud_coita]}), zoom=15)
    st.markdown("""
        <div style='background: white; padding: 20px; border-radius: 15px; border-left: 5px solid #FF6B00;'>
            <h4>🕒 Horario</h4>
            <p>Lunes a Domingo<br><strong>6:00 PM - 12:00 AM</strong></p>
        </div>
        """, unsafe_allow_html=True)



