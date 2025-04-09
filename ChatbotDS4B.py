from openai import OpenAI
from dotenv import load_dotenv
import os
import streamlit as st

# Carga las variables de entorno desde un archivo .env
load_dotenv()

# Inicializa el cliente de OpenAI con la clave API obtenida de las variables de entorno.
cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Función para cargar el contenido de un archivo markdown (.md)
def cargar_contexto_md(ruta_archivo):
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        return archivo.read()


# Carga el contexto
contexto = cargar_contexto_md("contexto.md")

# Título de la aplicación web con Streamlit
st.title("Chat bot DS4B")

# Inicializa el estado de la sesión de Streamlit si no existe.
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": f"Eres un chatbot para esta página web:\n\n{contexto}",
        },
        {
            "role": "assistant",
            "content": "Hola, en que puedo ayudarte?",
        },
    ]

# Muestra los mensajes anteriores en el chat (excepto los mensajes del sistema)
for msg in st.session_state["messages"]:
    if msg["role"] == "system":
        continue

    # Muestra el mensaje.
    st.chat_message(msg["role"]).write(msg["content"])

# Verifica si el usuario ha ingresado un mensaje
if input_usuario := st.chat_input():
    # Si el usuario ingresa un mensaje, lo añade al historial de mensajes
    st.session_state["messages"].append({"role": "user", "content": input_usuario})
    st.chat_message("user").write(
        input_usuario
    )  # Muestra el mensaje del usuario en el chat

    # Realiza una solicitud a OpenAI para obtener una respuesta del modelo GPT-3.5
    completion = cliente.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state["messages"],
        max_tokens=100,
        temperature=0,
    )

    # Obtiene la respuesta del modelo.
    respuesta = completion.choices[0].message.content

    # Añade la respuesta del asistente al historial de mensajes.
    st.session_state["messages"].append({"role": "assistant", "content": respuesta})
    st.chat_message("assistant").write(
        respuesta
    )  # Muestra la respuesta del asistente en el chat
