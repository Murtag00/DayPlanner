import unittest
import sys
sys.path.append('.\\production\\logic')
import CalcTime 
import Load 
from entry import Entry 
from plan import Plan 
from template import Template
import TestHelper
import Change

class Test_Plan(unittest.TestCase):

    test_source = "material\\test\\test_template_1.txt"

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template = Load.loadTemplate(Test_Plan.test_source)


    def test_addToPlan(self):
        p,e = TestHelper.createPlan(self,"ETE")

        step_list = p.step_list
        self.assertEqual(step_list[0].start,Plan.STANDARD_START)
        self.assertEqual(step_list[1].start,CalcTime.addTime(Plan.STANDARD_START,step_list[0].duration))
        self.assertEqual(step_list[2].start,CalcTime.addTime(step_list[1].start,step_list[1].duration))
    
    def test_removeElement(self):
        p = TestHelper.createPlan(self,"TTT")

        self.assertNotEqual(Plan.STANDARD_START,p.step_list[1].start)
        self.assertEqual(3,len(p.step_list))
        end = p.end

        p.remove(0)
        self.assertEqual(Plan.STANDARD_START,p.step_list[0].start)
        self.assertEqual(2,len(p.step_list))
        self.assertNotEqual(end,p.end)

    def test_removeElement(self):
        t1 = self.template.clone()
        t2 = self.template.clone()
 
        p = Plan("Today")
        p.add(t1)
        p.add(self.template)
        p.add(t2)
        
        endBefore = p.end
        p.splitTemplate(1,2)

        self.assertEqual(endBefore,p.end)
        self.assertEqual(len(p.step_list),4)
        self.assertEqual(p.step_list[0].theme,t1.theme)
        self.assertEqual(p.step_list[3].theme,t2.theme)

    def test_pEqual(self):
        p1 = Plan("1")
        p2 = Plan("2")

        p1.add(self.template)
        p2.add(self.template)

        self.assertEqual(p1,p2)
        self.assertNotEqual(id(p1),id(p2))


    def test_update(self):
        #always the same template
        #test as p with 1 templates discover template
        p,e = TestHelper.createPlan(self,"T")
        t_text_1,end = self.template.templateToText(startTime="07:02")
        p.update(t_text_1)
        self.assertEqual(len(p.step_list),1)
        self.assertEqual(p.step_list[0].theme,self.template.theme)

        #test as p with 1 templates discover template+ entry
        p,e = TestHelper.createPlan(self,"T")
        t_text_2 = t_text_1+end+" rofl\n"
        p.update(t_text_2)
        self.assertEqual(p.step_list[0].theme,self.template.theme)
        self.assertEqual(p.step_list[1].theme,"rofl")
        TestHelper.test_listByInstance(self,p.step_list,"2TE")

        text = "07:00 Hallo ich bin Ricke\n"
        t,end = self.template.templateToText(startTime="07:02")
        text = text + t
        text = text + end +" Ich bin heute 15km gelaufen ... ich mache Kickboxen ... Pooldance\n"
        t,end = self.template.templateToText(startTime=CalcTime.addTime(end,"05:00"))
        text = text + t 
        text = text + end +" Nun sind wir zu dritt. Machen wir das Beste draus.\n"

        p,e = TestHelper.createPlan(self,"TT")
        p.update(text)
        TestHelper.test_listByInstance(self,p.step_list,"5ETETE")
    

if __name__ == '__main__': 
    unittest.main()