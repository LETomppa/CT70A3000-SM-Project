import unittest
import tkinter as tk
from unittest.mock import MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from billing import billClass



class TestBilling(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.bill = billClass.__new__(billClass)
        self.bill.root = self.root
        self.bill.cartList = []
        self.bill.varPid = tk.StringVar()
        self.bill.varPname = tk.StringVar()
        self.bill.varPrice = tk.StringVar()
        self.bill.varQty = tk.StringVar()
        self.bill.varStock = tk.StringVar()
        self.bill.cartTable = MagicMock()
        self.bill.cartTitle = MagicMock()
        self.bill.lblAmnt = MagicMock()
        self.bill.lblNetPay = MagicMock()
        self.bill.varCalInput = tk.StringVar()

    def testAddUpdateCart(self):
        self.bill.varPid.set("productID1")
        self.bill.varPname.set("Test Product")
        self.bill.varPrice.set("10")
        self.bill.varQty.set("1")
        self.bill.varStock.set("10")

        self.bill.addUpdateCart()

        self.assertEqual(len(self.bill.cartList), 1)
        self.assertEqual(self.bill.cartList[0][0], "productID1") # make sure the product ID is correct


    def testBillUpdate(self):
        self.bill.cartList = [["productID1", "Test Product", "10", "2", "10"], ["productID2", "Another Product", "5", "1", "5"]] # id, name, price, quantity, stock

        self.bill.billUpdate()

        self.assertEqual(self.bill.netPay, 23.75)

    def testPerformCal(self):
        
        self.bill.varCalInput.set("1+2")
        self.bill.performCal()
        self.assertEqual(self.bill.varCalInput.get(), "3")

        self.bill.varCalInput.set("1-2")
        self.bill.performCal()
        self.assertEqual(self.bill.varCalInput.get(), "-1")

        self.bill.varCalInput.set("1*2")
        self.bill.performCal()
        self.assertEqual(self.bill.varCalInput.get(), "2")

        self.bill.varCalInput.set("1/2")
        self.bill.performCal()
        self.assertEqual(self.bill.varCalInput.get(), "0.5")
        
if __name__ == '__main__':
    unittest.main()
