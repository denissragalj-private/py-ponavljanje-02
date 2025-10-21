# Invoice
class Invoice:
    def __init__(self, invoice_number, invoice_date, due_date, client_name, client_address, items, tax_rate):
        self.invoice_number = invoice_number
        self.invoice_date = invoice_date
        self.due_date = due_date
        self.client_name = client_name
        self.client_address = client_address
        self.items = items
        self.tax_rate = tax_rate
        self.subtotal, self.tax, self.total = self.calculate_totals()

    def calculate_totals(self):
        subtotal = sum(item["quantity"] * item["unit_price"] for item in self.items)
        tax = subtotal * self.tax_rate
        total = subtotal + tax
        return subtotal, tax, total

    def print_invoice(self):
        print(f"Invoice Number: {self.invoice_number}")
        print(f"Invoice Date: {self.invoice_date}")
        print(f"Due Date: {self.due_date}")
        print(f"Bill To: {self.client_name}")
        print(f"Address: {self.client_address}\n")
        print("Items:")
        for item in self.items:
            print(f"- {item['description']}: {item['quantity']} x {item['unit_price']:.2f} €")
        print(f"\nSubtotal: {self.subtotal:.2f} €")
        print(f"Tax (25%): {self.tax:.2f} €")
        print(f"Total: {self.total:.2f} €")

    def add_item(self, description, quantity, unit_price):
        self.items.append({"description": description, "quantity": quantity, "unit_price": unit_price})
        self.subtotal, self.tax, self.total = self.calculate_totals()

    def __str__(self):
        return f"Invoice({self.invoice_number}, Total: {self.total:.2f} €)"






invoice = Invoice(
    invoice_number="INV-1001",
    invoice_date="2024-06-15",
    due_date="2024-07-15",
    client_name="Acme Corporation",
    client_address="123 Business Rd, Business City, BC 54321",
    items=[
        {"description": "Web Design Services", "quantity": 1, "unit_price": 1500.00},
        {"description": "Hosting (12 months)", "quantity": 1, "unit_price": 240.00},
        {"description": "Domain Registration (1 year)", "quantity": 1, "unit_price": 15.00},
    ],
    tax_rate=0.25
)
print('Inoice Total ', invoice.total)
invoice.print_invoice()
invoice.add_item("SEO Services", 5, 300.00)
print(invoice.total)
invoice.print_invoice()


# Invoice

invoices = []  # Lista za cuvanje racuna
invoices.append(invoice)

print(invoices[0])
invoice_1 = Invoice(
    invoice_number="INV-1002",
    invoice_date="2024-06-20",
    due_date="2024-07-20",
    client_name="Beta LLC",
    client_address="456 Commerce St, Trade Town, TT 67890",
    items=[
        {"description": "Consulting Services", "quantity": 2, "unit_price": 800.00},
    ],
    tax_rate=0.25
)
invoices.append(invoice_1)
print(invoices[1])