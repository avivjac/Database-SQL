from persistence import *




def print_table_data():
    # Print Activities table ordered by date
    print("Activities")
    activities = repo.execute_command("SELECT * FROM activities ORDER BY date")
    for row in activities:
        print(row)

    # Print Branches table ordered by id
    print("Branches")
    branches = repo.execute_command("SELECT * FROM branches ORDER BY id")
    for row in branches:
        print(row)

    # Print Employees table ordered by id
    print("Employees")
    employees = repo.execute_command("SELECT * FROM employees ORDER BY id")
    for row in employees:
        print(row)

    # Print Products table ordered by id
    print("Products")
    products = repo.execute_command("SELECT * FROM products ORDER BY id")
    for row in products:
        print(row)

    # Print Suppliers table ordered by id
    print("Suppliers")
    suppliers = repo.execute_command("SELECT * FROM suppliers ORDER BY id")
    for row in suppliers:
        print(row)

def print_employee_report():
    # Detailed report of employees
    print("Employees report")
    employees_report = repo.execute_command("""
        SELECT e.name, e.salary, b.location, SUM(a.quantity * p.price * -1)
        FROM employees e
        LEFT JOIN branches b ON e.branch = b.id
        LEFT JOIN activities a ON a.activator_id = e.id
        LEFT JOIN products p ON a.product_id = p.id
        GROUP BY e.id
        ORDER BY e.name
    """)

    for row in employees_report:
        if row[3] is None:
            print(f"{row[0]} {row[1]} {row[2]}" + " 0")
        else:
            print(f"{row[0]} {row[1]} {row[2]} {row[3]}")


def print_activitie_report():
    # Detailed report of activities
    print("Activities report")
    activities_report = repo.execute_command("""
        SELECT a.date, p.description, a.quantity, e.name, s.name
        FROM activities a
        LEFT JOIN products p ON a.product_id = p.id
        LEFT JOIN employees e ON a.activator_id = e.id
        LEFT JOIN suppliers s ON a.activator_id = s.id
        ORDER BY a.date
    """)

    for row in activities_report:
        print(row)

        
def main():
     # Print the database tables
    print_table_data()
    
    # Print detailed employee report
    print_employee_report()

    # Print detailed activity report
    print_activitie_report()

if __name__ == '__main__':
    main()