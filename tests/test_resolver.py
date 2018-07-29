import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pedal.report import *
from pedal.source import set_source
from pedal.tifa import tifa_analysis
from pedal.resolvers import simple
import pedal.sandbox.compatibility as compatibility

class TestCode(unittest.TestCase):

    def test_gently(self):
        clear_report()
        (success, score, category, label, 
         message, data, hide) = simple.resolve()
        self.assertFalse(success)
        self.assertEqual(message, "No errors reported.")
        
        gently('You should always create unit tests.')
        (success, score, category, label, 
         message, data, hide) = simple.resolve()
        self.assertFalse(success)
        self.assertEqual(message, 'You should always create unit tests.')
        
        gently('A boring message that we should not show.')
        (success, score, category, label, 
         message, data, hide) = simple.resolve()
        self.assertFalse(success)
        self.assertEqual(message, 'You should always create unit tests.')
        
        set_success()
        (success, score, category, label, 
         message, data, hide) = simple.resolve()
        self.assertTrue(success)
        self.assertEqual(message, 'You should always create unit tests.')
    
    def test_hidden_error(self):
        clear_report()
        set_source('import pedal')
        tifa_analysis()
        (success, score, category, label, 
         message, data, hide) = simple.resolve()
        self.assertNotEqual(message, "No errors reported.")
    
    def test_unmessaged_tifa(self):
        clear_report()
        set_source('import random\nrandom')
        tifa_analysis()
        (success, score, category, label, 
         message, data, hide) = simple.resolve()
        self.assertEqual(message, "No errors reported.")
    
    def test_premade_exceptions(self):
        try:
            a
        except Exception as e:
            ne = e
        clear_report()
        set_source('a=0\na')
        compatibility.raise_exception(ne)
        (success, score, category, label, 
         message, data, hide) = simple.resolve()
        self.assertEqual(message, "<pre>name 'a' is not defined</pre>\n"+
        "A name error almost always means that you have used a variable before it has a value.  Often this may be a simple typo, so check the spelling carefully.  <br><b>Suggestion: </b>Check the right hand side of assignment statements and your function calls, this is the most likely place for a NameError to be found. It really helps to step through your code, one line at a time, mentally keeping track of your variables.")

if __name__ == '__main__':
    unittest.main(buffer=False)