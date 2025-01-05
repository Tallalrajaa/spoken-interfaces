import serial  
import time  
import speech_recognition as sr  
import pyttsx3  
import webbrowser  
import sys  

try:
    pico = serial.Serial('COM4', 115200, timeout=1)  
except serial.SerialException as e:  
    print(f"Error: {e}")
    sys.exit(1) 

engine = pyttsx3.init()  
engine.setProperty('rate', 150)  

def speak(text):
    """Speak a given text using text-to-speech."""
    engine.say(text) 
    engine.runAndWait()  

def recognize_speech(prompt="What do you want?"):
    """Use speech recognition to capture and process voice commands."""
    recognizer = sr.Recognizer()  
    recognizer.energy_threshold = 300  
    recognizer.dynamic_energy_threshold = True  
    with sr.Microphone() as source:  
        speak(prompt) 
        print(prompt)  
        try:
            audio = recognizer.listen(source, timeout=5)  
            command = recognizer.recognize_google(audio)  
            print(f"You said: {command}") 
            return command  
        except sr.UnknownValueError:  
            print("Sorry, I didn't understand that.")  
            speak("Sorry, I didn't understand that.")
            return None  
        except sr.RequestError as e:  
            print(f"Could not request results; {e}")  
            speak("Speech service is unavailable.")  
            return None

def send_servo_angle(angle):
    """Send the servo angle to the Pico."""
    if 0 <= angle <= 180:  
        pico.write((str(angle) + '\n').encode()) 
        print(f"Sent angle: {angle}")  
        speak(f"Servo moved to {angle} degrees.") 
    else:
        print("Invalid angle. Please provide a number between 0 and 180.")  
        speak("Invalid angle. Please provide a number between 0 and 180.")  

def open_youtube():
    """Open YouTube in the default web browser."""
    webbrowser.open("https://www.youtube.com")  
    print("Opened YouTube.")  # Debugging feedback
    speak("Opening YouTube.")  

# Ask for the user's name at the start
name = recognize_speech("What is your name?")
name = "TALLAL"
if name:  
    print(f"DEAR, {name}!")
    speak(f"DEAR, {name}! Nice to meet you.")  
#else:  # If no name was provided
    #print("No name provided. Program ends.")  
   # speak("No name provided. Program ends.")  
   # pico.close()  
    #sys.exit(0)  # Exit the program

# Main Loop
try:
    while True:
        command = recognize_speech(f"{name}, what do you want?")  
        if command is None or command.strip() == "":  
            print("No command detected. Program ends.")  # Debugging feedback
            speak("Thank you. Program ends.")  # Voice feedback
            break  # Exit the loop
        command = command.lower()
        if "thank you for assistance" in command:  
            speak("You're welcome. Goodbye!")  
            print("Ending program on your request.")  
            break  # Exit the loop
        elif "move servo" in command: 
            angle_command = recognize_speech("What angle do you want to move the servo to?")  
            if angle_command and angle_command.isdigit():
                angle = int(angle_command)  
                send_servo_angle(angle)  
            else:  
                speak("Invalid angle. Please provide a number between 0 and 180.")  
        elif "open youtube" in command:  
            open_youtube()  
        else:  
            speak("I didn't understand that command. Please try again.")
            print("Unrecognized command.")
except KeyboardInterrupt:  
    print("Program interrupted. Exiting...")  
    speak("Program interrupted. Goodbye!")  
finally:
    pico.close()  
