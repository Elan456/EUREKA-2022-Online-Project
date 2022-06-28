# Python program to show
# how to convert text to speech
import pyttsx3
import time

# Initialize the converter
converter = pyttsx3.init()

# Set properties before adding
# Things to say


def askAlexa(phrase):
    converter.say("Alexa")
    converter.say(phrase)
    converter.runAndWait()
    waitForResponse()


def waitForResponse():
    time.sleep(2)

# Sets speed percent
# Can be more than 100
converter.setProperty('rate', 150)
# Set volume 0-1
converter.setProperty('volume', 0.7)

converter.setProperty("voice", r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")

# Queue the entered text
# There will be a pause between
# each one like a pause in
# a sentence

converter.save_to_file("I like chicken", 'speech.mp3')

askAlexa("What is the weather like?")
askAlexa("What time is it?")
askAlexa("Where am I?")
askAlexa("Are you mad at me?")
askAlexa("What is the temperature")
askAlexa("What is the weather like?")
askAlexa("What time is it?")
askAlexa("Where am I?")
askAlexa("Are you mad at me?")
askAlexa("What is the temperature")
askAlexa("What is the weather like?")
askAlexa("What time is it?")
askAlexa("Where am I?")
askAlexa("Are you mad at me?")
askAlexa("What is the temperature")
askAlexa("What is the weather like?")
askAlexa("What time is it?")
askAlexa("Where am I?")
askAlexa("Are you mad at me?")
askAlexa("What is the temperature")
askAlexa("Stop")