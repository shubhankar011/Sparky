import os
import pyttsx3 as tts
import speech_recognition as sr
from groq import Groq
import time
from dotenv import load_dotenv

messages = [
    {
        "role": "system",
        "content": """
        You are Sparky, an AI-powered robotic assistant.
        Your name is Sparky.
        Be humane, concise, natural and witty if user is reponding in humour.
        Explain in not more than 30 words.
        Created 
"""
    }
]
# engine = tts.init()
recognizer = sr.Recognizer()

def speak(audio):
    engine = tts.init()

    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    print("trying to speak..")
    engine.say(audio)
    engine.runAndWait()
    engine.stop()
    time.sleep(0.2)
    print("finished speaking...")
    

def recognize():
    with sr.Microphone() as source:
        print("Adjusting, please wait! ...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        print("Listening...")
        
        try:
            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=10
            )
        except sr.WaitTimeoutError:
            print("No speech detected.")
            return False

        print("Processing audio...")

        try:
            print("Going to Google...")
            text = recognizer.recognize_google(audio, timeout=5)

            print("Done!")
            print(f"\nYou said: {text}")

            return text

        except sr.UnknownValueError:
            print("\nSorry, I could not understand the audio.")
            speak("Sorry, I could not understand the audio.")
            return False

        except sr.RequestException as e:
            print(f"\nCould not request results from the service: {e}")
            return False

load_dotenv(dotenv_path='.env')
TOKEN = os.getenv('GROQ_API_KEY')
Client = Groq()

while True:
    # user_input = recognize()
    user_input = input("You: ") # For debugging purpose
    if user_input == False:
        continue

    if user_input.lower() in ["exit", "quit"]:
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    response = Client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=messages,
        stream=True,
        temperature=0.7,
        reasoning_effort="none",
        max_completion_tokens=100
    )
    print("Sparky: ", end="", flush=True)

    answer = ""

    for chunk in response:
        delta = chunk.choices[0].delta.content
        if delta:
            print(delta, end="", flush= True)
            answer+=delta
    print()
    messages.append({
        "role": "assistant",
        "content": answer
    })
    speak(answer)

    # engine.setProperty('rate', 125)