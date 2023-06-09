import kivy
import datetime
import random
import time

from bs4 import BeautifulSoup
import requests
import re

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
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
from kivy.uix.image import Image, AsyncImage


from kivy.core.window import Window
Window.size = (400, 700)


class HomePage(Screen):
    pass

#Global Variables
i=0
start_y_label=0.4
start_y_textInput=0.8
start_y_checkBox=0.8
myNumberLabels=[]
myTextInputs=[]
myCheckBoxes=[]

class DailyEntryPage(Screen,Widget):

    def checkbox_click(self, instance, value):
        def hide_label(dt):
            self.ids.motivation.text=""

        words=["Way to go!","Good job!","Awesome work!","Well done!"]
        ran_num=random.randrange(len(words))

        #Value is true or false depending on if checkbox is checked or not
        if value:
            self.ids.motivation.text=words[ran_num]
            Clock.schedule_once(hide_label, 2)

            userInput=self.ids.DailyHighlightEntry.text
            userInputList=userInput.split()
            

            try:
                userInputString='+'.join(userInputList)
                url="https://www.everypixel.com/search?q=" + userInputString
                #print(url)
                page=requests.get(url).text
                doc=BeautifulSoup(page,"html.parser")
              

                all_images=doc.find('div',{'class':'content clearfix'})
                image_tags=all_images.find_all('div',{'class':'thumb'})

            except:
                userInputString2='-'.join(userInputList)
                url="https://www.everypixel.com/q/" + userInputString2
                #print(url)
                page=requests.get(url).text
                doc=BeautifulSoup(page,"html.parser")
                
           
                all_images=doc.find('div',{'class':'content clearfix'})
                image_tags=all_images.find_all('div',{'class':'thumb'})
            
            myImages=[]
            for image in image_tags:
                image_tag=image.find('img')
                image_url=image_tag.get('src')
                myImages.append(image_url)

        
            ran_num=random.randrange(len(myImages))
           
            self.displayImage = AsyncImage(source=myImages[ran_num])
            self.displayImage.size_hint=0.8,0.2
            self.displayImage.pos_hint= {"top":0.65,'x':0.125}
            self.ids.dailyEntry.add_widget(self.displayImage)
        
    
    
  
    def addToDo(self):
        global i, start_y_label, start_y_textInput, start_y_checkBox
        i+=1
      
        #Number label
        self.numberLabel = Label(
            text=str(i) + ".",
            font_size=12,
            pos_hint={"x":-0.4,"y":start_y_label},
            height= 1000,
        )
       
        start_y_label-=0.4
        self.ids.scroller.add_widget(self.numberLabel)
        myNumberLabels.append(self.numberLabel)
        
        #Text input
        self.textInput = TextInput(
            multiline=False,
            size_hint_x=0.6,
            size_hint_y=0.2,
            pos_hint= {"x":0.15,"y":start_y_textInput},
            font_size= 10,
        )
        start_y_textInput-=0.4
        self.ids.scroller.add_widget(self.textInput)
        myTextInputs.append(self.textInput)

        #Checkbox
        self.checkBox=CheckBox(
            active=False,
            pos_hint= {"x":0.9,"y":start_y_checkBox},
            size_hint_x=None,
            size_hint_y=None,
            size= (20,20),
            color=(0,255,255,0.5),
            #on_active= self.checkbox_click(self,active) #PROBLEM calling this function
        )
       
        start_y_checkBox-=0.4
        self.ids.scroller.add_widget(self.checkBox)
        myCheckBoxes.append(self.checkBox)
    
    def displayRemovePopup(self):
        show=DailyEntryPage().RemovePopup()
        popupWindow = Popup(title="Enter a number from 1 to "+str(i), content=show, size_hint=(None,None),size=(220,220),pos_hint={"top":1})
        popupWindow.open()

    class RemovePopup(FloatLayout):
        
        def shiftTasks(self):
            global i, start_y_label, start_y_textInput, start_y_checkBox
            numberInput=self.ids.userInput.text
            
            if numberInput==str(i):
                #Remove element from screen by making size=0 and changing background color
                myNumberLabels[len(myNumberLabels)-1].size_hint=(0,0)
                myTextInputs[len(myTextInputs)-1].size_hint=(0,0)
                myTextInputs[len(myTextInputs)-1].background_color=(0,0,0,1)
                myCheckBoxes[len(myCheckBoxes)-1].size=(0,0)
                myCheckBoxes[len(myCheckBoxes)-1].color=(0,0,0,1)
               
                #Remove element in corresponding lists
                myNumberLabels.pop(len(myNumberLabels)-1)
                myTextInputs.pop(len(myTextInputs)-1)
                myCheckBoxes.pop(len(myCheckBoxes)-1)

                #Reverse the global variables
                i-=1
                start_y_label+=0.4
                start_y_textInput+=0.4
                start_y_checkBox+=0.4
            else:
                myNumberLabels[int(numberInput)-1].size_hint=(0,0)
                myTextInputs[int(numberInput)-1].size_hint=(0,0)
                myTextInputs[int(numberInput)-1].background_color=(0,0,0,1)
                myCheckBoxes[int(numberInput)-1].size=(0,0)
                myCheckBoxes[int(numberInput)-1].color=(0,0,0,1)

                #Shift elements to correct position
                
                for j in range(int(numberInput),len(myNumberLabels)):
                    print(myNumberLabels[j].text)
                    myNumberLabels[j].text=str(int(myNumberLabels[j].text[0])-1)
                    
                    factor=(len(myNumberLabels) - j + 1) * 0.4
                    myNumberLabels[j].pos_hint={"x":-0.4,"y":start_y_label + factor}
                    myTextInputs[j].pos_hint={"x":0.15,"y":start_y_textInput + factor}
                    myCheckBoxes[j].pos_hint={"x":0.9,"y":start_y_checkBox + factor}
                
                #Remove element in corresponding lists
                myNumberLabels.pop(int(numberInput)-1)
                myTextInputs.pop(int(numberInput)-1)
                myCheckBoxes.pop(int(numberInput)-1)

                i-=1
                start_y_label+=0.4
                start_y_textInput+=0.4
                start_y_checkBox+=0.4

                
class PastEntriesPage(Screen):
    pass

class WindowManager3(ScreenManager):
    pass
   

class Navigation(Screen,FloatLayout):
    pass

kv = Builder.load_file("DailyKvFile.kv")
class myApp(App):
    def build(self):
        return kv
    

if __name__ == "__main__":
    myApp().run()