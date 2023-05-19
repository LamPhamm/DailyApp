import kivy

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config

Config.set('graphics', 'resizable', True)
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '700')

class HomePage(Screen):
    pass

class DailyEntryPage(Screen):
    pass


class PastEntriesPage(Screen):
    pass

class WindowManager(ScreenManager):
    pass


class Popup1(FloatLayout):
    pass



kv = Builder.load_file("DailyKvFile.kv")
class myApp(App):
    def build(self):
        return kv
    

if __name__ == "__main__":
    myApp().run()