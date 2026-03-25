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

# T2. Refactoring

- Changed variable and function naming convention to use lowerCamelCase so that it is consistent across all python files
- Removed unused variables and imports
- Created helpers.py that has helper functions that can be reused for labeling for example
- Added helper function setHeadingsAndColumns and addLabelAndEntry
- Added global font variable in helpers.py

1. dashboard.py
- Simplified button creation for sidebar to use a for loop
- Simplified content creation in dashboard to be in the same for loop
- Made a single function "openModule" that handles all the module openings rather than having multiple functions that essentially do the same thing
- Simplified updateContent function to use for loop

2. billing.py
- Simplified button creation to use for loop so there isnt code duplication
- Added function addLabelAndEntry
- Removed useless self.siscount as it didnt do anything
- Removed useless comments for billTop, billMiddle, and billBottom
- removed unused variable "ev" from getData and getDataCart

3. category.py
- Added correct filepath for images
- Created addImage function to reduce code duplication
- Removed unused variable in getData
- Removed redudant clear statement in delete() function and added to self.varCatId.set("") clear() function

4. employee.py, product.py, supplier.py, category.py
- Cleaned up label and entry creation
- Cleaned up heading and column creation

5. sales.py 
- Fixed the typo in the variable billList (was blllList)

# T3. Adding New Features
The hypothetical stakeholders have said that they want to open the billing module from the dashboard itself. This has now been implemented as a button on the bottom right. 

# T4. Testing and Test Coverage
- Added 3 unit tests in test.py
    - testAddUpdateCart: adds a product to the cart and checks that it is in the cart list
    - testBillUpdate: checks that the bill updates the correct netPay for the items in the cart
    - testPerformCal: Tests that the calculator in billing works as intended

