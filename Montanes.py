import streamlit as st
import urllib.parse  # Necesario para el enlace de WhatsApp

# Configuración de la página
st.set_page_config(page_title="EL TACO LOCO", page_icon="🌮", layout="wide")

# --- ESTILO CORREGIDO (LETRAS NEGRAS FORZADAS) ---
st.markdown("""
    <style>
    /* 1. Fondo Blanco Absoluto */
    .stApp { 
        background-color: #ffffff; 
    }
    
    /* 2. FORZAR TEXTO NEGRO (Para que no se ponga blanco por el tema oscuro) */
    h1, h2, h3, h4, h5, h6, p, span, div, label, .stMarkdown {
        color: #000000 !important;
    }
    
    /* 3. Excepción: Los botones deben tener letra blanca */
    .stButton>button {
        color: white !important;
        background-color: #d62828;
        border-radius: 8px;
        border: none;
        width: 100%;
        padding: 0.6rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #b91d1d;
        color: white !important;
    }

    /* 4. Estilos de Precios y Títulos */
    .precio-tag {
        color: #1a1a1a !important;
        font-weight: 800;
        font-size: 26px;
        margin-top: 5px;
    }
    .nombre-taco { 
        font-size: 24px; 
        font-weight: 700; 
        color: #000000 !important; 
    }
    .desc-taco { 
        color: #333333 !important; 
        font-size: 15px; 
    }
    
    /* 5. Barra Lateral Clara */
    [data-testid="stSidebar"] { 
        background-color: #f4f4f4; 
        border-right: 1px solid #ddd;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] p {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
col_logo_1, col_logo_2, col_logo_3 = st.columns([1, 1, 1])
with col_logo_2:
    try:
        # Asegúrate de que tu imagen sea .png o .jpg según corresponda
        st.image("imagenes/logo.png", use_container_width=True)
    except:
        st.warning("⚠️ Logo no encontrado")

st.markdown("<h1 style='text-align: center; color: black;'>EL TACO LOCO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #d62828; font-weight: bold;'>Taqueria “El Taco Loco” te ofrece un sazón inigualable y un servicio excelente</p>", unsafe_allow_html=True)
st.write("---")

# --- BARRA LATERAL (CARRITO) ---
with st.sidebar:
    st.title("🛒 Tu Carrito")
    
    if 'carrito' not in st.session_state:
        st.session_state.carrito = {}

    if not st.session_state.carrito:
        st.info("Aún no has agregado tacos.")
    else:
        # --- LÓGICA DEL CARRITO VISIBLE Y WHATSAPP ---
        total_venta = 0
        texto_pedido = "Hola Taco Loco 🌮, quiero hacer un pedido:\n\n"
        
        # Recorremos el carrito
        for item, cant in list(st.session_state.carrito.items()):
            # Precio fijo de $14
            subtotal = cant * 14 
            total_venta += subtotal
            
            # 1. VISUALIZAR EN LA LISTA (Esto faltaba)
            st.markdown(f"<span style='color:black'>**{cant}x** {item} (${subtotal})</span>", unsafe_allow_html=True)
            
            # 2. AGREGAR AL MENSAJE DE WHATSAPP
            texto_pedido += f"• {cant}x {item} (${subtotal})\n"
        
        texto_pedido += f"\n*Total a pagar: ${total_venta} MXN*"
        
        st.divider()
        st.markdown(f"<h3 style='color:black'>Total: ${total_venta} MXN</h3>", unsafe_allow_html=True)
        
        # --- BOTÓN DE WHATSAPP ---
        mensaje_codificado = urllib.parse.quote(texto_pedido)
        # ¡OJO! Cambia este número por el tuyo real: 52 + lada + numero
        numero_whatsapp = "9681171392" 
        link_whatsapp = f"https://wa.me/{numero_whatsapp}?text={mensaje_codificado}"
        
        st.link_button("📲 Enviar Pedido por WhatsApp", link_whatsapp, type="primary")
        
        # Botón para limpiar carrito (opcional)
        if st.button("🗑️ Vaciar Carrito"):
            st.session_state.carrito = {}
            st.rerun() # Recarga la página para limpiar

    st.write("---")
    st.header("🏢 Empresa")
    menu_info = st.radio("Info:", ["Historia", "Misión", "Reseña"])
    
    if menu_info == "Historia":
        st.write("Somos EL TACO LOCO, una taqueria orgullosamente originaria de Ocozocoautla, Chiapas. Desde 2005 hemos servido con pasión nuestros tradicionales tacos de res, puerco, tripa, manteniendo el sabor que nos distingue.")
    elif menu_info == "Misión":
        st.write("**Misión:** Ofrecer a cada cliente una experiencia autentica y deliciosa.")
    elif menu_info == "Reseña":
        st.text_input("Nombre")
        st.text_area("Comentario")
        if st.button("Enviar"):
            st.toast("¡Gracias!")

# --- CATÁLOGO DE PRODUCTOS ---
st.subheader("🌮 Menú Interactivo")

tacos = {
    "Taco de Res": {"precio": 14, "img": "imagenes/taco 1.jpg", "desc": "Suave bistec de res."},
    "Taco de Puerco": {"precio": 14, "img": "imagenes/taco 2.jpg", "desc": "Deliciosa carne de cerdo."},
    "Taco de Tripa": {"precio": 14, "img": "imagenes/taco 3.jpg", "desc": "Tripa de Res dorada lentamente hasta quedar crujiente."},
    "Taco de Suadero": {"precio": 14, "img": "imagenes/taco 4.jpg", "desc": "Suadero cocido lentamente en su jugo."}
}

cols = st.columns(2)

for i, (nombre, info) in enumerate(tacos.items()):
    with cols[i % 2]:
        st.image(info["img"], use_container_width=True)
        st.markdown(f"<div class='nombre-taco'>{nombre}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='desc-taco'>{info['desc']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='precio-tag'>${info['precio']} MXN</div>", unsafe_allow_html=True)
        
        # AQUÍ ESTÁ EL CAMBIO DEL BOTÓN CON CARRITO
        if st.button(f"🛒 Agregar al Carrito", key=f"btn_{nombre}"):
            st.session_state.carrito[nombre] = st.session_state.carrito.get(nombre, 0) + 1
            st.toast(f"✅ {nombre} añadido")
        st.write("")