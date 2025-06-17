
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import av
import os
import queue
import soundfile as sf
from reconhecimento import identificar_usuario

st.set_page_config(page_title="Reconhecimento de Voz", layout="centered")
st.title("🎙️ Reconhecimento de Pessoas por Voz")

if not os.path.exists("audios"):
    os.makedirs("audios")

# Configuração WebRTC
client_settings = ClientSettings(
    media_stream_constraints={"audio": True, "video": False},
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
)

audio_queue = queue.Queue()

class AudioProcessor:
    def __init__(self) -> None:
        self.recorded_frames = []

    def recv(self, frame: av.AudioFrame):
        audio = frame.to_ndarray().flatten()
        audio_queue.put(audio)

st.header("🎤 Gravar voz para reconhecimento")
ctx = webrtc_streamer(
    key="audio",
    mode=WebRtcMode.SENDRECV,
    in_audio=True,
    client_settings=client_settings,
    audio_processor_factory=AudioProcessor,
)

if st.button("🔍 Identificar pessoa"):
    with st.spinner("Processando..."):
        audio_data = []
        while not audio_queue.empty():
            audio_data.extend(audio_queue.get())

        if len(audio_data) < 16000:
            st.error("Áudio muito curto. Fale por pelo menos 2 segundos.")
        else:
            caminho_teste = "audios/teste_stream.wav"
            sf.write(caminho_teste, audio_data, samplerate=16000)
            resultado = identificar_usuario(caminho_teste)
            st.success(f"✅ Resultado: {resultado}")

st.header("➕ Cadastrar novo usuário")
nome = st.text_input("Nome para cadastrar")
gravar_cadastro = st.button("🎙️ Gravar e salvar")

if gravar_cadastro and nome:
    with st.spinner("Gravando..."):
        audio_data = []
        while not audio_queue.empty():
            audio_data.extend(audio_queue.get())

        if len(audio_data) < 16000:
            st.error("Áudio muito curto. Fale por pelo menos 2 segundos.")
        else:
            caminho_user = f"audios/{nome.lower()}.wav"
            sf.write(caminho_user, audio_data, samplerate=16000)
            st.success(f"Usuário '{nome}' cadastrado com sucesso!")
