import speech_recognition as sr
import webbrowser
import pyttsx3
import urllib.parse
import music

recognizer = sr.Recognizer()
engine = pyttsx3.init() 

def speak(text):
    print(f"Hammer: {text}")
    engine.say(text)
    engine.runAndWait()


def processCommand(a):
    command_lower = a.strip().lower()

    if command_lower in ["exit", "quit", "stop", "bye", "shutdown"]:
        return False

    if "open google" in command_lower:
        webbrowser.open("https://google.com")
    elif "open facebook" in command_lower:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in command_lower:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in command_lower:
        webbrowser.open("https://linkedin.com")
    elif "open spotify" in command_lower:
        webbrowser.open("https://open.spotify.com/")
    elif command_lower.startswith("play"):
        parts = command_lower.split("play", 1)
        song = parts[1].strip() if len(parts) > 1 else ""

        if not song:
            return True

        if song in music.musiclib:
            webbrowser.open(music.musiclib[song])
           
        else:
            search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(song)}"
            webbrowser.open(search_url)
    
    elif command_lower.startswith("search"):
        query = command_lower.replace("search", "", 1).strip()
        if query:
            search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
            webbrowser.open(search_url)
        else:
            speak("What would you like me to search for?")
    else:
        speak("Sorry, I didn't recognize that command.")

    return True


if __name__ == "__main__":
    speak("Initializing Hammer....")
    r = sr.Recognizer()

    # Calibrate microphone for ambient noise at startup
    try:
        with sr.Microphone() as source:
            print("Calibrating microphone for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=1)
            print("Microphone ready.")
    except Exception as e:
        print(f"Warning: Could not calibrate microphone: {e}")

    running = True
    while running:
        try:
            with sr.Microphone() as source:
                print("\nListening for wake word 'Hammer'...")
                audio = r.listen(source, timeout=5, phrase_time_limit=8)

            print("Recognizing...")
            word = r.recognize_google(audio).strip()
            print(f"Heard: {word}")

            lower_word = word.lower()
            if "hammer" in lower_word:
                # Check if command was included in the same utterance (e.g., "Hammer open YouTube")
                parts = lower_word.split("hammer", 1)
                direct_command = parts[1].strip() if len(parts) > 1 else ""

                if direct_command:
                    print(f"Executing direct command: {direct_command}")
                    running = processCommand(direct_command)
                else:
                    speak("Coming...")
                    # Listen for subsequent command
                    try:
                        with sr.Microphone() as source:
                            print("Hammer Activated, listening for command...")
                            audio = r.listen(source, timeout=6, phrase_time_limit=10)
                        command = r.recognize_google(audio)
                        print(f"Command: {command}")
                        running = processCommand(command)
                    except sr.WaitTimeoutError:
                        print("Listening timed out waiting for command.")
                    except sr.UnknownValueError:
                        speak("Sorry, I could not understand your command.")

        except sr.WaitTimeoutError:
            # Idle timeout waiting for phrase - continue silently
            pass
        except sr.UnknownValueError:
            # Audio was heard but not recognized - continue listening silently
            pass
        except sr.RequestError as e:
            print(f"Google Speech Recognition service error: {e}")
            speak("Network error connecting to speech recognition service.")
        except Exception as e:
            print(f"Unexpected error: {e}")


        

