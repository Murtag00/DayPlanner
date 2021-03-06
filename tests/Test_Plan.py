import unittest
import sys
import os
sys.path.append(os.path.join('./production/logic'))
import CalcTime 
import load 
from entry import Entry 
from plan import Plan 
from routine import Routine
import TestHelper

class Test_Plan(unittest.TestCase):

    test_source = "material/test/test_template_1.txt"

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.routine = load.loadRoutine(Test_Plan.test_source)

    def test_getEntryX(self):
        p,e = TestHelper.createPlan(self,"E2RES")
        e1 = p.getEntryAtIndex(0)
        self.assertEqual(e1,TestHelper.standard)
        e2 = p.getEntryAtIndex(2+len(self.routine.step_list))
        self.assertEqual(e2,TestHelper.besonders)
        e3 = p.getEntryAtIndex(3)
        self.assertEqual(e3,self.routine.step_list[1])



    def test_addToPlan(self):
        p,e = TestHelper.createPlan(self,"ERE")
        step_list = p.step_list
        self.assertEqual(step_list[0].start,Plan.STANDARD_START)
        self.assertEqual(step_list[1].start,CalcTime.addTime(Plan.STANDARD_START,step_list[0].duration))
        self.assertEqual(step_list[2].start,CalcTime.addTime(step_list[1].start,step_list[1].duration))
    
    def test_doesAddingFirstEntryChangeStart(self):
        p = Plan("h")
        p.add(Entry("00:00","h",start="10:00"))
        self.assertEqual(p.start,"10:00")
        p.add(Entry("01:00","h",start="12:00"))
        self.assertEqual(p.end,"11:00")

    def test_removeElement(self):
        p = TestHelper.createPlan(self,"RRR")

        self.assertNotEqual(Plan.STANDARD_START,p.step_list[1].start)
        self.assertEqual(3,len(p.step_list))
        end = p.end

        p.remove(0)
        self.assertEqual(Plan.STANDARD_START,p.step_list[0].start)
        self.assertEqual(2,len(p.step_list))
        self.assertNotEqual(end,p.end)

    def test_removeElement(self):
        r1 = self.routine.clone()
        r2 = self.routine.clone()
 
        p = Plan("Today")
        p.add(r1)
        p.add(self.routine)
        p.add(r2)
        
        endBefore = p.end
        p.splitRoutine(1,2)

        self.assertEqual(endBefore,p.end)
        self.assertEqual(len(p.step_list),4)
        self.assertEqual(p.step_list[0].theme,r1.theme)
        self.assertEqual(p.step_list[3].theme,r2.theme)

    def test_pEqual(self):
        p1 = Plan("1")
        p2 = Plan("2")

        p1.add(self.routine)
        p2.add(self.routine)

        self.assertEqual(p1,p2)
        self.assertNotEqual(id(p1),id(p2))

    
    def test_update(self):
        #always the same routine
        #test as p with 1 routine discover routine
        p,e = TestHelper.createPlan(self,"R")
        t_text_1,end = self.routine.routineToText(startTime="07:02")
        p.update(t_text_1)
        self.assertEqual(len(p.step_list),1)
        self.assertEqual(p.step_list[0].theme,self.routine.theme)

        #test as p with 1 routine discover routine+ entry
        p,e = TestHelper.createPlan(self,"R")
        t_text_2 = t_text_1+end+" rofl\n"
        p.update(t_text_2)
        self.assertEqual(p.step_list[0].theme,self.routine.theme)
        self.assertEqual(p.step_list[1].theme,"rofl")
        TestHelper.test_listByInstance(self,p.step_list,"2RE")

        text = "07:00 Hallo ich bin Ricke\n"
        t,end = self.routine.routineToText(startTime="07:02")
        text +=  t
        text +=  end +" Ich bin heute 15km gelaufen ... ich mache Kickboxen ... Pooldance\n"
        t,end = self.routine.routineToText(startTime=CalcTime.addTime(end,"05:00"))
        text +=  t 
        text +=  end +" Nun sind wir zu dritt. Machen wir das Beste draus.\n"

        p,e = TestHelper.createPlan(self,"RR")
        p.update(text)
        TestHelper.test_listByInstance(self,p.step_list,"5ERERE")

    def test_update2(self):
        p = Plan("today")
        p.update("07:00 aufstehen")
        self.assertEqual(p.step_list[0],Entry("00:00","aufstehen"))

    def test_update3(self):
        p = Plan("today")
        p.update("07:00 aufstehen\n08:00 essen")
        TestHelper.test_listByInstance(self,p.step_list,"1R")
        t = p.step_list[0]
        self.assertEqual(t.step_list[0],Entry("01:00","aufstehen"))
        self.assertEqual(t.step_list[1],Entry("00:00","essen"))
    
    def test_update4(self):
        text = "07:00 aufstehen\n08:00 essen\n09:00 Zaehneputzen"
        p = Plan("today")
        p.update(text)
        TestHelper.test_listByInstance(self,p.step_list,"1R")
        t = p.step_list[0]
        self.assertEqual(t.step_list[0],Entry("01:00","aufstehen"))
        self.assertEqual(t.step_list[1],Entry("01:00","essen"))
        self.assertEqual(t.step_list[2],Entry("00:00","Zaehneputzen"))
    
    def test_update_after_update(self):
        p = Plan("today")
        p.update("07:00 aufstehen\n08:00 essen")
        TestHelper.test_listByInstance(self,p.step_list,"1R")
        t = p.step_list[0]
        self.assertEqual(t.step_list[0],Entry("01:00","aufstehen"))
        self.assertEqual(t.step_list[1],Entry("00:00","essen"))
        
        text = "07:00 aufstehen\n08:00 essen\n09:00 Zaehneputzen"
        p.update(text)
        TestHelper.test_listByInstance(self,p.step_list,"2RE")
        t = p.step_list[0]
        self.assertEqual(t.step_list[0],Entry("01:00","aufstehen"))
        self.assertEqual(t.step_list[1].duration,"01:00")   
        self.assertEqual(p.step_list[1],Entry("00:00","Zaehneputzen"))   

    def test_addAfterUpdate(self):
        p = TestHelper.createPlan(self,"EE")[0]
        duration = p.step_list[0].duration
        e = p.step_list[1].clone()
        p.update(p.getText())
        e2 = p.step_list[0].step_list[1].clone()
        self.assertEqual(e2.duration,"00:00")
        p.update(p.getText()+"\n"+CalcTime.addTime(e.start,duration)+" "+e2.theme)
        
        TestHelper.test_listByInstance(self,p.step_list,"2RE")
        t = p.step_list[0]
        self.assertEqual(t.step_list[0].duration,duration)
        self.assertEqual(t.step_list[1].duration,duration)   
        self.assertEqual(p.step_list[1].duration,"00:00")   

    

if __name__ == '__main__': 
    unittest.main()