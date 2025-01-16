import subprocess
import os
from google.cloud import texttospeech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcloud_keys.json"



def synthesize_text(text):
    """Synthesizes speech from the input string of text."""
    

    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="es-ES",
        name="es-ES-Wavenet-B",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    # The response's audio_content is binary.
    with open("tmp/output.mp3", "wb") as out:
        out.write(response.audio_content)



def convertir_mp3_a_wav(ruta_mp3, ruta_wav):
    # Convertir MP3 a WAV usando mpg123
    comando_convertir = ["mpg123", "-w", ruta_wav, ruta_mp3]
    subprocess.run(comando_convertir)



def reproducir_wav_con_aplay(ruta_wav):
    # Reproducir archivo WAV con aplay
    comando_aplay = ["aplay", ruta_wav]
    subprocess.run(comando_aplay)



def eliminar_archivos(ruta_mp3, ruta_wav):
    # Eliminar archivos después de la reproducción
    os.remove(ruta_mp3)
    os.remove(ruta_wav)




def texto_a_voz_festival(texto):

    synthesize_text(texto)
    convertir_mp3_a_wav("tmp/output.mp3","tmp/output.wav")
    reproducir_wav_con_aplay("tmp/output.wav")
    eliminar_archivos("tmp/output.mp3","tmp/output.wav")
