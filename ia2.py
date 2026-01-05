import streamlit as st
import ollama
import streamlit.components.v1 as components  # <--- NUEVA IMPORTACIÓN

# --- DICCIONARIO DE MODELOS ---
INFO_MODELOS = {
    "Gemma 3 27B (Heavy / Solo pruebas)": "gemma3:27b-it-qat",
    "Gemma 3 12B (Recomendado RTX 4080)": "gemma3:12b-it-qat",
    "Gemma 2 (Equilibrio Premium)": "gemma2:27b",


    "Llama 3.1 (Oficial)": "llama3.1",
    "Llama 3.2 Vision (Multimodal)": "llama3.2-vision:latest",

    "DeepSeek R1 (Razonamiento Puro)": "deepseek-r1:32b",
    "DeepSeek Coder v2 (Técnico/Código)": "deepseek-coder-v2:lite",

    "Mistral Small (Lógica Pesada)": "mistral-small:latest",
    "Mistral NeMo (Optimizado NVIDIA)": "mistral-nemo:latest",

    "Qwen 2.5 32B (Generalista Potente)": "qwen2.5:32b",

    "Dolphin Llama 3 (Sin Censura)": "dolphin-llama3:latest",

    "LLaVA (Visión / Imagen)": "llava:latest",

    "Nomic Embed Text (Embeddings)": "nomic-embed-text:latest"
}


# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Chat IA", page_icon="🤖", layout="centered")

# --- CSS PERSONALIZADO ---
st.markdown("""
<style>
    .main > div {
        padding-bottom: 0px !important;
        height: 100vh;
        display: flex;
        flex-direction: column;
    }

    section[data-testid="stSidebar"] + div > div:first-child {
        flex-grow: 1;
        display: flex;
        flex-direction: column;
    }

    [data-testid="stVerticalBlock"] > div:first-child {
        flex-grow: 1;
        overflow-y: auto;
    }

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

# --- ENTRADA DEL USUARIO ---
if pregunta := st.chat_input("Escribe tu mensaje aquí..."):
    st.session_state.mensajes.append({"role": "user", "content": pregunta})
    with st.chat_message("user"):
        st.markdown(pregunta)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        respuesta_completa = ""

        # ENVIAR SEÑAL DE INICIO (Activa el latido)
        components.html("<script>window.parent.postMessage('start_thinking', '*');</script>", height=0)

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
        
        # ENVIAR SEÑAL DE FIN (Detiene el latido)
        components.html("<script>window.parent.postMessage('stop_thinking', '*');</script>", height=0)

    st.session_state.mensajes.append({"role": "assistant", "content": respuesta_completa})
