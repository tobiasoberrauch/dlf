from pydub import AudioSegment
from huggingsound import SpeechRecognitionModel
import os

model = SpeechRecognitionModel("jonatasgrosman/wav2vec2-large-xlsr-53-german")

def split_audio(audio_path, chunk_length=60000):  # chunk_length in milliseconds
    audio = AudioSegment.from_file(audio_path)
    for i in range(0, len(audio), chunk_length):
        yield audio[i:i + chunk_length]

audio_directory = 'data/bronze'
transcription_directory = 'data/silver'

if not os.path.exists(transcription_directory):
    os.makedirs(transcription_directory)

for filename in os.listdir(audio_directory):
    if filename.endswith('.mp3') or filename.endswith('.wav'):
        audio_path = os.path.join(audio_directory, filename)
        base_name = os.path.splitext(filename)[0]
        transcription_file = os.path.join(transcription_directory, f"{base_name}.txt")
        
        with open(transcription_file, 'w') as file:
            for chunk in split_audio(audio_path):
                transcription = model.transcribe(chunk.raw_data)
                file.write(transcription['transcription'] + '\n\n')

        print(f"Transcription for {audio_path} saved to {transcription_file}")
