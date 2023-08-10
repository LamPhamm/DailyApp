import kivy
import datetime
import random
import time
import mysql.connector

#Connect to the database
db=mysql.connector.connect(
host="localhost",
user="Lam",
passwd="water",
database="dailyAppData"
)
myCursor=db.cursor()

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
currDate=""
myToDoList=[]

class DailyEntryPage(Screen,Widget):
    def updateTableHighlightText(self,highlightText):
        #Updates the table each time the highlight is modified
        qHighlightText='UPDATE DailyEntry SET Highlight=%s WHERE Date=%s'
        values=(highlightText,currDate)
        myCursor.execute(qHighlightText,values)
        db.commit()
        myCursor.execute('SELECT * FROM DailyEntry')
        for x in myCursor:
            print(x)

    
    def checkbox_click(self, instance, value):
        def hide_label(dt):
            self.ids.motivation.text=""

        words=["Way to go!","Good job!","Awesome work!","Well done!"]
        ran_num=random.randrange(len(words))

        #Value is true or false depending on if checkbox is checked or not
        if value:
            self.ids.motivation.text=words[ran_num]
            Clock.schedule_once(hide_label, 10)

            userInput=self.ids.DailyHighlightEntry.text
            userInputList=userInput.split()
            
            #Use BS4 to parse through a website to find a related image according to the highlight
            try:
                userInputString='+'.join(userInputList)
                url="https://www.everypixel.com/search?q=" + userInputString
                page=requests.get(url).text
                doc=BeautifulSoup(page,"html.parser")
              

                all_images=doc.find('div',{'class':'content clearfix'})
                image_tags=all_images.find_all('div',{'class':'thumb'})

            except:
                userInputString2='-'.join(userInputList)
                url="https://www.everypixel.com/q/" + userInputString2
                page=requests.get(url).text
                doc=BeautifulSoup(page,"html.parser")
                
           
                all_images=doc.find('div',{'class':'content clearfix'})
                image_tags=all_images.find_all('div',{'class':'thumb'})
            
            myImages=[] #Holds all the image urls of the userInput
            for image in image_tags:
                image_tag=image.find('img')
                image_url=image_tag.get('src')
                myImages.append(image_url)

            #Generate a random image and display it
            ran_num=random.randrange(len(myImages))
           
            self.displayImage = AsyncImage(source=myImages[ran_num])
            self.displayImage.size_hint=0.8,0.2
            self.displayImage.pos_hint= {"top":0.65,'x':0.125}
            self.ids.dailyEntry.add_widget(self.displayImage)


            #Sql statement to update status of highlight column
            qCheckbox='UPDATE DailyEntry SET statusHighlight=%s WHERE Date=%s'
            valuesCheckbox=(True,currDate)

        else:
            self.displayImage.size_hint=0,0 #Remove image by making size 0
            url=None
            qCheckbox='UPDATE DailyEntry SET statusHighlight=%s WHERE Date=%s'
            valuesCheckbox=(False,currDate)

        #Update image sql column
        qImage='UPDATE DailyEntry SET highlightImageLink=%s WHERE Date=%s'
        valuesImage=(url,currDate)
        myCursor.execute(qImage,valuesImage)
        db.commit()

        #Update status sql column
        myCursor.execute(qCheckbox,valuesCheckbox)
        db.commit()

        myCursor.execute('SELECT * FROM DailyEntry')
        for x in myCursor:
            print(x)
    
    
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
        currI=i
        #difficulty with callback(not successful)
        #callback = partial(self.updateText, self.textInput.text)
        #self.textInput.bind(on_text=callback)
        #self.textInput.bind(on_text = lambda x: self.updateText(x, x.text, currI))
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
        #Bind each checkBox widget(successful)
        self.checkBox.bind(on_release = lambda x: self.updateCheckStatus(x, x.active, currI))
        start_y_checkBox-=0.4
        self.ids.scroller.add_widget(self.checkBox)
        myCheckBoxes.append(self.checkBox)

        global myToDoList
        newToDo=[i,"",False]
        myToDoList.append(newToDo)
        print(myToDoList)

    def printCurr(self):
        global i

    

    def updateCheckStatus(self,checkbox,active,currI):
        for item in myToDoList:
            if item[0]==currI:
                item[2]=active
        
        print('myToDoList:',myToDoList)

        
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
currDate=str(datetime.datetime.now())[:10]



qDate='INSERT INTO DailyEntry(Date) SELECT %s WHERE NOT EXISTS (SELECT * FROM DailyEntry WHERE Date=%s)'
values=(currDate,currDate)
myCursor.execute(qDate,values) 
db.commit()


myCursor.execute('SELECT * FROM DailyEntry')
for x in myCursor:
    print(x)

class myApp(App):
    def build(self):
        return kv
    

if __name__ == "__main__":
    myApp().run()