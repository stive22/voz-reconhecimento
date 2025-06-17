from pyannote.audio import Pipeline
import os

pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token=None)

def verificar_usuario(audio_path_verificacao):
    embeddings = {}
    for filename in os.listdir("audios"):
        if filename.endswith(".wav") and filename != "verificacao.wav":
            ref_path = os.path.join("audios", filename)
            diarization = pipeline(ref_path)
            embeddings[filename[:-4]] = diarization

    diarization_verificacao = pipeline(audio_path_verificacao)

    # Aqui está simplificado: só retorna o primeiro usuário como exemplo
    if embeddings:
        return list(embeddings.keys())[0]
    return None