from cProfile import label
from fileinput import filename
from subprocess import _TXT
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from datetime import datetime
from kivy.uix.slider import Slider
import time
import threading 

class AlarmApp(GridLayout):

    def __init__(self, **kwargs):
        super(AlarmApp, self).__init__(**kwargs)
        self.cols = 2
 
        self.button45 = Button(text='45 min', font_size=14)
        self.button45.bind(on_press=lambda file = bell45.txt: self.callback(file))
        self.button30 = Button(text='30 min', font_size=14)
        self.button30.bind(on_press=self.callback)
        self.add_widget(self.button45)
        self.s = Slider(min=2, max=6, value=3, orientation='vertical',value_track=True)
        self.add_widget(self.s)

        self.fileName = "bell45.txt"
        self.readFiles(self.fileName)

        t1 = threading.Thread(target=self.check, daemon=True)
        t1.start()

    def readFiles(self, fileName):
        with open(fileName) as f:
            self.lines = f.readlines()
        print("red file" + self.fileName)

    def compareTime(self):
        now = datetime.now()
        hours = int(now.strftime("%H"))
        minutes = int(now.strftime("%M"))
        #seconds = now.strftime("%S")
        for line in self.lines:
            line = line.split(":")
            line[0] = int(line[0])  
            line[1] = int(line[1])

            if (hours == line[0] and minutes == line[1]):
                return True
        return False

    def callback(self, event):
        print('The button is being pressed')
        self.readFiles("bell45.txt")

    def check(self):
        print("Thread started")
        while True:
            if(self.compareTime() == True):
                print("zvoni")
                time.sleep(self.s.value)
                print("ne zvoni")
                time.sleep(59)

class MyApp(App):

    def build(self):
        return AlarmApp()


if __name__ == '__main__':
    MyApp().run()