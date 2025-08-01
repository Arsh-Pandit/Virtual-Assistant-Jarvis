import speech_recognition as sr
import webbrowser
import pyttsx3
import musicPlayer
import requests
import openai
import os

from dotenv import load_dotenv

load_dotenv()

recoginizer = sr.Recognizer() # The recognizer for the speech
engine = pyttsx3.init() #Initialize the text to speech module
newsapi = os.getenv("NEWS_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")
def speak(text):
    engine.say(text)
    engine.runAndWait()

def openchat(command):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": command}
        ]
        
    )
    return response['choices'][0]['message']['content']


def processCommand (command):
    print(command)
    if "google" in command.lower():
        webbrowser.open("https://google.com")
    elif "facebook" in command.lower():
        webbrowser.open("https://facebook.com")
    elif "youtube" in command.lower():
        webbrowser.open("https://youtube.com")
    elif command.lower().startswith("play"):
       song = command.lower().split()[1]
       link = musicPlayer.music[song]
       webbrowser.open(link)
    elif "news" in command.lower():
        r = requests.get(f"https://newsdata.io/api/1/latest?apikey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            if "results" in data:
                for idx, article in enumerate(data["results"][:5], start=1):  # top 5 articles
                    print(f"\n{idx}. {article.get('title')}")
                    print(f"   Source: {article.get('source_id')}")
                    print(f"   Link: {article.get('link')}")
            else:
               print("No results found.")
    else:
        output = openchat(command)
        speak(output)


if __name__ == "__main__" :
    speak("Intializing Jarvis")
    #Checking the wake you call

    # obtain audio from the microphone
    while True:
        print("Recognizing....")
        try:
            with sr.Microphone() as source:
                print("Listening....")
                audio = recoginizer.listen(source,timeout=5,phrase_time_limit=3)   # recognize speech using Jarvis
            word = recoginizer.recognize_google(audio)
            print(word)
            if (word.lower() == "jarvis"):
                speak("Yes Sir, How can I help you")
                with sr.Microphone() as source:
                    print("Jarvis Active....")
                    audio = recoginizer.listen(source,timeout=5,phrase_time_limit=3) 
                command = recoginizer.recognize_google(audio)
                processCommand(command)
        except Exception as e:
            print("Jarvis error; {0}".format(e)) 

    
