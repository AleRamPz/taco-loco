import streamlit as st
import urllib.parse
import pandas as pd
import base64 
import requests 
import threading 

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="EL TACO LOCO", page_icon="🌮", layout="wide")

# --- 2. LÓGICA DEL CARRITO Y VELOCIDAD ---
if 'carrito' not in st.session_state:
    st.session_state.carrito = {}

if 'fase_pedido' not in st.session_state:
    st.session_state.fase_pedido = 1

def agregar_al_carrito(producto, tipo):
    if producto in st.session_state.carrito:
        st.session_state.carrito[producto] += 1
    else:
        st.session_state.carrito[producto] = 1
    
    icono = "🔥" if tipo == "taco" else "🧊"
    st.toast(f"¡1 {producto} agregado!", icon=icono)

def quitar_del_carrito(producto):
    if producto in st.session_state.carrito:
        st.session_state.carrito[producto] -= 1
        if st.session_state.carrito[producto] <= 0:
            del st.session_state.carrito[producto] 
        st.toast(f"¡1 {producto} quitado!", icon="➖")

def obtener_total_items():
    return sum(st.session_state.carrito.values())

def enviar_datos_excel(url, datos):
    try:
        requests.post(url, json=datos, timeout=5)
    except:
        pass

@st.cache_data
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
    :root {
        --color-naranja: #FF6B00;
        --color-rojo: #D32F2F;
        --color-crema: #F4F6F8; /* BLANCO/GRIS QUE RELAJA LA VISTA */
        --color-texto: #212121;
    }

    /* OCULTAR TODO EL RASTRO DE STREAMLIT (Marca de agua, footer, botones) */
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; display: none !important; }
    .stAppDeployButton { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stDecoration"] { display: none !important; }
    [data-testid="stStatusWidget"] { display: none !important; }
    #MainMenu { visibility: hidden !important; }
    
    /* HACK PARA OCULTAR LA PESTAÑA FLOTANTE DE LA ESQUINA INFERIOR */
    a[href^="https://streamlit.io/cloud"] { display: none !important; }
    div[class^="viewerBadge"] { display: none !important; }
    div[class^="stDeployButton"] { display: none !important; }
    
    /* EVITAR PARPADEO GRIS AL RECARGAR */
    [data-testid="stAppViewBlockContainer"], [data-testid="stVerticalBlock"] { opacity: 1 !important; }
    
    [data-testid="stAppViewContainer"], .stApp { 
        background-color: var(--color-crema) !important; 
        font-family: 'Poppins', sans-serif;
    }
    .stApp { margin-top: -50px; }
    
    h1, h2, h3, h4, p, div, span, label, li { color: var(--color-texto) !important; }

    /* ESTILO MODAL NARANJA */
    div[role="dialog"] {
        background: linear-gradient(135deg, var(--color-naranja), var(--color-rojo)) !important;
        border: 2px solid white;
    }
    div[role="dialog"] h1, div[role="dialog"] h2, div[role="dialog"] h3, 
    div[role="dialog"] p, div[role="dialog"] span, div[role="dialog"] label {
        color: white !important;
    }
    
    /* INPUTS (CAJAS DE TEXTO) */
    div[role="dialog"] input, div[role="dialog"] textarea {
        background-color: white !important;
        color: #212121 !important;
        border: 2px solid var(--color-naranja) !important;
        border-radius: 10px;
    }
    div[role="dialog"] input::placeholder, div[role="dialog"] textarea::placeholder { color: #757575 !important; }

    div[role="dialog"] div[data-baseweb="select"] > div {
        background-color: white !important;
        color: #212121 !important;
        border: 2px solid var(--color-naranja) !important;
    }
    div[role="dialog"] div[data-baseweb="select"] span { color: #212121 !important; font-weight: bold; }
    div[role="dialog"] div[data-baseweb="select"] svg { fill: var(--color-naranja) !important; }
    div[data-baseweb="popover"] div { background-color: white !important; color: #FF6B00 !important; font-weight: bold; }

    /* TOASTS (NOTIFICACIONES FLOTANTES NARANJAS CON TEXTO BLANCO) */
    div[data-baseweb="toast"] {
        background-color: var(--color-naranja) !important;
        border: 2px solid white;
        border-radius: 10px;
    }
    div[data-baseweb="toast"] div { color: white !important; font-weight: bold; }

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
    /* LOGO MÁS GRANDE */
    .logo-esquina {
        display: block;
        margin: 0 auto 15px auto;
        width: 100px;
        border-radius: 50%; border: 3px solid white;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    .header-frase-peque { color: white !important; font-weight: 700; font-size: 1.2rem; margin: 0; }
    .header-frase-grande { color: white !important; font-weight: 900; font-size: 3rem; line-height: 1.1; margin: 0; }

    /* BOTONES CON EFECTO DE ILUMINACIÓN AL PASAR EL MOUSE */
    .stButton>button, [data-testid="stFormSubmitButton"]>button {
        background: linear-gradient(45deg, var(--color-naranja), var(--color-rojo)) !important;
        color: white !important;
        border: none;
        border-radius: 20px;
        font-weight: bold;
        transition: all 0.2s ease; 
    }
    .stButton>button:hover, [data-testid="stFormSubmitButton"]>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(255, 107, 0, 0.4); 
    }
    .stButton>button:active, [data-testid="stFormSubmitButton"]>button:active { transform: scale(0.95); }
    
    div[data-testid="column"] button[kind="primary"] {
        background: white !important; color: var(--color-rojo) !important; border: 2px solid var(--color-rojo) !important;
    }
    div[data-testid="column"] button[kind="primary"]:hover {
        box-shadow: 0 8px 15px rgba(211, 47, 47, 0.3); 
        transform: translateY(-2px);
    }

    /* TABS Y PRODUCTOS */
    .stTabs [data-baseweb="tab-list"] { background-color: white; padding: 5px; border-radius: 15px; }
    .stTabs [data-baseweb="tab"] { color: var(--color-naranja) !important; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: var(--color-naranja) !important; color: white !important; border-radius: 10px; }
    [data-testid="column"] { background: white; padding: 15px; border-radius: 15px; border-bottom: 4px solid var(--color-naranja); margin-bottom: 10px; }
    .precio-tag { color: var(--color-verde) !important; font-weight: 900; font-size: 1.5rem; }
    .nombre-prod { font-size: 1.2rem; font-weight: 800; color: #212121 !important; }
    .ubicacion-box {
        background-color: white; padding: 20px; border-radius: 15px; 
        border-left: 5px solid var(--color-naranja); margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* EFECTO ZOOM EN IMÁGENES AL PASAR EL MOUSE */
    [data-testid="stImage"] img { transition: transform 0.3s ease; border-radius: 10px; }
    [data-testid="stImage"] img:hover { transform: scale(1.05); }
    
    .contador-item { text-align: center; font-weight: 900; font-size: 1.3rem; color: var(--color-rojo); margin-top: 5px; }

    /* FOOTER (PIE DE PÁGINA BLINDADO PARA TEXTO BLANCO) */
    .footer-container {
        background-color: #1A1A1A !important;
        padding: 2rem;
        text-align: center;
        border-radius: 20px 20px 0 0;
        margin-top: 4rem;
        box-shadow: 0 -4px 15px rgba(0,0,0,0.2);
    }
    .footer-container, .footer-container h3, .footer-container p, .footer-container span, .footer-container div {
        color: #FFFFFF !important; 
    }
    .footer-container a { color: var(--color-naranja) !important; text-decoration: none; font-weight: bold; margin: 0 10px; font-size: 1.2rem; }
    .footer-container a:hover { color: var(--color-crema) !important; }
    .texto-creditos { color: #888888 !important; font-size: 0.8rem !important; margin-top: 30px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. BASE DE DATOS DEL MENÚ (GOOGLE SHEETS) ---
@st.cache_data(ttl=10) 
def cargar_menu(url_csv):
    try:
        df = pd.read_csv(url_csv)
        tacos = {}
        bebidas = {}
        for _, row in df.iterrows():
            categoria = str(row["Categoria"]).strip().lower()
            nombre = str(row["Nombre"]).strip()
            item = {
                "precio": float(row["Precio"]),
                "img": str(row["Imagen"]).strip(),
                "desc": str(row["Descripcion"]).strip() if pd.notna(row["Descripcion"]) else ""
            }
            if categoria == "taco":
                tacos[nombre] = item
            elif categoria == "bebida":
                bebidas[nombre] = item
        return tacos, bebidas
    except Exception as e:
        return {}, {}

URL_CSV_MENU = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQTIoRwg327pe_n_h-paHJ2OMmufADQgIfeiTvXBWTzfnDyJn21dDhhSYq97WZIVb8ZzQfwaHlGGmvd/pub?gid=357751603&single=true&output=csv" 

menu_tacos, menu_bebidas = cargar_menu(URL_CSV_MENU)
menu_completo = {**menu_tacos, **menu_bebidas}

if not menu_tacos and not menu_bebidas:
    st.error("⚠️ No se pudo cargar el menú. Revisa tu Excel.")

# --- 5. VENTANA EMERGENTE (MODAL PERFECTO CON FORMULARIO INVISIBLE) ---
@st.dialog("🛒 TU PEDIDO")
def mostrar_carrito_modal():
    
    if st.session_state.fase_pedido == 1:
        if not st.session_state.carrito:
            st.info("Tu carrito está vacío.")
            return
            
        vista_fase1 = st.empty()
        
        with vista_fase1.container():
            total_venta = 0
            texto_pedido = ""
            texto_para_excel = ""
            
            for item, cant in st.session_state.carrito.items():
                if item not in menu_completo: continue 
                
                precio_u = menu_completo[item]["precio"]
                subtotal = cant * precio_u
                total_venta += subtotal
                
                c1, c2, c3 = st.columns([3, 1, 1])
                c1.markdown(f"**{item}**")
                c2.markdown(f"x{cant}")
                c3.markdown(f"${subtotal}")
                texto_pedido += f"• {cant}x {item} (${subtotal})\n"
                texto_para_excel += f"{cant}x {item}, "
            
            st.divider()
            st.markdown(f"<h3 style='text-align: right; color: white !important;'>Total: ${total_venta}</h3>", unsafe_allow_html=True)
            
            with st.form("form_pedido", border=False):
                st.markdown("#### 📍 Datos de Envío")
                nombre = st.text_input("Nombre:")
                direccion = st.text_area("Dirección exacta:")
                ref = st.text_input("Referencia de la casa:")
                notas = st.text_area("Instrucciones especiales (Opcional):", placeholder="Ej. Sin cebolla, salsas aparte...")
                pago = st.selectbox("Forma de Pago:", ["Efectivo 💵", "Transferencia 📱"])
                
                confirmar = st.form_submit_button("📝 CONFIRMAR PEDIDO", type="secondary", use_container_width=True)
            
            if st.button("🗑️ Vaciar Carrito", use_container_width=True):
                st.session_state.carrito = {}
                st.rerun()

        if confirmar:
            if nombre and direccion:
                msg_notas = f"\n📝 *Notas:* {notas}\n" if notas else "\n"
                msg_final = f"Hola Taco Loco 🌮, soy *{nombre}*.\n\n*MI PEDIDO:*\n{texto_pedido}{msg_notas}\n💰 *Total: ${total_venta}*\n📍 *Dir:* {direccion}\n🏠 *Ref:* {ref}\n💸 *Pago:* {pago}"

                url_google_guardar = "https://script.google.com/macros/s/AKfycbyHzbARjCcog41iCwBvCvA4aburgAlGGHSA5EEQuGP64CQe36-j-piizwITeysVVA5u/exec" 
                
                texto_excel_con_notas = texto_para_excel
                if notas:
                    texto_excel_con_notas += f" | NOTAS: {notas}"
                    
                datos_excel = {
                    "cliente": nombre,
                    "direccion": f"{direccion} ({ref})",
                    "pedido": texto_excel_con_notas,
                    "total": total_venta,
                    "pago": pago
                }
                
                threading.Thread(target=enviar_datos_excel, args=(url_google_guardar, datos_excel)).start()
                    
                msg_encoded = urllib.parse.quote(msg_final.encode('utf-8'))
                st.session_state.whatsapp_url = f"https://api.whatsapp.com/send?phone=529681171392&text={msg_encoded}"
                st.session_state.fase_pedido = 2
                
                vista_fase1.empty()
                
                st.markdown("""
                    <div style='background-color: rgba(255,255,255,0.2); padding: 20px; border-radius: 10px; border: 2px solid white; text-align: center; margin-bottom: 20px;'>
                        <h2>✅ ¡Casi listo!</h2>
                        <p style="font-size: 1.1rem;">Tu pedido ya está anotado. Toca el botón para enviarnos el mensaje y prepararlo rápido.</p>
                    </div>
                """, unsafe_allow_html=True)
                st.link_button("📲 ABRIR WHATSAPP AHORA", st.session_state.whatsapp_url, type="secondary", use_container_width=True)
                
                if st.button("✨ Terminar y limpiar carrito", use_container_width=True):
                    st.session_state.carrito = {}
                    st.session_state.fase_pedido = 1
                    st.rerun()
            else:
                st.error("⚠️ Completa tu nombre y dirección por favor.")

    elif st.session_state.fase_pedido == 2:
        st.markdown("""
            <div style='background-color: rgba(255,255,255,0.2); padding: 20px; border-radius: 10px; border: 2px solid white; text-align: center; margin-bottom: 20px;'>
                <h2>✅ ¡Casi listo!</h2>
                <p style="font-size: 1.1rem;">Tu pedido ya está anotado. Toca el botón para enviarnos el mensaje y prepararlo rápido.</p>
            </div>
        """, unsafe_allow_html=True)
        st.link_button("📲 ABRIR WHATSAPP AHORA", st.session_state.whatsapp_url, type="secondary", use_container_width=True)
        
        if st.button("✨ Terminar y limpiar carrito", use_container_width=True):
            st.session_state.carrito = {}
            st.session_state.fase_pedido = 1
            st.rerun()

# --- 6. INTERFAZ PRINCIPAL ---
logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="logo-esquina">' if logo_base64 else ''
st.markdown(f"""
    <div class="header-container">
        {logo_html}
        <p class="header-frase-peque">¿CON HAMBRE?</p>
        <p class="header-frase-grande">REVISA NUESTRO MENÚ</p>
    </div>
    """, unsafe_allow_html=True)

col_titulo, col_carrito = st.columns([7, 2])
with col_titulo:
    st.subheader("🔥 Menú del Día")

with col_carrito:
    total_items = obtener_total_items()
    label_btn = "🛒 Ver Carrito"
    tipo_btn = "secondary"
    
    if total_items > 0:
        label_btn = f"🛒 Ver Carrito ({total_items})"
        tipo_btn = "primary"
        
    if st.button(label_btn, type=tipo_btn, use_container_width=True):
        st.session_state.fase_pedido = 1 
        mostrar_carrito_modal()

tabs = st.tabs(["🌮 TACOS", "🥤 BEBIDAS", "📍 UBICACIÓN"])

with tabs[0]:
    if not menu_tacos:
        st.info("Aún no hay tacos en el menú. ¡Agrega algunos en tu Excel!")
    else:
        cols = st.columns(2)
        for i, (nombre, info) in enumerate(menu_tacos.items()):
            with cols[i % 2]:
                try: st.image(info["img"], use_container_width=True)
                except: st.error("Sin imagen")
                
                st.markdown(f"<div class='nombre-prod'>{nombre}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='desc-prod'>{info['desc']}</div>", unsafe_allow_html=True)
                st.markdown(f"<span class='precio-tag'>${int(info['precio'])}</span>", unsafe_allow_html=True)
                
                cantidad_actual = st.session_state.carrito.get(nombre, 0)
                if cantidad_actual > 0:
                    col_min, col_num, col_plus = st.columns([1, 1.2, 1])
                    with col_min: st.button("➖", key=f"min_t_{i}", on_click=quitar_del_carrito, args=(nombre,), use_container_width=True)
                    with col_num: st.markdown(f"<div class='contador-item'>{cantidad_actual} 🛒</div>", unsafe_allow_html=True)
                    with col_plus: st.button("➕", key=f"plus_t_{i}", on_click=agregar_al_carrito, args=(nombre, "taco"), use_container_width=True)
                else:
                    st.button("AGREGAR + 🛒", key=f"add_t_{i}", on_click=agregar_al_carrito, args=(nombre, "taco"), use_container_width=True)

with tabs[1]:
    if not menu_bebidas:
        st.info("Aún no hay bebidas en el menú. ¡Agrega algunas en tu Excel!")
    else:
        cols_b = st.columns(3)
        for i, (nombre, info) in enumerate(menu_bebidas.items()):
            with cols_b[i % 3]:
                try: st.image(info["img"], use_container_width=True)
                except: st.info("Sin imagen")
                
                st.markdown(f"<div class='nombre-prod'>{nombre}</div>", unsafe_allow_html=True)
                st.markdown(f"<span class='precio-tag'>${int(info['precio'])}</span>", unsafe_allow_html=True)
                
                cantidad_actual = st.session_state.carrito.get(nombre, 0)
                if cantidad_actual > 0:
                    col_min, col_num, col_plus = st.columns([1, 1.2, 1])
                    with col_min: st.button("➖", key=f"min_b_{i}", on_click=quitar_del_carrito, args=(nombre,), use_container_width=True)
                    with col_num: st.markdown(f"<div class='contador-item'>{cantidad_actual} 🥤</div>", unsafe_allow_html=True)
                    with col_plus: st.button("➕", key=f"plus_b_{i}", on_click=agregar_al_carrito, args=(nombre, "bebida"), use_container_width=True)
                else:
                    st.button("AGREGAR + 🛒", key=f"add_b_{i}", on_click=agregar_al_carrito, args=(nombre, "bebida"), use_container_width=True)

with tabs[2]:
    st.markdown("### 🗺️ Encuéntranos")
    mapa_html = """
    <iframe 
        src="https://www.google.com/maps?q=16.753554732500405,-93.37373160552643&hl=es&z=16&output=embed" 
        width="100%" height="350" 
        style="border:0; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);" 
        allowfullscreen="" loading="lazy">
    </iframe>
    """
    st.markdown(mapa_html, unsafe_allow_html=True)
    
    st.markdown("""
        <div class='ubicacion-box'>
            <h4 style='color: #FF6B00 !important; margin-top: 0;'>📍 Dirección</h4>
            <p><strong>El Taco Loco</strong><br>Ocozocoautla de Espinosa, Chiapas.</p>
            <h4 style='color: #FF6B00 !important; margin-top: 15px;'>🕒 Horario</h4>
            <p>Lunes a Domingo: <strong>6:00 PM - 12:00 AM</strong></p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### 📸 Conoce nuestro local:")
    try:
        st.image("imagenes/local.png", caption="¡Te esperamos con los mejores tacos!", use_container_width=True)
    except:
        st.info("Guarda una foto llamada 'local.png' en la carpeta 'imagenes' para que aparezca aquí.")

# --- 7. FOOTER CORREGIDO ---
st.markdown("""
    <div class='footer-container'>
        <h3 style="margin-bottom: 5px;">🌮 El Taco Loco</h3>
        <p style="margin-bottom: 20px;">Los mejores tacos de Coita, a un clic de distancia.</p>
        <div>
            <a href='#' target='_blank'>👍 Facebook</a>
            <a href='#' target='_blank'>📸 Instagram</a>
            <a href='#' target='_blank'>🎵 TikTok</a>
        </div>
        <p class="texto-creditos">Desarrollado por AleRamPz para El Taco Loco © 2026</p>
    </div>
""", unsafe_allow_html=True)











