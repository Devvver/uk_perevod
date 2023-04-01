import os
import random
import sys
import winsound
from pathlib import Path
import speech_recognition#Требуется для прослушки команд

from playsound import playsound#Требуется для озвучивание текста
import time
from googletrans import Translator
from ukrainian_tts.tts import TTS, Voices, Stress
import IPython.display as ipd

print()
tts = TTS(device="cpu")  # can try gpu, mps
winsound.PlaySound(str(Path("perevod_uk", 'kommand.wav')), winsound.SND_FILENAME)
while True:
    sr = speech_recognition.Recognizer()
    sr.pause_threshold = 0.5
    print("Скажи команду")


    commands_dict = {#Все команды прописываются тут 
        'commands': {           
            'greeting': ['перевод', 'переведи', 'переводчик'],
            'exit_program':['выход']
        }
    }
    def exit_program():
        print('До свидания')
        winsound.PlaySound(str(Path ("perevod_uk",'poka.wav')), winsound.SND_FILENAME)
        sys.exit()

    def translator_translate(word):
        translator = Translator()
        result = translator.translate(word, dest='uk')
        return result.text


    def listen_command():#распознает слова в тексте
        try:
            print("Слушаю микрофон")
            sr = speech_recognition.Recognizer()
            sr.pause_threshold = 0.5
            with speech_recognition.Microphone() as mic:
                sr.adjust_for_ambient_noise(source=mic, duration=0.5)
                audio = sr.listen(source=mic)
                query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()

            return query
        except speech_recognition.UnknownValueError:
            return 'generate2'
        except speech_recognition.RequestError as e:
            print("Не удалось запросить результаты у службы распознавания речи Google; {0}".format(e))

    def greeting():#вызывывает ответ на перевод
        #hello = ['voice/hello/hello.mp3', 'voice/hello/hello2.mp3', 'voice/hello/hello3.mp3']
        #playsound(random.choice(hello))
        print("Скажите фразу")
        query2 = listen_command()
        print(query2)
        fff = translator_translate(query2)
        print(fff)
        if query2 == "generate2":
            print("Я вас не понял")
            winsound.PlaySound(str(Path ("perevod_uk",'ne_ponyal.wav')), winsound.SND_FILENAME)
            return
        else:

            with open(str(Path ("perevod_uk",query2+".wav")), mode="wb") as file:
                _, output_text = tts.tts(fff, Voices.Dmytro.value, Stress.Dictionary.value, file)
            print("Accented text:", output_text)

            ipd.Audio(filename=str(Path ("perevod_uk",query2+".wav")))
            winsound.PlaySound(str(Path ("perevod_uk",query2+".wav")), winsound.SND_FILENAME)
            if os.path.isfile(str(Path ("perevod_uk",query2+".wav"))):
                os.remove(str(Path ("perevod_uk",query2+".wav")))
            else:
                print('файл или путь не найден')




    def main():#Сравнивает команды с командами в списке

        query = listen_command()
        
        for k, v in commands_dict['commands'].items():
            if query in v:
                print(globals()[k]())
            

    if __name__ == '__main__':
        main()



