import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image

# ===============================
# CONFIGURACIÓN INICIAL
# ===============================
st.set_page_config(page_title="Texto a Audio", page_icon="🎧", layout="centered")

# Crear carpeta temporal si no existe
os.makedirs("temp", exist_ok=True)

# ===============================
# INTERFAZ
# ===============================
st.title("🎧 Conversión de Texto a Audio")
image = Image.open('gato_raton.png')
st.image(image, width=350)

with st.sidebar:
    st.subheader("📌 Instrucciones")
    st.write("Escribe o pega un texto y conviértelo en audio.")
    st.write("Puedes elegir entre **Español** e **Inglés**.")

st.subheader("Una pequeña fábula")
st.write("""
¡Ay! -dijo el ratón-. El mundo se hace cada día más pequeño. 
Al principio era tan grande que le tenía miedo. Corría y corría 
y por cierto que me alegraba ver esos muros, a diestra y siniestra, 
en la distancia. Pero esas paredes se estrechan tan rápido que me 
encuentro en el último cuarto y ahí en el rincón está la trampa sobre 
la cual debo pasar. Todo lo que debes hacer es cambiar de rumbo dijo 
el gato... y se lo comió.  
— Franz Kafka
""")

# Entrada de texto
text = st.text_area("Ingrese el texto a escuchar:")

# Selección de idioma
option_lang = st.selectbox("🌐 Selecciona el idioma", ["Español", "English"])
lg = "es" if option_lang == "Español" else "en"


# ===============================
# FUNCIÓN DE CONVERSIÓN
# ===============================
def text_to_speech(text, lang):
    """Convierte texto a archivo mp3 con gTTS"""
    if not text.strip():
        return None

    # Nombre dinámico de archivo
    file_name = f"temp/audio_{int(time.time())}.mp3"
    tts = gTTS(text, lang=lang)
    tts.save(file_name)
    return file_name


# ===============================
# BOTÓN DE CONVERSIÓN
# ===============================
if st.button("🔊 Convertir a Audio"):
    if text.strip():
        audio_path = text_to_speech(text, lg)

        if audio_path:
            st.success("✅ Conversión completada!")
            st.audio(audio_path, format="audio/mp3")

            # Botón de descarga nativo Streamlit
            with open(audio_path, "rb") as file:
                st.download_button(
                    label="⬇️ Descargar Audio",
                    data=file,
                    file_name="audio.mp3",
                    mime="audio/mp3"
                )
    else:
        st.warning("⚠️ Por favor ingrese un texto antes de convertir.")


# ===============================
# LIMPIEZA DE ARCHIVOS ANTIGUOS
# ===============================
def remove_old_files(days: int = 7):
    """Elimina audios viejos de la carpeta temp"""
    now = time.time()
    max_age = days * 86400  # días en segundos
    for f in glob.glob("temp/*.mp3"):
        if os.stat(f).st_mtime < now - max_age:
            os.remove(f)

remove_old_files()

