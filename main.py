import pyttsx3
import pyaudio
import vosk
import json
import requests


#Синтез речи
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


#Распознавание речи
def listen():
    model = vosk.Model('vosk-model-small-ru-0.22')
    recognizer = vosk.KaldiRecognizer(model, 16000)

    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    print("Listening...")

    while True:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            text = json.loads(result).get("text", "")
            return text


#Команды
def get_random_user():
    response = requests.get('https://randomuser.me/api/')
    if response.status_code == 200:
        return response.json()['results'][0]
    else:
        return None

def create_user():
    user = get_random_user()
    if user:
        name = user['name']['first'] + " " + user['name']['last']
        speak(f"User created: {name}")
    else:
        speak("Failed to create user")

def say_name(user):
    name = user['name']['first'] + " " + user['name']['last']
    speak(f"The name is {name}")

def say_country(user):
    country = user['location']['country']
    speak(f"The country is {country}")

def save_picture(user):
    picture_url = user['picture']['large']
    picture_response = requests.get(picture_url)
    if picture_response.status_code == 200:
        with open('user_picture.jpg', 'wb') as file:
            file.write(picture_response.content)
        speak("Picture saved")
    else:
        speak("Failed to save picture")

def handle_command(command, user):
    if command == "создать":
        create_user()
    elif command == "имя":
        say_name(user)
    elif command == "страна":
        say_country(user)
    elif command == "сохранить":
        save_picture(user)
    else:
        speak("Unknown command")

if __name__ == "__main__":
    user = get_random_user()
    if user:
        while True:
            command = listen()
            handle_command(command, user)
    else:
        speak("Failed to retrieve user data")
