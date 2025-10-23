
class Invoice:
    def __init__(self, invoice_number, invoice_date, due_date, client, items=[], tax_rate=0.25):
        self.id = 1
        self.invoice_number = invoice_number
        self.invoice_date = invoice_date
        self.due_date = due_date
        self.client = client
        self.items = items
        self.tax_rate = tax_rate
        self.subtotal, self.tax, self.total = self.calculate_totals()
        self.qr_code = 'Ovo je QR Code'  # Placeholder for QR code generation

    def calculate_totals(self):
        subtotal = sum(item.total_price for item in self.items)
        tax = subtotal * self.tax_rate
        total = subtotal + tax
        return subtotal, tax, total

    def print_invoice(self):
        print(f"Invoice Number: {self.invoice_number}")
        print(f"Invoice Date: {self.invoice_date}")
        print(f"Due Date: {self.due_date}")
        print(f"Bill To: {self.client}")
        print(f"Address: {self.client.postal_address}\n")
        print(f"Emil: {self.client.email}\n")
        print(f"Phone: {self.client.phone}\n")
        print("Items:")
        for item in self.items:
            print(item)
        print(f"\nSubtotal: {self.subtotal:.2f} €")
        print(f"Tax (25%): {self.tax:.2f} €")
        print(f"Total: {self.total:.2f} €")

    def add_item(self, item):
        self.items.append(item)
        self.subtotal, self.tax, self.total = self.calculate_totals()

    def __str__(self):
        return f"Invoice({self.invoice_number}, Total: {self.total:.2f} €)"