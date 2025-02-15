from persistence import *

import sys
import os

def add_branche(splittedline : list[str]):
    branch_id, location, num_employees = splittedline
    repo.add_branche(int(branch_id), location, int(num_employees))

def add_supplier(splittedline : list[str]):
    supplier_id, name, contact_info = splittedline
    repo.add_supplier(int(supplier_id), name, contact_info)

def add_product(splittedline : list[str]):
    product_id, description, price, quantity = splittedline
    repo.add_product(int(product_id), description, float(price), int(quantity))

def add_employee(splittedline : list[str]):
    employee_id, name, salary, branch_id = splittedline
    repo.add_employee(int(employee_id), name, float(salary), int(branch_id))

adders = {  "B": add_branche,
            "S": add_supplier,
            "P": add_product,
            "E": add_employee}

def main(args : list[str]):
    inputfilename = args[1]
    # delete the database file if it exists
    repo._close()
    # uncomment if needed
    if os.path.isfile("bgumart.db"):
         os.remove("bgumart.db")


    repo.__init__()
    repo.create_tables()
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline : list[str] = line.strip().split(",")
            adders.get(splittedline[0])(splittedline[1:])

if __name__ == '__main__':
    main(sys.argv)