import speech_recognition as sr
import pyttsx3
import datetime
import os
import webbrowser
import requests

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-US')
            print(f"User said: {query}\n")
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return "None"
        except sr.RequestError:
            print("Request error from Google Speech Recognition service")
            return "None"
        return query.lower()

def tell_time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The current time is {current_time}")

def open_website(url):
    webbrowser.open(url)
    speak(f"Opening {url}")

def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak(f"Searching for {query}")

def get_weather(city):
    api_key = "your_openweathermap_api_key"  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + city + "&appid=" + api_key
    response = requests.get(complete_url)
    data = response.json()
    
    if data["cod"] != "404":
        main = data["main"]
        temperature = main["temp"]
        weather_desc = data["weather"][0]["description"]
        speak(f"The temperature in {city} is {temperature - 273.15:.2f} degrees Celsius with {weather_desc}")
    else:
        speak("City not found")

def open_application(path):
    os.startfile(path)
    speak(f"Opening application {path}")

def perform_task(query):
    if 'time' in query:
        tell_time()
    elif 'open website' in query:
        speak("Please tell me the website URL")
        url = listen()
        if url != "None":
            open_website(url)
    elif 'search' in query:
        speak("What do you want to search for?")
        search_query = listen()
        if search_query != "None":
            search_web(search_query)
    elif 'weather' in query:
        speak("Please tell me the city name")
        city = listen()
        if city != "None":
            get_weather(city)
    elif 'open application' in query:
        speak("Please tell me the application path")
        app_path = listen()
        if app_path != "None":
            open_application(app_path)
    else:
        speak("Sorry, I don't understand that. Can you please repeat?")

def main():
    speak("Hello, how can I assist you today?")
    while True:
        query = listen()
        
        if 'exit' in query or 'bye' in query or 'quit' in query:
            speak("Goodbye! Have a great day!")
            break

        perform_task(query)

if __name__ == "__main__":
    main()
