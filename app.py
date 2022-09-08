
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from datetime import datetime
from kivy.uix.slider import Slider
import time
import threading
#import RPi.GPIO as GPIO

class AlarmApp(GridLayout):
    pin = 5
    clocks = []
    def __init__(self, **kwargs):
        super(AlarmApp, self).__init__(**kwargs)
        self.cols = 2
    
        self.button45 = Button(text='45 min', font_size=14)
        self.button45.bind(on_press=lambda textFile = "bell45.txt": self.callback(textFile))
        self.button30 = Button(text='30 min', font_size=14)
        self.button30.bind(on_press=lambda textFile = "bell30.txt": self.callback(textFile))
        self.buttonCustom = Button(text='custom', font_size=14)
        self.buttonCustom.bind(on_press=lambda textFile = "bellCustom.txt": self.callback(textFile))
        self.add_widget(self.button45)
        self.add_widget(self.button30)
        self.add_widget(self.buttonCustom)

        self.s = Slider(min=2, max=6, value=3, orientation='vertical',value_track=True)
        self.add_widget(self.s)

        #self.fileName = "bell45.txt"
        #self.readFiles(self.fileName)


        #GPIO.setmode(GPIO.BCM)
        #GPIO.setwarnings(False)
        #GPIO.setup(self.pin,GPIO.OUT)

        t1 = threading.Thread(target=self.ring, daemon=True)
        t1.start()

    def readFiles(self, event, txtName):
        with open(txtName) as f:
            self.clocks = f.readlines()
        print("red file : " + txtName)

    def compareTime(self):
        now = datetime.now()
        hours = int(now.strftime("%H"))
        minutes = int(now.strftime("%M"))
        #seconds = now.strftime("%S")
        for line in self.clocks:
            line = line.split(":")
            line[0] = int(line[0])  
            line[1] = int(line[1])

            if (hours == line[0] and minutes == line[1]):
                return True
        return False

    def callback(self, txtFile):
        print('The button is being pressed')
        self.readFiles(txtFile)

    def ring(self):
        print("Thread started")
        while True:
            if(self.compareTime() == True):
                print("zvoni")
                #GPIO.output(self.pin, GPIO.HIGH)
                time.sleep(self.s.value)
                print("ne zvoni")
                #GPIO.output(self.pin, GPIO.LOW)
                time.sleep(60)

class MyApp(App):

    def build(self):
        return AlarmApp()


if __name__ == '__main__':
    MyApp().run()