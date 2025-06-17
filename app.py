import streamlit as st
import sounddevice as sd
import soundfile as sf
import numpy as np
import os
from reconhecimento import comparar_vozes

st.set_page_config(page_title="Reconhecimento por Voz Simplificado")
st.title("🔊 Reconhecimento por Voz (Versão Leve)")

opcao = st.radio("Escolha uma opção:", ["Cadastrar Voz", "Verificar Voz"])

def gravar_audio(caminho, duracao=4, taxa=16000):
    st.info("🎙️ Gravando... fale agora.")
    audio = sd.rec(int(duracao * taxa), samplerate=taxa, channels=1)
    sd.wait()
    sf.write(caminho, audio, taxa)
    st.success(f"✅ Áudio salvo: {caminho}")

os.makedirs("audios", exist_ok=True)

if opcao == "Cadastrar Voz":
    nome = st.text_input("Nome do usuário:")
    if st.button("Gravar"):
        if nome:
            gravar_audio(f"audios/{nome}.wav")
        else:
            st.warning("Digite um nome antes de gravar.")

elif opcao == "Verificar Voz":
    if st.button("Gravar para Verificação"):
        gravar_audio("audios/verificacao.wav")
        resultado = comparar_vozes("audios/verificacao.wav")
        if resultado:
            st.success(f"🎉 Voz reconhecida: {resultado}")
        else:
            st.error("❌ Voz não reconhecida.")