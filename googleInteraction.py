import os
import config
from google.cloud import texttospeech
credentialPath = config.path
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=credentialPath

def synthesizeText(textToSynthesize,outputFilename):
    """Synthesizes speech from the input file of text."""
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=textToSynthesize)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", name="en-US-Wavenet-D"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    # The response's audio_content is binary.
    with open(outputFilename, "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "ending.mp3"')