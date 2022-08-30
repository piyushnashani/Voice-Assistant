# VA for VoiceAssistant
import sys
import pyttsx3  # Used for transformation of text to speech
import webbrowser  # for web searching
import speech_recognition as sr
import datetime
import pyjokes
from geopy import Nominatim
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import random
import requests
import wikipedia
import os
import geocoder
import cv2
import pyautogui as pg
import pywhatkit
import smtplib
from bs4 import BeautifulSoup
import time
from datetime import date,datetime

name= "Piyush"
chrome_path = 'C:\Program Files\Google\Chrome\Application\chrome.exe %s'
# webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path),1)


def sendemail(mailID, content):
    server = smtplib.SMTP('smtp.gmail.com',587)     # 587 - open source server
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('your mail id', 'two step verification password')
    server.sendmail(
        'mail id of whom you want to send',
        mailID,
        content
    )
    text_to_speech("Email has been sent")
    server.quit()


def wish():
    hour = int(datetime.now().hour)
    if 0 <= hour <= 12:
        text_to_speech(f"Good morning {name} sir")
    elif 12 < hour < 18:
        text_to_speech(f"Good Afternoon {name} sir")
    else:
        text_to_speech(f"Good Evening {name} sir")
    text_to_speech("I am Jarvis, please tell me how can I help you?")


start = 0


def speech_to_text():
    global start
    recognizer = sr.Recognizer()  # object, Recognizer = class
    with sr.Microphone() as source:
        print("Listening...")
        # Your voice assistant should not stop listening you, while you are speaking
        recognizer.pause_threshold = 1
        # Noise cancellation
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, phrase_time_limit=5)
        try:
            print("Recognizing...")
            # speech to text
            data = recognizer.recognize_google(audio)
            print(data)
            start = start + 1
            return data
        except sr.UnknownValueError as e:
            if start == 0:
                start = start + 1
                print("Couldn't get you?")
                text_to_speech("Couldn't get you?")
            return ""


def text_to_speech(x):
    # object initialization
    engine = pyttsx3.init()  # init class
    # Setting voice assistant' voice
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # 0 for male voice,1 and 2 for female voices
    rate = engine.getProperty('rate')  # speed of VA
    engine.setProperty('rate', 220)
    print(x)
    engine.say(x)
    engine.runAndWait()


def news():
    your_api_key =""
    news_url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={your_api_key}"
    news_page = requests.get(news_url).json()
    articles = news_page["articles"]
    headlines = []
    for head in articles:
        headlines.append(head['title'])
    for i in range(10):
        if i == 0:
            text_to_speech("Sir today's first news is:")
        text_to_speech(headlines[i])


def program():
    pg.press('esc')
    text_to_speech("Verification Successful")
    wish()
    # name = speech_to_text()
    # if float(fuzz.token_set_ratio(name.lower(), "hi vision")) > 60:
    #     # print("Hello sir")
    #     # text_to_speech("Hello sir")
    while True:
        data = speech_to_text()
        data = data.lower()
        data = data.replace("Jarvis","")
        if float(fuzz.token_set_ratio(data, "your name")) > 80:
            name = "My name is Jarvis"
            text_to_speech(name)
        elif float(fuzz.token_set_ratio(data, "old you")) > 80 or float(fuzz.token_set_ratio(data, "your age")) > 80:
            age = "I am 2 years old, sir"
            text_to_speech(age)
        elif float(fuzz.token_set_ratio(data, "time now")) > 80:
            time = datetime.now().strftime("%I%M%p")
            text_to_speech(time)
        elif float(fuzz.token_set_ratio(data, "open youtube")) > 80:
            address = r"C:\Users\Asus\OneDrive\Desktop\YouTube.lnk"
            if "open" in data:
                os.startfile(address)
            else:
                os.system("taskkill /f /im YouTube.lnk")
        elif float(fuzz.token_set_ratio(data, "joke")) > 50:
            joke = pyjokes.get_joke(language="en", category="neutral")
            print(joke)
            text_to_speech(joke)
        elif float(fuzz.token_set_ratio(data, "play song from my computer")) > 90:
            address = r"C:\Users\Asus\Music"
            listsongraw = os.listdir(address)
            listsong = []
            for song in listsongraw:
                if song.endswith('.mp3'):
                    listsong.append(song)
            rd = listsong[2]
            if "random" in data:
                rd = random.choice(listsong)
            print(listsong)
            os.startfile(os.path.join(address, rd))
        elif float(fuzz.token_set_ratio(data, "open close notepad")) > 60:
            address = r"C:\Windows\System32\notepad.exe"
            if "open" in data:
                os.startfile(address)
            else:
                os.system("taskkill /f /im notepad.exe")
        elif float(fuzz.token_set_ratio(data, "open close cmd command prompt")) > 60:
            if "open" in data:
                os.system("start cmd")
            else:
                os.system("taskkill /f /im cmd.exe")
        elif float(fuzz.token_set_ratio(data, "my ip address")) > 60:
            ip = requests.get("https://api.ipify.org").text
            text_to_speech(ip)
        elif float(fuzz.token_set_ratio(data, "Thank so much Jarvis")) > 60:
            response = "my duty sir, your welcome"
            text_to_speech(response)
        elif float(fuzz.token_set_ratio(data, "open chrome")) > 60:
            text_to_speech("sir, what should I search on chrome?")
            query = speech_to_text()
            webbrowser.open(f"{query}")
        elif float(fuzz.token_set_ratio(data, "wikipedia")) > 60:
            text_to_speech("Searching wikipedia...")
            query = ""
            try:
                query = data.replace("wikipedia","")
            except Exception as e:
                pass
            response = wikipedia.summary(query, sentences = 2)
            text_to_speech("According to wikipedia")
            text_to_speech(response)
        elif float(fuzz.token_set_ratio(data, "open the camera")) > 60:
            cap = cv2.VideoCapture(0)  # 0 for internal cam and 1 for external cam
            while True:
                ret, img = cap.read()
                cv2.imshow('webcam', img)
                k = cv2.waitKey(50)
                if k == 27:
                    break
            cap.release()
            cv2.destroyAllWindows()
        elif float(fuzz.token_set_ratio(data, "jarvis you can go to sleep now")) > 80:
            # if int(datetime.datetime.now().strftime(%I)) > 20:
            #     text_to_speech("Good night sir")
            # else:
            text_to_speech("Thank you sir, have a good day!")
            sys.exit()
        elif float(fuzz.token_set_ratio(data, "send whatsapp message")) > 60:
            pywhatkit.sendwhatmsg("Enter the whatsapp number","This is a testing message for my project.", 18, 16)
        elif float(fuzz.token_set_ratio(data, "play a song on you tube")) > 60:
            text_to_speech("Which song sir?")
            query = speech_to_text()
            if "any song" in query or query == "":
                pywhatkit.playonyt("see you again")
            else:
                pywhatkit.playonyt(query)
        elif float(fuzz.token_set_ratio(data, "send an email")) > 60:
            print("Email: ")
            text_to_speech("sir please enter the mail id")
            mailId = str(input())
            text_to_speech("What should I write in the mail sir?")
            body = speech_to_text()
            text_to_speech("please confirm the message sir")
            confirmation = str(input())
            if confirmation.lower() == 'y' or confirmation.lower() == "yes":
                sendemail(mailId, body)
            else:
                body = confirmation
                sendemail(mailId, body)
        elif float(fuzz.token_set_ratio(data, "shutdown the system laptop"))>90:
            os.system("shutdown /s /t 1")
        elif float(fuzz.token_set_ratio(data, "restart the system laptop"))>90:
            os.system("shutdown /r /t 1")
        elif float(fuzz.token_set_ratio(data, "laptop on sleep"))>80:
            os.system("rundll32.exe powprof.dll,SetSuspendState 0,1,0")
        elif float(fuzz.token_set_ratio(data, "switch the window"))>80:
            pg.keyDown("alt")
            pg.press("tab")
            pg.keyUp("alt")
        elif float(fuzz.token_set_ratio(data, "tell me today's news"))>80:
            text_to_speech("Fetching the news")
            news()
        elif float(fuzz.token_set_ratio(data, "Where I am now"))>80 or float(fuzz.token_set_ratio(data, "what is my location now"))>80 or float(fuzz.token_set_ratio(data, "tell me my location"))>80:
            text_to_speech("checking sir")
            try:
                my_address = requests.get("https://mycurrentlocation.net/")
                time.sleep(2)
                soup = BeautifulSoup(my_address.content, 'html.parser')
                # print(soup)
                g = geocoder.ip('me')
                print(g.latlng)
                latitude = str(g.latlng[0])
                longitude = str(g.latlng[1])
                geolocator = Nominatim(user_agent="geoapiExercises")
                print(latitude," ", longitude)
                location = geolocator.reverse(latitude+","+longitude)
                my_address = location.raw["address"]
                city = my_address.get('city','')
                country = my_address.get('country','')
                state = my_address.get('state','')
                text_to_speech(f"Sir I am not sure but you must be in {city},{state} in {country}")
            except Exception as e:
                print(e)
                text_to_speech("Sorry sir, couldn't find your location")
                q1 = speech_to_text()
                if float(fuzz.token_set_ratio(data, "why"))>80:
                    text_to_speech(e)
        elif float(fuzz.token_set_ratio(data, "take a screenshot"))>80 or float(fuzz.token_set_ratio(data, "capture it"))>80:
            img = pg.screenshot()
            # text_to_speech("name of the image sir")
            date_now = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            name = f"Screenshot {date_now}"
            name = name.replace("/","_")
            name = name.replace(":","_")
            name = name.replace(" ","_")
            print(name)
            img.save(f"C:/Users/Asus/OneDrive/Pictures/Screenshots/{name}.png")
            text_to_speech("screenshot saved sir")
        elif float(fuzz.token_set_ratio(data, "how are you?"))>80:
            text_to_speech("I am good sir, thanks for asking")
        elif data != "":
            data = data.lower()
            data = data.replace("jarvis","")
            webbrowser.open(f"{data}")


    
    # else:
    #     print("Whose this?")


if __name__ == '__main__':
    recognizer = cv2.face.LBPHFaceRecognizer_create() # Local Binary Patterns Histograms
    recognizer.read('trainer/trainer.yml')   #load trained model
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath) #initializing haar cascade for object detection approach

    font = cv2.FONT_HERSHEY_SIMPLEX #denotes the font type


    id = 2 #number of persons you want to Recognize


    names = ['',name]  #names, leave first empty bcz counter starts from 0


    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW) #cv2.CAP_DSHOW to remove warning
    cam.set(3, 640) # set video FrameWidht
    cam.set(4, 480) # set video FrameHeight

    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)

    flag = 1
    x = 1
    while flag:
        if x%5 == 0:
            flag = int(input("Press 1 to recognize your face, else press 0 to terminate the program: "))
        x = x+1
        ret, img =cam.read() #read the frames using the above created object

        converted_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  #The function converts an input image from one color space to another

        faces = faceCascade.detectMultiScale( 
            converted_image,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
        )

        for(x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2) #used to draw a rectangle on any image

            id, accuracy = recognizer.predict(converted_image[y:y+h,x:x+w]) #to predict on every single image

            # Check if accuracy is less them 100 ==> "0" is perfect match 
            if (accuracy < 100):
                id = names[id]
                accuracy = "  {0}%".format(round(100 - accuracy))
                cam.release()
                cv2.destroyAllWindows()
                program()

            else:
                id = "unknown"
                accuracy = "  {0}%".format(round(100 - accuracy))
                text_to_speech("Verification Unsuccessful")
                break
            
            cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(accuracy), (x+5,y+h-5), font, 1, (255,255,0), 1)  
        text_to_speech("Verification Unsuccessful")
        # cv2.imshow('camera',img) 

        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break

    # Do a bit of cleanup
    print("Thanks for using this program, have a good day.")
    cam.release()
    cv2.destroyAllWindows()
