# Invoice
def calculate_totals(items, tax_rate):
    # duzi nacin zapisa sum(item["quantity"] * item["unit_price"] for item in items)
    # subtotal = 0
    # for item in items:
    #     item_total_price = item["quantity"] * item["unit_price"]
    #     subtotal += item_total_price
    subtotal = sum(item["quantity"] * item["unit_price"] for item in items)
    tax = subtotal * tax_rate
    total = subtotal + tax
    return subtotal, tax, total

def print_invoice(invoice_number,
                  invoice_date,
                  due_date,
                  client_name,
                  client_address,
                  items,
                  subtotal,
                  tax,
                  total):
    print(f"Invoice Number: {invoice_number}")
    print(f"Invoice Date: {invoice_date}")
    print(f"Due Date: {due_date}")
    print(f"Bill To: {client_name}")
    print(f"Address: {client_address}\n")
    print("Items:")
    for item in items:
        print(f"- {item['description']}: {item['quantity']} x {item['unit_price']:.2f} €")
    print(f"\nSubtotal: {subtotal:.2f} €")
    print(f"Tax (25%): {tax:.2f} €")
    print(f"Total: {total:.2f} €")

invoice_number = "INV-1001"
invoice_date = "2024-06-15"
due_date = "2024-07-15"
client_name = "Acme Corporation"
client_address = "123 Business Rd, Business City, BC 54321"
items = [
    {"description": "Web Design Services", "quantity": 1, "unit_price": 1500.00},
    {"description": "Hosting (12 months)", "quantity": 1, "unit_price": 240.00},
    {"description": "Domain Registration (1 year)", "quantity": 1, "unit_price": 15.00},
]
tax_rate = 0.25  # 25% sales tax

subtotal, tax, total = calculate_totals(items, tax_rate)

print_invoice(invoice_number,
              invoice_date,
              due_date,
              client_name,
              client_address,
              items,
              subtotal,
              tax,
              total)

# Invoice

# TODO Dodati listu racuna
invoices = []  # Lista za cuvanje racuna
invoices.append(invoice_number)
invoices.append(invoice_date)
invoices.append(due_date)
invoices.append(client_name)
invoices.append(client_address)
invoices.append(items)
invoices.append(items)
invoices.append(subtotal)
invoices.append(tax)
invoices.append(total)

print(invoices[2])