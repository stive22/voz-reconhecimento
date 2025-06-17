import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import av
import os
import numpy as np
import wave
from reconhecimento import comparar_vozes

st.set_page_config(page_title="Reconhecimento de Voz via Navegador")
st.title("🔊 Reconhecimento de Voz (WebRTC)")

os.makedirs("audios", exist_ok=True)

class AudioProcessor:
    def __init__(self):
        self.frames = []

    def recv(self, frame):
        audio = frame.to_ndarray()
        self.frames.append(audio)
        return av.AudioFrame.from_ndarray(audio, layout="mono")

def salvar_audio(frames, filename):
    audio = np.concatenate(frames, axis=0).astype(np.int16)
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(48000)
        wf.writeframes(audio.tobytes())

modo = st.radio("Escolha uma opção:", ["Cadastrar voz", "Verificar voz"])

if modo == "Cadastrar voz":
    nome = st.text_input("Nome do usuário para cadastro:")
    if nome:
        st.info("Grave sua voz por 5 segundos")
        ctx = webrtc_streamer(
            key="cadastro",
            mode=WebRtcMode.SENDONLY,
            in_audio=True,
            client_settings=ClientSettings(media_stream_constraints={"audio": True, "video": False}),
            audio_processor_factory=AudioProcessor,
        )
        if ctx.audio_processor and st.button("Salvar voz"):
            salvar_audio(ctx.audio_processor.frames, f"audios/{nome}.wav")
            st.success("✅ Voz cadastrada com sucesso.")

elif modo == "Verificar voz":
    st.info("Grave sua voz para verificação (5 segundos)")
    ctx = webrtc_streamer(
        key="verificar",
        mode=WebRtcMode.SENDONLY,
        in_audio=True,
        client_settings=ClientSettings(media_stream_constraints={"audio": True, "video": False}),
        audio_processor_factory=AudioProcessor,
    )
    if ctx.audio_processor and st.button("Verificar voz"):
        salvar_audio(ctx.audio_processor.frames, "audios/verificacao.wav")
        resultado = comparar_vozes("audios/verificacao.wav")
        if resultado:
            st.success(f"🎉 Voz reconhecida: {resultado}")
        else:
            st.error("❌ Voz não reconhecida.")
