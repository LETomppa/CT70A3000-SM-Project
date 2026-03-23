The task was to "Generate a class diagram, sequence diagram, and dependency graph" so I am assuming using the pyreverse tool is allowed

pyreverse was used in generating the class diagram and dependency graph: https://pylint.pycqa.org/en/latest/additional_tools/pyreverse/index.html

the command used was "pyreverse -o png -p InventoryManagement billing.py category.py create_db.py dashboard.py employee.py product.py sales.py supplier.py"