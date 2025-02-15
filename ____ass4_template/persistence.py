import sqlite3
import atexit
from dbtools import Dao
 
# Data Transfer Objects (DTOs)
class Employee(object):
    def __init__(self, id, name, salary, branche_id):
        self.id = id
        self.name = name
        self.salary = salary
        self.branche_id = branche_id

class Supplier(object):
    def __init__(self, id, name, contact_information):
        self.id = id
        self.name = name
        self.contact_information = contact_information

class Product(object):
    def __init__(self, id, description, price, quantity):
        self.id = id
        self.description = description
        self.price = price
        self.quantity = quantity

class Branche(object):
    def __init__(self, id, location, number_of_employees):
        self.id = id
        self.location = location
        self.number_of_employees = number_of_employees

class Activitie(object):
    def __init__(self, product_id, quantity, activator_id, date):
        self.product_id = product_id
        self.quantity = quantity
        self.activator_id = activator_id
        self.date = date
 
 
#Repository
class Repository(object):
    def __init__(self):
        self._conn = sqlite3.connect('bgumart.db')
        # self.cursor = self._conn.cursor()
        self._conn.text_factory = str
        self.branches = self.Branches(self._conn)
        self.suppliers = self.Suppliers(self._conn)
        self.products = self.Products(self._conn)
        self.employees = self.Employees(self._conn)
        self.activities = self.Activities(self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()
 
    def create_tables(self):
        self._conn.executescript("""
            CREATE TABLE employees (
                id              INT         PRIMARY KEY,
                name            TEXT        NOT NULL,
                salary          REAL        NOT NULL,
                branch    INT REFERENCES branches(id)
            );
    
            CREATE TABLE suppliers (
                id                   INTEGER    PRIMARY KEY,
                name                 TEXT       NOT NULL,
                contact_information  TEXT
            );

            CREATE TABLE products (
                id          INTEGER PRIMARY KEY,
                description TEXT    NOT NULL,
                price       REAL NOT NULL,
                quantity    INTEGER NOT NULL
            );

            CREATE TABLE branches (
                id                  INTEGER     PRIMARY KEY,
                location            TEXT        NOT NULL,
                number_of_employees INTEGER
            );
    
            CREATE TABLE activities (
                product_id      INTEGER REFERENCES products(id),
                quantity        INTEGER NOT NULL,
                activator_id    INTEGER NOT NULL,
                date            TEXT    NOT NULL
            );
        """)

    def execute_command(self, script: str) -> list:
        return self._conn.cursor().execute(script).fetchall()
    
    def _close(self):
        self._conn.commit()
        self._conn.close()

    def add_branche(self, branch_id, location, num_employees):
        self.branches.insert((branch_id, location, num_employees))

    def add_supplier(self, supplier_id, name, contact_info):
        self.suppliers.insert((supplier_id, name, contact_info))

    def add_product(self, product_id, description, price, quantity):
        self.products.insert((product_id, description, price, quantity))

    def add_employee(self, employee_id, name, salary, branch_id):
        self.employees.insert((employee_id, name, salary, branch_id))

    def add_activitie(self, product_id, quantity, activator_id, date):
        self.activities.insert((product_id, quantity, activator_id, date))

    class Branches:
        def __init__(self, conn):
            self._conn = conn

        def insert(self, branch):
            self._conn.execute("""
                INSERT INTO branches (id, location, number_of_employees) VALUES (?, ?, ?)
            """, branch)

    class Suppliers:
        def __init__(self, conn):
            self._conn = conn

        def insert(self, supplier):
            self._conn.execute("""
                INSERT INTO suppliers (id, name, contact_information) VALUES (?, ?, ?)
            """, supplier)

    class Products:
        def __init__(self, conn):
            self._conn = conn

        def insert(self, product):
            self._conn.execute("""
                INSERT INTO products (id, description, price, quantity) VALUES (?, ?, ?, ?)
            """, product)

        def find(self, product_id):
            c = self._conn.cursor()
            c.execute("""
                SELECT * FROM products WHERE id = ?
            """, (product_id,))
            return c.fetchone()  

        def update(self, product_id, new_quantity):
            self._conn.execute("""
                UPDATE products SET quantity = ? WHERE id = ?
            """, (new_quantity, product_id))
 

    class Employees:
        def __init__(self, conn):
            self._conn = conn

        def insert(self, employee):
            self._conn.execute("""
                INSERT INTO employees (id, name, salary, branch) VALUES (?, ?, ?, ?)
            """, employee)

    class Activities:
        def __init__(self, conn):
            self._conn = conn

        def insert(self, action):
            self._conn.execute("""
                INSERT INTO activities (product_id, quantity, activator_id, date) VALUES (?, ?, ?, ?)
            """, action)
    

# singleton
repo = Repository()
atexit.register(repo._close)

