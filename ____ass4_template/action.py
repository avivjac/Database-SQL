import sys
from persistence import repo

def process_action(action: tuple):
    product_id, quantity, activator_id, date = action
    product_id = int(product_id)
    quantity = int(quantity)
    activator_id = int(activator_id)
    date = date  # Keep date as string

    product = repo.products.find(product_id)

    current_quantity = product[3]  # Assuming quantity is the 4th field in the products table

    if quantity > 0:
        # Supply arrival
        new_quantity = current_quantity + quantity
        repo.products.update(product_id, new_quantity)
        repo.activities.insert((product_id, quantity, activator_id, date))

    elif quantity < 0:
        # Sale activity
        if current_quantity + quantity >= 0:
            new_quantity = current_quantity + quantity
            repo.products.update(product_id, new_quantity)
            repo.activities.insert((product_id, quantity, activator_id, date))

def main(args: list[str]):
    inputfilename: str = args[1]
    actions = []
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline: list[str] = line.strip().split(", ")
            actions.append(tuple(splittedline))  # Convert list to tuple

    # Sort actions by date
    actions.sort(key=lambda x: x[3])  # Assuming date is the 4th element in the tuple

    # Process each action
    for action in actions:
        process_action(action)

if __name__ == '__main__':
    main(sys.argv)