import streamlit as st
import urllib.parse
import pandas as pd
import base64 
import requests  # <--- NUEVA LIBRERÍA PARA HABLAR CON GOOGLE

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="EL TACO LOCO", page_icon="🌮", layout="wide")

# --- 2. LÓGICA DEL CARRITO ---
if 'carrito' not in st.session_state:
    st.session_state.carrito = {}

def agregar_al_carrito(producto, tipo):
    if producto in st.session_state.carrito:
        st.session_state.carrito[producto] += 1
    else:
        st.session_state.carrito[producto] = 1
    
    icono = "🔥" if tipo == "taco" else "🧊"
    st.toast(f"¡{producto} agregado!", icon=icono)

def obtener_total_items():
    return sum(st.session_state.carrito.values())

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
        --color-crema: #FFF8E1;
        --color-texto: #212121;
    }

    header { visibility: hidden !important; }
    .stAppDeployButton, [data-testid="stToolbar"], [data-testid="stDecoration"], footer { display: none !important; }
    
    [data-testid="stAppViewContainer"], .stApp { 
        background-color: var(--color-crema) !important; 
        font-family: 'Poppins', sans-serif;
    }
    .stApp { margin-top: -50px; }
    
    h1, h2, h3, h4, p, div, span, label, li { color: var(--color-texto) !important; }

    /* ESTILO MODAL */
    div[role="dialog"] {
        background: linear-gradient(135deg, var(--color-naranja), var(--color-rojo)) !important;
        border: 2px solid white;
    }
    div[role="dialog"] h1, div[role="dialog"] h2, div[role="dialog"] h3, 
    div[role="dialog"] p, div[role="dialog"] span, div[role="dialog"] label {
        color: white !important;
    }
    
    /* INPUTS */
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

    /* TOASTS */
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
    .logo-esquina {
        position: absolute; top: 15px; left: 20px; width: 80px;
        border-radius: 50%; border: 3px solid white;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    .header-frase-peque { color: white !important; font-weight: 700; font-size: 1.2rem; margin: 0; }
    .header-frase-grande { color: white !important; font-weight: 900; font-size: 3rem; line-height: 1.1; margin: 0; }

    /* BOTONES */
    .stButton>button {
        background: linear-gradient(45deg, var(--color-naranja), var(--color-rojo)) !important;
        color: white !important;
        border: none;
        border-radius: 20px;
        font-weight: bold;
        transition: transform 0.1s;
    }
    .stButton>button:active { transform: scale(0.95); }
    div[data-testid="column"] button[kind="primary"] {
        background: white !important; color: var(--color-rojo) !important; border: 2px solid var(--color-rojo) !important;
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
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATOS ---
menu_tacos = {
    "Taco de Res": {"precio": 14, "img": "imagenes/taco 1.jpg", "desc": "Suave bistec de res."},
    "Taco de Puerco": {"precio": 14, "img": "imagenes/taco 2.jpg", "desc": "Adobado especial."},
    "Taco de Tripa": {"precio": 14, "img": "imagenes/taco 3.jpg", "desc": "Doradita y crujiente."},
    "Taco de Suadero": {"precio": 14, "img": "imagenes/taco 4.jpg", "desc": "Cocido en su jugo."}
}
menu_bebidas = {
    "Agua de Horchata": {"precio": 20, "img": "imagenes/horchata.png", "desc": "Arroz y canela."},
    "Agua de Jamaica": {"precio": 20, "img": "imagenes/jamaica.png", "desc": "Natural y fresca."},
    "Senzao": {"precio": 25, "img": "imagenes/senzao.png", "desc": "Tradicional de Coita."}
}
menu_completo = {**menu_tacos, **menu_bebidas}

# --- 5. VENTANA EMERGENTE (MODAL CON BASE DE DATOS) ---
@st.dialog("🛒 TU PEDIDO")
def mostrar_carrito_modal():
    
    # Manejamos el estado del formulario para que no se borre al guardar
    if 'pedido_guardado' not in st.session_state:
        st.session_state.pedido_guardado = False

    if not st.session_state.carrito:
        st.info("Tu carrito está vacío.")
    else:
        total_venta = 0
        texto_pedido = ""
        texto_para_excel = "" # Guardamos el pedido resumido para tu base de datos
        
        for item, cant in st.session_state.carrito.items():
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
        
        # Si el pedido aún no se ha guardado en la base de datos, mostramos el formulario
        if not st.session_state.pedido_guardado:
            st.markdown("#### 📍 Datos de Envío")
            nombre = st.text_input("Nombre:")
            direccion = st.text_area("Dirección exacta:")
            ref = st.text_input("Referencia de la casa:")
            pago = st.selectbox("Forma de Pago:", ["Efectivo 💵", "Transferencia 📱"])
            
            msg_final = f"Hola Taco Loco 🌮, soy *{nombre}*.\n\n*MI PEDIDO:*\n{texto_pedido}\n💰 *Total: ${total_venta}*\n📍 *Dir:* {direccion}\n🏠 *Ref:* {ref}\n💸 *Pago:* {pago}"
            
            if st.button("📝 CONFIRMAR PEDIDO", use_container_width=True):
                if nombre and direccion:
                  # --- AQUÍ OCURRE LA MAGIA DE GUARDAR EN EXCEL ---
                    url_google = "https://script.google.com/macros/s/AKfycbyHzbARjCcog41iCwBvCvA4aburgAlGGHSA5EEQuGP64CQe36-j-piizwITeysVVA5u/exec" 
                    datos_excel = {
                        "cliente": nombre,
                        "direccion": f"{direccion} ({ref})",
                        "pedido": texto_para_excel,
                        "total": total_venta,
                        "pago": pago
                    }
                    try:
                        respuesta = requests.post(url_google, json=datos_excel)
                        
                        # Ahora Python leerá la respuesta real de Google
                        if "Error" in respuesta.text:
                            st.error(f"Google rechazó el dato: {respuesta.text}")
                        else:
                            st.toast("✅ ¡Guardado en el Excel!")
                            
                        # Pasamos a la fase del WhatsApp
                        st.session_state.mensaje_whatsapp = msg_final
                        st.session_state.pedido_guardado = True
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Falló la conexión: {e}")
                    
                    # Guardamos el mensaje de whatsapp en memoria y pasamos a la fase 2
                    st.session_state.mensaje_whatsapp = msg_final
                    st.session_state.pedido_guardado = True
                    st.rerun()
                else:
                    st.warning("Falta tu nombre o dirección.")
            
            if st.button("🗑️ Vaciar Carrito"):
                st.session_state.carrito = {}
                st.rerun()
        
        # FASE 2: EL PEDIDO YA ESTÁ EN LA BASE DE DATOS, AHORA MANDAMOS EL WHATSAPP
        else:
            st.success("✅ ¡Tu pedido ya fue registrado en nuestro sistema!")
            st.markdown("Solo falta un paso: **Envíanos el WhatsApp para preparar tus tacos.**")
            
            msg_encoded = urllib.parse.quote(st.session_state.mensaje_whatsapp)
            whatsapp_url = f"https://wa.me/529681171392?text={msg_encoded}"
            
            st.link_button("📲 ENVIAR POR WHATSAPP AHORA", whatsapp_url, type="primary", use_container_width=True)
            
            if st.button("⬅️ Volver a empezar y Vaciar Carrito", use_container_width=True):
                st.session_state.pedido_guardado = False
                st.session_state.carrito = {}
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
        mostrar_carrito_modal()

tabs = st.tabs(["🌮 TACOS", "🥤 BEBIDAS", "📍 UBICACIÓN"])

# TACOS
with tabs[0]:
    cols = st.columns(2)
    for i, (nombre, info) in enumerate(menu_tacos.items()):
        with cols[i % 2]:
            try: st.image(info["img"], use_container_width=True)
            except: st.error("Sin imagen")
            
            st.markdown(f"<div class='nombre-prod'>{nombre}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='desc-prod'>{info['desc']}</div>", unsafe_allow_html=True)
            st.markdown(f"<span class='precio-tag'>${info['precio']}</span>", unsafe_allow_html=True)
            
            cantidad_actual = st.session_state.carrito.get(nombre, 0)
            texto_boton = f"AGREGAR ({cantidad_actual}) 🛒" if cantidad_actual > 0 else "AGREGAR + 🛒"
            st.button(texto_boton, key=f"t_{i}", on_click=agregar_al_carrito, args=(nombre, "taco"))

# BEBIDAS
with tabs[1]:
    cols_b = st.columns(3)
    for i, (nombre, info) in enumerate(menu_bebidas.items()):
        with cols_b[i % 3]:
            try: st.image(info["img"], use_container_width=True)
            except: st.info("Sin imagen")
            
            st.markdown(f"<div class='nombre-prod'>{nombre}</div>", unsafe_allow_html=True)
            st.markdown(f"<span class='precio-tag'>${info['precio']}</span>", unsafe_allow_html=True)
            
            cantidad_actual = st.session_state.carrito.get(nombre, 0)
            texto_boton = f"AGREGAR ({cantidad_actual}) 🛒" if cantidad_actual > 0 else "AGREGAR + 🛒"
            st.button(texto_boton, key=f"b_{i}", on_click=agregar_al_carrito, args=(nombre, "bebida"))

# UBICACIÓN
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
        st.info("Guarda una foto llamada 'local.jpg' en la carpeta 'imagenes' para que aparezca aquí.")





