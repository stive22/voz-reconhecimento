import librosa
import numpy as np
import os

def extrair_mfcc(caminho_audio):
    y, sr = librosa.load(caminho_audio, sr=48000)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfcc, axis=1)

def comparar_vozes(arquivo_verificacao):
    emb_verificacao = extrair_mfcc(arquivo_verificacao)
    distancias = {}

    for arquivo in os.listdir("audios"):
        if arquivo.endswith(".wav") and arquivo != "verificacao.wav":
            emb_ref = extrair_mfcc(f"audios/{arquivo}")
            dist = np.linalg.norm(emb_verificacao - emb_ref)
            distancias[arquivo[:-4]] = dist

    if distancias:
        usuario, distancia = min(distancias.items(), key=lambda x: x[1])
        if distancia < 50:
            return usuario
    return None
