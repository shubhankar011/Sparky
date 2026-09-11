import os
import pyttsx3 as tts
import speech_recognition as sr
from groq import Groq
import time
messages = [
    {
        "role": "system",
        "content": """
You are Sparky, an AI-powered robotic assistant.
Your name is Sparky.
Be witty, concise, and natural.
Explain in not more than 30 words.
Your maker is Shubhankar and his team.
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
        audio = recognizer.listen(source)
        print("Processing audio...")
        try:
            text = recognizer.recognize_google(audio)
            print(f"\nYou said: {text}")
            
        except sr.UnknownValueError:
            text = False
            print("\nSorry, I could not understand the audio.")
            speak("Sorry, I could not understand the audio.")
        except sr.RequestException as e:
            text = False
            print(f"\nCould not request results from the service; {e}")
    return text

os.environ['GROQ_API_KEY'] = "API_KEY"
Client = Groq()

while True:
    user_input = recognize()
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
        reasoning_effort="none"
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
