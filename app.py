import os
import streamlit as st
import base64
import openai
from PIL import Image
import numpy as np
from streamlit_drawable_canvas import st_canvas

# Configuración de la página
st.set_page_config(page_title="🖌️ Lienzo Creativo AI 🎉", layout="wide")

# Título y descripción de la aplicación
st.title("🌟 Lienzo Creativo con Inteligencia Artificial 🌈")
st.markdown("""
    #### Explora tu imaginación y deja que la IA analice tus creaciones.
    ✨ ¡Dibuja, pinta y recibe comentarios instantáneos! 🎊
""")

# Sidebar para opciones de personalización
with st.sidebar:
    st.header("🎨 Personaliza tu Herramienta")
    st.write("Ajusta las herramientas para dar vida a tus ideas.")
    
    # Controles para personalización del lienzo
    stroke_width = st.slider("🖍️ Grosor de Línea", 1, 100, 10, step=1)
    drawing_mode = st.selectbox("🖌️ Selecciona Herramienta:", ["Dibujar", "Línea", "Rectángulo", "Círculo", "Pincel", "Borrador", "Transformar"])
    
    st.write("### 🌈 Escoge el Color de Trazo")
    stroke_color = st.color_picker("Elige un color", "#1E90FF")  # Color azul brillante

    # Nuevo control para opacidad
    opacity = st.slider("🔆 Opacidad", 0.0, 1.0, 1.0, step=0.1)
    
    ke = st.text_input("🔑 Clave API de OpenAI", type="password", help="Introduce tu clave API aquí.")
    os.environ['OPENAI_API_KEY'] = ke

# Espacio para dibujar
st.write("### 🎉 Tu Espacio Creativo Sin Límites")
canvas_result = st_canvas(
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color="#F0F8FF",  # Color de fondo azul claro
    height=600,
    width=1000,
    drawing_mode=drawing_mode,
    key="canvas",
    initial_background_color="#FFFFFF",
    hide_axes=True,
    enable_dragging=True,
    enable_zoom=True,
    stroke_alpha=opacity
)

# Botón para analizar el dibujo
analyze_button = st.button("🔍 Analizar Dibujo con IA 🧠")
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
    prompt_text = "Describe brevemente esta imagen en español."

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
            background-color: #F0F8FF;  /* Fondo azul claro */
            padding: 20px;
            border-radius: 10px;
        }
        .sidebar .sidebar-content {
            background-color: #FFDEAD;  /* Fondo lateral en tono crema */
            border-radius: 10px;
            padding: 15px;
        }
        h1, h2, h3 {
            color: #FF4500; /* Cambiar el color de los encabezados a naranja */
        }
        .stButton>button {
            background-color: #4682B4; /* Color azul para los botones */
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)
