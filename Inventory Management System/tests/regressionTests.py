import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from unitTests import TestBilling
from integrationTests import TestAddEmployee, TestAddSupplierCategoryProduct

def buildSuite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    #Unit tests
    suite.addTests(loader.loadTestsFromTestCase(TestBilling))

    #Integration tests
    suite.addTests(loader.loadTestsFromTestCase(TestAddEmployee))
    suite.addTests(loader.loadTestsFromTestCase(TestAddSupplierCategoryProduct))

    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(buildSuite())