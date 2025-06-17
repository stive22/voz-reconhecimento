
import torch
import numpy as np
import soundfile as sf
from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
from pyannote.core import Segment
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = PretrainedSpeakerEmbedding("speechbrain/spkrec-ecapa-voxceleb", device=device)

def extrair_embedding(caminho_audio):
    audio, sample_rate = sf.read(caminho_audio)
    duration = len(audio) / sample_rate
    segment = Segment(0, duration)
    emb = model({'waveform': torch.tensor(audio.T).unsqueeze(0), 'sample_rate': sample_rate}, segment)
    return emb.detach().cpu().numpy().squeeze()

def comparar_vozes(audio1, audio2):
    emb1 = extrair_embedding(audio1)
    emb2 = extrair_embedding(audio2)
    sim = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
    return sim

def identificar_usuario(audio_teste, base_path="audios/", limiar=0.75):
    resultados = []
    for arquivo in os.listdir(base_path):
        if arquivo.endswith(".wav"):
            usuario = arquivo.split('.')[0]
            caminho_ref = os.path.join(base_path, arquivo)
            similaridade = comparar_vozes(caminho_ref, audio_teste)
            resultados.append((usuario, similaridade))

    melhores = sorted(resultados, key=lambda x: x[1], reverse=True)
    if melhores and melhores[0][1] > limiar:
        return f"{melhores[0][0]} (confiança: {melhores[0][1]:.2f})"
    else:
        return "Pessoa não reconhecida"
