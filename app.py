import streamlit as st
from reconhecimento import verificar_usuario
import sounddevice as sd
import soundfile as sf
import os

st.set_page_config(page_title="Reconhecimento por Voz", layout="centered")
st.title("🔊 Reconhecimento de Usuário por Voz")

opcao = st.radio("Escolha uma opção:", ("Cadastrar voz", "Verificar voz"))

if not os.path.exists("audios"):
    os.makedirs("audios")

def gravar_audio(filename, duration=5, sample_rate=16000):
    st.info("Gravando... Fale agora")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    sf.write(filename, audio, sample_rate)
    st.success(f"Áudio salvo como: {filename}")

if opcao == "Cadastrar voz":
    nome = st.text_input("Digite um nome para o cadastro:")
    if st.button("Gravar voz"):
        if nome:
            filepath = f"audios/{nome}.wav"
            gravar_audio(filepath)
        else:
            st.warning("Digite um nome antes de gravar.")

elif opcao == "Verificar voz":
    if st.button("Gravar voz para verificação"):
        filepath = f"audios/verificacao.wav"
        gravar_audio(filepath)
        resultado = verificar_usuario(filepath)
        if resultado:
            st.success(f"Usuário identificado: {resultado}")
        else:
            st.error("Usuário não reconhecido.")