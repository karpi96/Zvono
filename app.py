
from fileinput import filename
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from datetime import datetime
from kivy.uix.slider import Slider
import time
import threading
import RPi.GPIO as GPIO
from kivy.core.window import Window


class AlarmApp(GridLayout):
    pin = 5
    clocks = []
    def __init__(self, **kwargs):
        super(AlarmApp, self).__init__(**kwargs)
        self.cols = 3
    
        self.button45 = Button(text='45 min', font_size=14)
        self.button45.bind(on_press=self.callback45)
        self.button30 = Button(text='30 min', font_size=14)
        self.button30.bind(on_press=self.callback30)
        self.buttonCustom = Button(text='custom', font_size=14)
        self.buttonCustom.bind(on_press=self.callbackCustom)
        self.buttonExit = Button(text='exit', font_size=14)
        self.buttonExit.bind(on_press=self.callbackExit)
        self.add_widget(self.button45)
        self.add_widget(self.button30)
        self.add_widget(self.buttonCustom)
        self.add_widget(self.buttonExit)


        self.bellTime = Slider(min=3, max=10, value=5, orientation='vertical',value_track=True)
        
        self.add_widget(self.bellTime)
        self.bellTime.bind(value = self.changeLabel)


        self.fileName = "bell45.txt"
        self.readFiles(self.fileName)

        self.lbl = Label(text=("aktivno: " + "45 minuta" + "\n  duzina zvona: " + str(self.bellTime.value)) + "s")

        self.add_widget(self.lbl)

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin,GPIO.OUT)

        t1 = threading.Thread(target=self.ring, daemon=True)
        t1.start()

    def changeLabel(self, instance, event):
        self.lbl.text ="active file: " + self.fileName + "\n  duzina zvona: " + str(round(self.bellTime.value,2)) + "s"


    def callbackExit(self, event):
        App.get_running_app().stop()
        # removing window
        Window.close()

    def readFiles(self, txtName):
        with open(txtName) as f:
            self.clocks = f.readlines()
        print("read file : " + txtName)

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

    def callback30(self, event):
        print('The button is being pressed')
        self.fileName = "bell30.txt"
        self.readFiles(self.fileName)
        self.lbl.text ="aktivno: " + "45 minuta" +"\n  duzina zvona: " + str(round(self.bellTime.value,2)) + "s"


    def callback45(self, event):
        print('The button is being pressed')
        self.fileName = "bell45.txt"
        self.readFiles(self.fileName)
        self.lbl.text ="aktivno: "+ "30 minuta" +"\n  duzina zvona: " + str(round(self.bellTime.value,2)) + "s"

    
    def callbackCustom(self, event):
        print('The button is being pressed')
        self.fileName = "bellCustom.txt"
        self.readFiles(self.fileName)
        self.lbl.text ="aktivno: " + "van standarda" +"\n  duzina zvona: " + str(round(self.bellTime.value,2)) + "s"
    
    def ring(self):
        print("Thread started")
        while True:
            if(self.compareTime() == True):
                print("zvoni")
                GPIO.output(self.pin, GPIO.HIGH)
                time.sleep(self.bellTime.value)
                print("ne zvoni")
                GPIO.output(self.pin, GPIO.LOW)
                time.sleep(60)

class MyApp(App):

    def build(self):
        return AlarmApp()


if __name__ == '__main__':
    Window.fullscreen = 'auto'
    MyApp().run()
