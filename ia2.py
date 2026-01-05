import streamlit as st
import ollama

# --- DICCIONARIO DE MODELOS ---
INFO_MODELOS = {
    "Llama 3.1 (Oficial)": "llama3.1",
    "DeepSeek R1 (Razonamiento Puro)": "deepseek-r1:32b",
    "Gemma 2 (Equilibrio Premium)": "gemma2:27b",
    "Mistral Small (Lógica Pesada)": "mistral-small:latest",
    "Mistral NeMo (Optimizado NVIDIA)": "mistral-nemo",
    "Dolphin Llama 3 (Sin Censura)": "dolphin-llama3",
    "DeepSeek Coder (Técnico/Código)": "deepseek-coder-v2:lite",
    "LLaVA (Visión/Imagen)": "llava"
}

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Chat IA", page_icon="🤖", layout="centered")

# --- CSS PERSONALIZADO PARA FIJAR EL CHAT_INPUT AL FONDO SIEMPRE ---
st.markdown("""
<style>
    /* Contenedor principal ocupa toda la altura de la ventana */
    .main > div {
        padding-bottom: 0px !important;
        height: 100vh;
        display: flex;
        flex-direction: column;
    }

    /* El bloque que contiene los mensajes crece para ocupar el espacio disponible */
    section[data-testid="stSidebar"] + div > div:first-child {
        flex-grow: 1;
        display: flex;
        flex-direction: column;
    }

    /* El área del chat (donde van los mensajes) ocupa todo el espacio y permite scroll */
    [data-testid="stVerticalBlock"] > div:first-child {
        flex-grow: 1;
        overflow-y: auto;
    }

    /* Fijar el chat_input al fondo permanentemente */
    [data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 0;
        left: 0;
        right: 0;
        background: var(--default-background-color);
        z-index: 999;
        padding: 1rem;
        border-top: 1px solid var(--neutral-200);
    }

    /* Añadir padding inferior al contenedor de mensajes para que no quede tapado por el input */
    .block-container {
        padding-bottom: 100px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("Modelo de IA")
    modelo_opcion = st.selectbox(
        label="Selecciona el modelo",
        options=list(INFO_MODELOS.keys()),
        index=0,
        label_visibility="collapsed"
    )
    modelo_id = INFO_MODELOS[modelo_opcion]

    if st.button("🗑️ Limpiar Chat"):
        st.session_state.mensajes = []
        st.rerun()

# --- ESTADO DE SESIÓN ---
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# --- HISTORIAL DEL CHAT ---
for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# --- ENTRADA DEL USUARIO (siempre pegada al fondo) ---
if pregunta := st.chat_input("Escribe tu mensaje aquí..."):
    st.session_state.mensajes.append({"role": "user", "content": pregunta})
    with st.chat_message("user"):
        st.markdown(pregunta)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        respuesta_completa = ""

        try:
            stream = ollama.chat(
                model=modelo_id,
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.mensajes],
                stream=True
            )

            for chunk in stream:
                texto = chunk['message']['content']
                respuesta_completa += texto
                placeholder.markdown(respuesta_completa + "▌")

            placeholder.markdown(respuesta_completa)

        except Exception as e:
            st.error(f"Error: {e}")

    st.session_state.mensajes.append({"role": "assistant", "content": respuesta_completa})
