import cv2
import pyttsx3
import random as r
import time

time.sleep(2)

# list containing images of all animal faces
animal_faces = ["cat_1.jpg", "cat_2.jpg", "cat_3.jpg", "cat_4.jpg", "cat_5.jpg",
                "dog_1.jpg", "dog_2.jpg", "dog_3.jpg", "dog_4.jpg", "dog_5.jpeg"]

# list containing strings of all jokes
jokes = []
with open("jokes_list.txt", "r") as joke_file:
    for joke in joke_file.read().split("\n"):
        jokes.append(joke)

engine = pyttsx3.init() # creating object

# function for speech
def talk(message):
    engine.say(str(message))
    engine.runAndWait()
    engine.stop()

# function for showing a random animal picture
def show_animal():
    animal_image = cv2.imread(animal_faces[r.randint(0, len(animal_faces) - 1)], 1)
    cv2.imshow("Cute Animal", animal_image)
    cv2.moveWindow("Cute Animal", 20, 20)
    cv2.waitKey(1)
    time.sleep(1)

# function for selecting and telling random joke
def random_joke():
    joke = jokes[r.randint(0, len(jokes) - 1)]
    talk(joke)

# defining cascades
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
smile_cascade = cv2.CascadeClassifier("haarcascade_smile.xml")

# accessing webcam
web_cam = cv2.VideoCapture(0)

# function for the detection of faces and smiles
def smile_detect(wait_time):
    stop_counter = 0
    while wait_time >= stop_counter:
        success, video_image = web_cam.read()
        grayscale_image = cv2.cvtColor(video_image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(grayscale_image, 1.1, 35)
        for (x, y, w, h) in faces:
            cv2.rectangle(video_image, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.putText(video_image, "FACE", (x, y), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            smiles = smile_cascade.detectMultiScale(grayscale_image, 1.3, 45)
            for (xx, yy, ww, hh) in smiles:
                if (x < xx < x + w) and (y < yy , y + h):
                    cv2.rectangle(video_image, (xx, yy), (xx + ww, yy + hh), (255, 255, 0), 2)
                    cv2.putText(video_image, "SMILE", (xx, yy + hh + 32), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                    return True
        cv2.imshow("Smile Detection", video_image)
        cv2.moveWindow("Smile Detection", 600, 250)
        stop_counter += 1
        cv2.waitKey(1)

while True:
    currently_smiling = smile_detect(20)
    if (currently_smiling):
        talk("You seem happy, as a reward I'll be showing you a picture of a cute animal")
        show_animal()
        time.sleep(1)
        cv2.destroyAllWindows()
    else:
        talk("You don't seem happy enough, let me tell you a joke, and if you end up smiling then you will get a reward")
        random_joke()