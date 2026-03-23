# T1. Code Comprehension
pyreverse was used in creating the class diagram and dependency graph: https://pylint.pycqa.org/en/latest/additional_tools/pyreverse/index.html. PlantUML was used in creating the sequence diagram.

## System's architecture
The Inventory Management System is a python based project that uses `tkinter` modules for Graphical User Interface(GUI). The system works around the central dashboard (dashboard.py) that is the main entry point and navigation hub. From the dashboard, the user can navigate to every module except the billing module (This will be implemented in T3). Each module has its own user interface, data validation and direct access to the database via SQLite. The database is initialized with create_db.py, which defines the schema for the tables needed.

## Main components

1. Dashboard (dashboard.py - "IMS" class)
This is the main part of the system and is the main navigation point. It also displays a summary of the total employees, suppliers, categories, products, and sales. It also has a sidebar to launch each module in a new window.

2. Billing (billing.py - billClass)
This module is used during the sale of a product. It displays all the products, lets the user to add a product to the cart, enter the customers details, calculates the total and generates an invoice in text format. It also includes a calculator and a function to print the bill.

3. Category management (category.py -categoryClass)
This module lets the user create or delete categories with a simple id and name. 

4. Database initialization (create_db.py)
This is a script that initializes the database with schemas for the necessary tables if they dont exist already

5. Employee management (employee.py - employeeClass)
This module is for managing the employees. The module lets the user search for an employee using email, name, or contact. The module also lets the user create, update, or delete employees. 

6. Product management (product.py - productClass)
This module is for managing products. The module lets the user search for a product using category, supplier, or name. The module also lets the user create, update, or delete products.

7. Sales (sales.py - salesClass)
This module lets the user view customer bills and also search for them using the invoice number.

8. Supplier Management (supplier.py - supplierClass)
This module is for managing suppliers. The module lets the user search for a supplier using the invoice number. The module also lets the user create, update, or delete suppliers.
