import os
import streamlit as st
import base64
import openai
from PIL import Image
import numpy as np
from streamlit_drawable_canvas import st_canvas

# Configuración de la página
st.set_page_config(page_title="🎨 Lienzo Creativo con IA", layout="wide")

# Título y descripción de la aplicación
st.title("🌈 Lienzo Creativo con Inteligencia Artificial ✨")
st.markdown("""
    #### Desata tu creatividad y permite que la IA analice tus obras.
    🎉 ¡Crea, dibuja y recibe retroalimentación al instante! 🚀
""")

# Sidebar para opciones de personalización
with st.sidebar:
    st.header("🛠️ Personaliza tu Experiencia de Dibujo")
    st.write("Ajusta las herramientas y colores para dar vida a tus ideas.")
    
    # Controles para personalización del lienzo
    stroke_width = st.slider("📏 Grosor de Línea", 1, 50, 8, step=1)
    drawing_mode = st.selectbox("✏️ Selecciona Herramienta:", ["Dibujar libremente", "Línea", "Rectángulo", "Círculo", "Transformar"])
    
    st.write("### 🎨 Escoge el Color del Trazo")
    stroke_color = st.color_picker("Selecciona un color", "#FF5733")
    
    ke = st.text_input("🔑 Clave API de OpenAI", type="password", help="Introduce tu clave API aquí para analizar tus dibujos.")
    os.environ['OPENAI_API_KEY'] = ke

# Espacio para dibujar
st.write("### 🎊 Tu Espacio Creativo Sin Límites")
canvas_result = st_canvas(
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color="#FFF8DC", 
    height=600,  
    width=1000,  
    drawing_mode=drawing_mode,
    key="canvas",
)

# Botón para analizar el dibujo
analyze_button = st.button("🔍 Analizar Dibujo con IA")
save_button = st.button("💾 Guardar Dibujo")

# Función para codificar la imagen en base64
def encode_image_to_base64(image_path):
    """Codifica una imagen en formato base64."""
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_image
    except FileNotFoundError:
        st.error("Error: La imagen no se encontró en la ruta especificada.")
        return None

# Función para guardar la imagen
def save_image(image):
    """Guarda la imagen en el sistema."""
    try:
        image.save("mi_dibujo.png")
        st.success("🖼️ ¡Dibujo guardado como 'mi_dibujo.png'!")
    except Exception as e:
        st.error(f"Error al guardar la imagen: {e}")

# Procesar el análisis si se ha dibujado algo y se ha ingresado la clave API
if canvas_result.image_data is not None and ke and analyze_button:
    st.write("🔄 **Procesando tu obra maestra...**")

    # Convertir el canvas a imagen y guardarla
    input_numpy_array = np.array(canvas_result.image_data)
    input_image = Image.fromarray(input_numpy_array.astype("uint8"), "RGBA")
    
    # Guardar imagen y codificar a base64
    input_image.save("img.png")
    base64_image = encode_image_to_base64("img.png")
    
    # Crear un mensaje para el análisis
    prompt_text = "Proporciona un análisis breve de esta imagen en español."

    if base64_image:  # Solo proceder si la codificación fue exitosa
        try:
            with st.spinner("Analizando..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "user", "content": prompt_text},
                        {"role": "user", "content": f"data:image/png;base64,{base64_image}"}
                    ],
                    max_tokens=500,
                )

                full_response = response.choices[0].message["content"]
                st.write("### 🔍 Resultado del Análisis:")
                st.success(full_response)  # Mostrar resultado con estilo de éxito
        except Exception as e:
            st.error(f"Error durante el análisis: {e}")

# Guardar la imagen si el botón es presionado
if save_button:
    if canvas_result.image_data is not None:
        save_image(input_image)
    else:
        st.warning("⚠️ No hay dibujo para guardar.")

# Advertencias si no se cumple alguna condición
else:
    if not ke:
        st.warning("⚠️ Por favor, ingresa tu clave API de OpenAI.")

# Estilos CSS para mejorar la apariencia
st.markdown(
    """
    <style>
        .reportview-container {
            background-color: #FFF8DC;  /* Fondo en amarillo suave */
            padding: 20px;
            border-radius: 10px;
        }
        .sidebar .sidebar-content {
            background-color: #FFE4B5;  /* Fondo lateral en tono melón */
            border-radius: 10px;
            padding: 15px;
        }
        h1, h2, h3 {
            color: #4B0082; /* Cambiar el color de los encabezados */
        }
        .stButton>button {
            background-color: #4CAF50; /* Color verde para los botones de analizar y guardar */
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)
