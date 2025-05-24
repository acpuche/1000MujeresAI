# Frontend (FE)
import requests
import streamlit as st
from PIL import Image
from io import BytesIO  # Importar BytesIO para la conversión de imágenes
import base64

# Load custom CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load and encode the image
image = Image.open("feelsread-small.png")  # Adjust the image filename as needed

# Convert the image to Base64
buffered = BytesIO()
image.save(buffered, format="PNG")
encoded_image = base64.b64encode(buffered.getvalue()).decode()

# Display the centered image
st.markdown(
    f"""
    <div class="centered-image">
        <img src="data:image/png;base64,{encoded_image}" alt="Centered Image">
    </div>
    """,
    unsafe_allow_html=True
)

# Definición de la URL de la API
API_URL = "http://localhost:8000/sentiment/"

# Streamlit interface, # Configuración de la página
# Center the title using HTML
st.markdown(
    """
    <h1 style="text-align: center;">Sentiment Analysis of Book Reviews</h1>
    """,
    unsafe_allow_html=True
)

# Mostrar disclaimer al iniciar la página
if 'show_disclaimer' not in st.session_state:
        with st.expander("Disclaimer", expanded=True):
            st.warning(
                """
                **Disclaimer of Use for Sentiment Analysis API**

                The Sentiment Analysis API provides automated sentiment assessments based on user-entered text. 
                This API is intended for informational and research purposes and should not be used as a substitute 
                for human interpretation in critical contexts. Although our model has been trained to achieve high accuracy, 
                its predictions may not be accurate in all cases due to technical limitations and variations in natural language.

                By using this API, users accept the terms and conditions described in this notice and release the development 
                team from any liability arising from the use of the API, including decisions made based on the results provided by the API.
                """
            )
            if st.button("I Accept"):
                st.session_state.show_disclaimer = False

else:  
    st.markdown('Write a review about the book you just read and receive a positive (👍) or negative (👎) rating: \n')
    review = st.text_area("") # Text Area para ingreso de usuario
    if st.button('Submit'):
        if review:
            # Preparar los datos para enviar a la API
            data = {"text": review}
            # Hacer la solicitud POST a la API
            response = requests.post(API_URL, json=data)
            if response.status_code == 200:
                results = response.json()
                stars = int(max(results, key=results.get).split('_')[0])  # Split y conversión a entero
                if stars == 2:
                    st.markdown("Review rating: 👍")
                else:
                    st.markdown("Review rating: 👎")
            else:
                st.error("Error in API response")
        else:
            st.warning("Please write a review for analysis.")
        

