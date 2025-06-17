import streamlit as st
from reconhecimento import comparar_vozes
import soundfile as sf
import os

st.title("🔊 Reconhecimento de Voz (Upload de Áudio)")

os.makedirs("audios", exist_ok=True)

st.header("➕ Cadastrar voz")
user_name = st.text_input("Nome do usuário:")
uploaded_ref = st.file_uploader("Envie um áudio (.wav) para cadastro", type="wav", key="cadastro")
if st.button("Cadastrar"):
    if user_name and uploaded_ref:
        with open(f"audios/{user_name}.wav", "wb") as f:
            f.write(uploaded_ref.read())
        st.success(f"✅ Usuário {user_name} cadastrado!")
    else:
        st.error("Preencha nome e áudio de cadastro.")

st.header("🎤 Verificar voz")
uploaded_test = st.file_uploader("Envie um áudio (.wav) para verificação", type="wav", key="verificacao")
if st.button("Verificar"):
    if uploaded_test:
        with open("audios/verificacao.wav", "wb") as f:
            f.write(uploaded_test.read())
        resultado = comparar_vozes("audios/verificacao.wav")
        if resultado:
            st.success(f"Voz reconhecida: {resultado}")
        else:
            st.error("❌ Voz não reconhecida.")
    else:
        st.error("Envie um áudio para verificação.")
