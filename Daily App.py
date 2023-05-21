import kivy
import datetime
import random
import time

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
from kivy.uix.checkbox import CheckBox
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout


from kivy.core.window import Window
Window.size = (400, 700)

'''
Config.set('graphics', 'resizable', True)
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '700')'''


class HomePage(Screen):
    pass


class DailyEntryPage(Screen,Widget):
    
    # Callback for the checkbox
    def checkbox_click(self, instance, value):
        def hide_label(dt):
            self.ids.motivation.text=""

        words=["Way to go!","Good job!","Awesome work!","Well done!"]
        ran_num=random.randrange(len(words))

        #Value is true or false depending on if checkbox is checked or not
        if value:
            self.ids.motivation.text=words[ran_num]
            Clock.schedule_once(hide_label, 2)
            
        else:
            self.ids.motivation.text=""

    i=1
    start_y_label=0.4
    start_y_textInput=0.8
    start_y_checkBox=0.8
    def addToDo(self):
        
        #Number label
        numberLabel = Label(
            text=str(self.i) + ".",
            font_size=12,
            pos_hint={"x":-0.4,"y":self.start_y_label},
            
        )
      
        self.i+=1
        self.start_y_label-=0.4
        self.ids.scroller.add_widget(numberLabel)
        
        
        #Text input
        textInput = TextInput(
            multiline=False,
            size_hint_x=0.6,
            size_hint_y=0.2,
            pos_hint= {"x":0.15,"y":self.start_y_textInput},
            font_size= 10,
        )
        self.start_y_textInput-=0.4
        self.ids.scroller.add_widget(textInput)

        #Checkbox
        checkBox=CheckBox(
            active=False,
            pos_hint= {"x":0.9,"y":self.start_y_checkBox},
            size_hint_x=None,
            size_hint_y=None,
            size= (20,20),
            color=(0,255,255,0.5),
            #on_active= self.checkbox_click(self,active) #PROBLEM calling this function
        )
       
        self.start_y_checkBox-=0.4
        self.ids.scroller.add_widget(checkBox)
        


class PastEntriesPage(Screen):
    pass

class WindowManager(ScreenManager):
    pass






kv = Builder.load_file("DailyKvFile.kv")
class myApp(App):
    def build(self):
        return kv
    

if __name__ == "__main__":
    myApp().run()