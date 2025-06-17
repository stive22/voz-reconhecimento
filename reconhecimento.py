import librosa
import numpy as np
import os

def extrair_mfcc(caminho):
    y, sr = librosa.load(caminho, sr=16000)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfcc, axis=1)

def comparar_vozes(caminho_teste):
    emb = extrair_mfcc(caminho_teste)
    dist = {}
    for f in os.listdir("audios"):
        if f.endswith(".wav") and f != "verificacao.wav":
            d = np.linalg.norm(emb - extrair_mfcc(f"audios/{f}"))
            dist[f[:-4]] = d
    if dist:
        nome, dmin = min(dist.items(), key=lambda x: x[1])
        if dmin < 50:
            return nome
    return None
