import speech_recognition as sr
from pydub import AudioSegment
import math
import os

#convert mp3 to wav
def mp3_to_wav(mp3_file, wav_file):
    sound = AudioSegment.from_mp3(mp3_file)
    sound.export(wav_file, format="wav")


class SplitWavAudioMubin():
    def __init__(self, folder, filename):
        self.folder = folder
        self.filename = filename
        self.filepath = folder + filename
        
        self.audio = AudioSegment.from_wav(self.filepath)
    
    def get_duration(self):
        return self.audio.duration_seconds
    
    def single_split(self, from_min, to_min, split_filename):
        t1 = from_min * 60 * 1000
        t2 = to_min * 60 * 1000
        split_audio = self.audio[t1:t2]
        split_audio.export(self.folder +"//" + split_filename, format="wav")
        
    def multiple_split(self, min_per_split):
        total_mins = math.ceil(self.get_duration() / 60)
        for i in range(0, total_mins, min_per_split):
            split_fn = str(i) + '_' + self.filename
            self.single_split(i, i+min_per_split, split_fn)
            print(str(i) + ' Done')
            if i == total_mins - min_per_split:
                print('All splited successfully')


#convert mp3 to wav
mp3_to_wav('/home/rouxmi/Documents/so.mp3', '/home/rouxmi/Documents/Audio/so.wav')


folder = "/home/rouxmi/Documents/Audio/"
file = "so.wav"
split_wav = SplitWavAudioMubin(folder, file)
split_wav.multiple_split(min_per_split=1)

# get all the audio files from Audio folder
folder = "/home/rouxmi/Documents/Audio/"
files = os.listdir(folder)
files = [f for f in files if f.endswith('.wav')]
for f in files:
    if f == 'so.wav':
        continue
    #print the name of the file
    
    file_audio = sr.AudioFile(folder + f)
    r = sr.Recognizer()
    with file_audio as source:
        audio_text = r.record(source)

    # recognize speech using google
    text = r.recognize_google(audio_text, language='fr-FR')
    print(f + ' : Done')
    #put the text in a text file with the same name as the audio file
    with open(folder + f[:-4] + '.txt', 'w') as f:
        f.write(text)
        f.close()

# Join all the text files in a single text file in order from 0_so.txt to 66_so.txt
folder = "/home/rouxmi/Documents/Audio/"
files = os.listdir(folder)
files = [f for f in files if f.endswith('.txt')]
files.sort()
with open(folder + 'so.txt', 'w') as f:
    for file in files:
        with open(folder + file, 'r') as f1:
            f.write(f1.read())
            f1.close()
    f.close()
    


            
                                     
