import unittest
import sys
sys.path.append('.\\production\\logic')
import Load


class Test_Load(unittest.TestCase):

    test_source = "material\\test\\"

    def Load(self):
        Load.loadTemplateDir(self.test_source)


if __name__ == '__main__':
    unittest.main()