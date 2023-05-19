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

Config.set('graphics', 'resizable', True)
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '700')

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