import streamlit as st
import pandas as pd
import openai

# Configuración inicial
st.title("Análisis de Base de Datos con OpenAI")
st.sidebar.header("Configuración")

# Solicitar la API Key desde la interfaz
api_key = st.sidebar.text_input("Introduce tu API Key de OpenAI", type="password")

if api_key:
    openai.api_key = api_key

    # Subida de archivo
    uploaded_file = st.file_uploader("Sube tu archivo de Excel", type=["xlsx", "xls"])

    if uploaded_file:
        # Cargar datos de Excel
        try:
            df = pd.read_excel(uploaded_file)
            st.write("Vista previa de los datos:")
            st.dataframe(df)

            # Conversión de los datos a texto para el modelo
            df_summary = df.head(10).to_string(index=False)
            st.write("Resumen de los datos cargados (primeras 10 filas):")
            st.text(df_summary)

            # Entrada del usuario
            question = st.text_area("Haz una pregunta sobre los datos:")

            if st.button("Enviar pregunta"):
                try:
                    # Crear el contexto para la API de Chat
                    messages = [
                        {"role": "system", "content": "Eres un asistente que ayuda a analizar datos en tablas."},
                        {
                            "role": "user",
                            "content": f"Tengo la siguiente tabla de datos:\n{df_summary}\n\n"
                                       f"Por favor, responde esta pregunta basada en los datos: {question}"
                        }
                    ]

                    # Llamada a la API de OpenAI
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",  # Cambiar a 'gpt-4' si tienes acceso
                        messages=messages,
                        max_tokens=150,
                        temperature=0.5
                    )

                    # Mostrar la respuesta
                    answer = response["choices"][0]["message"]["content"].strip()
                    st.write("Respuesta:")
                    st.write(answer)

                except Exception as e:
                    st.error(f"Error al procesar la pregunta: {e}")
        except Exception as e:
            st.error(f"No se pudo procesar el archivo: {e}")
    else:
        st.info("Por favor, sube un archivo de Excel para comenzar.")
else:
    st.warning("Por favor, introduce tu API Key de OpenAI en la barra lateral para continuar.")
