# importing libraries
import shutil
import uuid

import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

# create a speech recognition object
r = sr.Recognizer()

TYPES = {
    'wav': AudioSegment.from_wav,
    'mp3': AudioSegment.from_mp3,
    'ogg': AudioSegment.from_ogg
}


def transcription_fast_audio(path, lang='en-US', audio_type='wav'):
    with sr.AudioFile(path) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data, language=lang)
        print(text)
        return text


def transcription_audio(path, lang='en-US', audio_type='wav'):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = TYPES[audio_type](path)
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
                              # experiment with this value for your target audio file
                              min_silence_len=500,
                              # adjust this per requirement
                              silence_thresh=sound.dBFS - 14,
                              # keep the silence for 1 second, adjustable as well
                              keep_silence=500,
                              )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}." + audio_type)
        audio_chunk.export(chunk_filename, format=audio_type)
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened, language=lang)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    remove_chunk_files()
    return whole_text


def write_text_on_file(text, experiment_id):
    """
    Write the text on a file
    """
    with open('{}.txt'.format(experiment_id), mode='w') as file:
        file.write(text)
        print("The text is written on file successfully.")
    file.close()


def remove_chunk_files():
    """
    Remove the audio chunks
    """
    folder_name = "audio-chunks"
    # remove the directory and all contents
    for filename in os.listdir(folder_name):
        file_path = os.path.join(folder_name, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    os.rmdir(folder_name)


if __name__ == "__main__":
    print("Please wait...")
    path = os.path.join("../gravacao.wav")
    print("Start...")
    text = transcription_audio(path, lang='pt-BR', audio_type='wav')
    print("Finish...")
    write_text_on_file(text, str(uuid.uuid4()))
    remove_chunk_files()
