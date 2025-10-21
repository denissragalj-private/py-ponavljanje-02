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

def print_invoice(invoice):
    print(f"Invoice Number: {invoice["invoice_number"]}")
    print(f"Invoice Date: {invoice["invoice_date"]}")
    print(f"Due Date: {invoice["due_date"]}")
    print(f"Bill To: {invoice["client_name"]}")
    print(f"Address: {invoice["client_address"]}\n")
    print("Items:")
    for item in invoice["items"]:
        print(f"- {item['description']}: {item['quantity']} x {item['unit_price']:.2f} €")
    print(f"\nSubtotal: {invoice["subtotal"]:.2f} €")
    print(f"Tax (25%): {invoice["tax"]:.2f} €")
    print(f"Total: {invoice["total"]:.2f} €")


invoice = {
    "invoice_number": "INV-1001",
    "invoice_date": "2024-06-15",
    "due_date": "2024-07-15",
    "client_name": "Acme Corporation",
    "client_address": "123 Business Rd, Business City, BC 54321",
    "items": [
        {"description": "Web Design Services", "quantity": 1, "unit_price": 1500.00},
        {"description": "Hosting (12 months)", "quantity": 1, "unit_price": 240.00},
        {"description": "Domain Registration (1 year)", "quantity": 1, "unit_price": 15.00},
    ],
    "tax_rate": 0.25
}
invoice["subtotal"], invoice["tax"], invoice["total"] = calculate_totals(invoice["items"], invoice["tax_rate"])


print_invoice(invoice)

# Invoice

# TODO Dodati listu racuna
invoices = []  # Lista za cuvanje racuna
invoices.append(invoice)

print(invoices[0])

invoice_1 = {
    "invoice_number": "INV-1002",
    "invoice_date": "2024-06-20",
    "due_date": "2024-07-20",
    "client_name": "Beta LLC",
    "client_address": "456 Commerce St, Trade Town, TT 67890",
    "items": [
        {"description": "Consulting Services", "quantity": 2, "unit_price": 800.00},
        {"description": "Software License", "quantity": 3, "unit_price": 200.00},
    ],
    "tax_rate": 0.25
}
invoice_1["subtotal"], invoice_1["tax"], invoice_1["total"] = calculate_totals(invoice_1["items"], invoice_1["tax_rate"])

invoices.append(invoice_1)

print(invoices[1])