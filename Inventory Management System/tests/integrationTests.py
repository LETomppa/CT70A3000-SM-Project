import unittest
import sqlite3
import tkinter as tk
from unittest.mock import MagicMock, patch
import sys
import os
import tempfile
import warnings

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass

def createTestDb():
    # Create a temporary database with all tables needed for the integration tests
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT,name text,email text,gender text,contact text,dob text,doj text,pass text,utype text,address text,salary text)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS supplier(invoice INTEGER PRIMARY KEY AUTOINCREMENT,name text,contact text,desc text)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS category(cid INTEGER PRIMARY KEY AUTOINCREMENT,name text)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS product(pid INTEGER PRIMARY KEY AUTOINCREMENT,Category text, Supplier text,name text,price text,qty text,status text)")
    con.commit()
    con.close()
    os.close(db_fd)
    return db_path

class TestAddEmployee(unittest.TestCase):
    # Scenario: Adding an employee saves it to the database and refreshes the table, then adds another employee and checks the database again

    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        self.root = tk.Tk()
        self.root.withdraw()
        self.emp = employeeClass.__new__(employeeClass)
        self.emp.root = self.root
        self.emp.varEmpId = tk.StringVar()
        self.emp.varName = tk.StringVar()
        self.emp.varEmail = tk.StringVar()
        self.emp.varGender = tk.StringVar()
        self.emp.varContact = tk.StringVar()
        self.emp.varDob = tk.StringVar()
        self.emp.varDoj = tk.StringVar()
        self.emp.varPass = tk.StringVar()
        self.emp.varUtype = tk.StringVar()
        self.emp.varSalary = tk.StringVar()
        self.emp.varSearchby = tk.StringVar()
        self.emp.varSearchtxt = tk.StringVar()
        self.emp.txtAddress = MagicMock()
        self.emp.txtAddress.get.return_value = "Test Address"
        self.emp.employeeTable = MagicMock()

        self.db_path = createTestDb()

    def testAddEmployeeSavesToDatabase(self):
        #Add employee
        self.emp.varEmpId.set("1")
        self.emp.varName.set("Bob")
        self.emp.varEmail.set("bob@test.com")
        self.emp.varGender.set("Male")
        self.emp.varContact.set("1234567890")
        self.emp.varDob.set("1.1.2000")
        self.emp.varDoj.set("1.1.2026")
        self.emp.varPass.set("password")
        self.emp.varUtype.set("Employee")
        self.emp.varSalary.set("10000")

        real_connect = sqlite3.connect
        with patch('helpers.sqlite3.connect', side_effect=lambda *a, **kw: real_connect(self.db_path)), \
             patch('helpers.messagebox'), \
             patch('employee.messagebox'):
            self.emp.add()

        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute("SELECT name, email, salary FROM employee WHERE eid=1")
        row = cur.fetchone()
        con.close()

        self.assertIsNotNone(row)
        self.assertEqual(row[0], "Bob")
        self.assertEqual(row[1], "bob@test.com")
        self.assertEqual(row[2], "10000")

        #Adding another employee
        self.emp.varEmpId.set("2")
        self.emp.varName.set("Alice")
        self.emp.varEmail.set("alice@test.com")
        self.emp.varGender.set("Female")
        self.emp.varContact.set("0987654321")
        self.emp.varDob.set("2.2.2000")
        self.emp.varDoj.set("2.2.2026")
        self.emp.varPass.set("password")
        self.emp.varUtype.set("Employee")
        self.emp.varSalary.set("20000")

        with patch('helpers.sqlite3.connect', side_effect=lambda *a, **kw: real_connect(self.db_path)), \
             patch('helpers.messagebox'), \
             patch('employee.messagebox'):
            self.emp.add()

        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute("SELECT name, email, salary FROM employee WHERE eid=2")
        row = cur.fetchone()
        con.close()

        self.assertIsNotNone(row)
        self.assertEqual(row[0], "Alice")
        self.assertEqual(row[1], "alice@test.com")
        self.assertEqual(row[2], "20000")


class TestAddSupplierCategoryProduct(unittest.TestCase):
    # Scenario: Adding a supplier, a category, and then a product that uses both, then checking the database that everything was saved correctly

    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        self.root = tk.Tk()
        self.root.withdraw()

        #Supplier
        self.sup = supplierClass.__new__(supplierClass)
        self.sup.root = self.root
        self.sup.varSupInvoice = tk.StringVar()
        self.sup.varName = tk.StringVar()
        self.sup.varContact = tk.StringVar()
        self.sup.varSearchtxt = tk.StringVar()
        self.sup.txtDesc = MagicMock()
        self.sup.txtDesc.get.return_value = "Test Description"
        self.sup.supplierTable = MagicMock()

        #Category
        self.cat = categoryClass.__new__(categoryClass)
        self.cat.root = self.root
        self.cat.varName = tk.StringVar()
        self.cat.varCatId = tk.StringVar()
        self.cat.categoryTable = MagicMock()

        #Product
        self.prod = productClass.__new__(productClass)
        self.prod.root = self.root
        self.prod.varCat = tk.StringVar()
        self.prod.varSup = tk.StringVar()
        self.prod.varName = tk.StringVar()
        self.prod.varPrice = tk.StringVar()
        self.prod.varQty = tk.StringVar()
        self.prod.varStatus = tk.StringVar()
        self.prod.varPid = tk.StringVar()
        self.prod.varSearchby = tk.StringVar()
        self.prod.varSearchtxt = tk.StringVar()
        self.prod.productTable = MagicMock()

        self.db_path = createTestDb()

    def testAddSupplierCategoryProduct(self):
        real_connect = sqlite3.connect

        #Add supplier
        self.sup.varSupInvoice.set("1")
        self.sup.varName.set("Test Supplier")
        self.sup.varContact.set("1234567890")

        with patch('helpers.sqlite3.connect', side_effect=lambda *a, **kw: real_connect(self.db_path)), \
             patch('helpers.messagebox'), \
             patch('supplier.messagebox'):
            self.sup.add()

        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute("SELECT name, contact FROM supplier WHERE invoice=1")
        row = cur.fetchone()
        con.close()

        self.assertIsNotNone(row)
        self.assertEqual(row[0], "Test Supplier")
        self.assertEqual(row[1], "1234567890")

        #Add category
        self.cat.varName.set("Test Category")

        with patch('helpers.sqlite3.connect', side_effect=lambda *a, **kw: real_connect(self.db_path)), \
             patch('helpers.messagebox'), \
             patch('category.messagebox'):
            self.cat.add()

        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute("SELECT name FROM category WHERE cid=1")
        row = cur.fetchone()
        con.close()

        self.assertIsNotNone(row)
        self.assertEqual(row[0], "Test Category")

        #Add product
        self.prod.varCat.set("Test Category")
        self.prod.varSup.set("Test Supplier")
        self.prod.varName.set("Test Product")
        self.prod.varPrice.set("100")
        self.prod.varQty.set("100")
        self.prod.varStatus.set("Active")

        with patch('helpers.sqlite3.connect', side_effect=lambda *a, **kw: real_connect(self.db_path)), \
             patch('helpers.messagebox'), \
             patch('product.messagebox'):
            self.prod.add()

        #Check that the product was added correctly
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute("SELECT Category, Supplier, name, price, qty FROM product WHERE pid=1")
        row = cur.fetchone()
        con.close()

        self.assertIsNotNone(row)
        self.assertEqual(row[0], "Test Category")
        self.assertEqual(row[1], "Test Supplier")
        self.assertEqual(row[2], "Test Product")
        self.assertEqual(row[3], "100")
        self.assertEqual(row[4], "100")


if __name__ == '__main__':
    unittest.main()
    
