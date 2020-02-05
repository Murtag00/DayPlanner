from kivy.uix.popup import Popup

try:
    from .pop.popmenu import PopMenu
except:
    from pop.popmenu import PopMenu
    
class FunctionManager(): 
    def __init__(self,plan,updateEntryListLabels,splitTemplate,removeElement):
        self.plan = plan
        self.source = plan
        self.updateEntryListLabels = updateEntryListLabels
        self.splitTemplate = splitTemplate
        self.removeElement = removeElement

    def get_renameTemplate(self,temp_index):
        def renameTemplate(new_name):
            self.plan.step_list[temp_index].theme = new_name
            self.updateEntryListLabels(0)
        return renameTemplate

    def _getShow_popMenu(self,index):
        def showPopMenu():
            temp= self.source.step_list[index]
            pM = PopMenu()
            pW = Popup(title=temp.theme,content=pM,size_hint=(0.8,0.8))
            
            pM.addEntries(temp)
            pM.addDeleteFunction(self._getRemoveEntry(index,dismiss_func=pW.dismiss))
            pM.addSplitFunction(self._get_get_splitFunc(index,dismiss_func=pW.dismiss))
            pM.addRename(self.get_renameTemplate(index))

            pW.open()
        return showPopMenu

    def _getRemoveEntry(self,index,dismiss_func=None):
        def removeEntry():
            self.removeElement(index)
            if not dismiss_func==None:
                dismiss_func()
        return removeEntry

    def _get_get_splitFunc(self,template_index,dismiss_func=None):
        def get_splitFunc(entry_index):
            def splitFunc():
                self.splitTemplate(template_index,entry_index)
                if not dismiss_func== None:
                    dismiss_func()
            return splitFunc
        return get_splitFunc