import random
import speech_recognition as sr
import pyttsx3


class SpeechToText():
    def __init__(self) -> None:
        self.recognizer=sr.Recognizer()

    def Speech_to_text(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source,duration=0.7)
            listen = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(listen)
                return text
            except:
                return False


class TextToSpeech():
    def __init__(self) -> None:
        self.speaker = pyttsx3.init()

        self.volume = self.speaker.getProperty("volume")
        self.voice = self.speaker.getProperty("voices")
        self.rate = self.speaker.getProperty("rate")

        self.speaker.setProperty("volume",1.0)
        self.speaker.setProperty("voice",self.voice[random.randint(0,1)].id)
        self.speaker.setProperty("rate",140)

    def Text_to_speech(self,text):
        self.speaker.say(text)
        self.speaker.runAndWait()