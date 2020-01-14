import kivy
kivy.require('1.11.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.recycleview import RecycleView
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup


import sys
sys.path.append(".\\production")
from plan import Plan
from template import Template
from entry import Entry
from miniWidget.minimenu import *

class P(RecycleView):
    def __init__(self,**args):
        super().__init__(**args)
        for i in range(10):
            self.data.append({"text":"hi"})
            print(self.data[i])

class PlanStructureWidget(FloatLayout):
    plan_t = ObjectProperty()
    structure = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.plan = Plan("Heute")

    def addTemplate(self,template:Template):
        temp = self.addToPlan(template)
        self.addToStucture(temp)
     
        return temp

    def addToPlan(self,template):
            temp = self.plan.add(template)
            self.plan_t.text = self.plan.getText()
            return temp

    def addToStucture(self,template):
        index = len(self.structure.data)
        self.structure.data.append({"text":str(index)+" "+template.toString(),
        "on_press": self.getShow_popMenu(index)
        })

    def getShow_popMenu(self,index):
        def showPopMenu():
            temp = self.plan.step_list[index]
            p = PopMenu(temp,on_press=self.getRemoveEntry(index))
            popupWindow = Popup(title=temp.theme,content=p,size_hint=(0.8,0.8))
            popupWindow.open()
        return showPopMenu

    def getRemoveEntry(self,index):
        def removeEntry():
            self.structure.data.pop(index)
            self.removeElement(index)
            self.updateStructureLabels(index)
        return removeEntry

    def updateStructureLabels(self,index):
        i = index
        for e in self.structure.data[index:]:
            e['text'] = str(i) + " " +self.plan.step_list[i].toString()
            e["on_press"] = self.getShow_popMenu(i)
            i+=1

    def removeElement(self,index):
        self.plan.remove(index)
        self.plan_t.text = self.plan.getText()

class PlanStructureApp(App):
    def build(self):
        return P()

if __name__ == "__main__":
    PlanStructureApp().run()
