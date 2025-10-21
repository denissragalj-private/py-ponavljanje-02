



class Client:
    def __init__(self, first_name, last_name, postal_address, email, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.postal_address = postal_address
        self.email = email
        self.phone = phone
        self.invoices = []
        self.total_invoices_amount = 0.0

    def add_invoice(self, invoice):
        # Napraviti provjeru dobivenih podataka!!! I samo ako je sve OK, dodati fakturu
        self.invoices.append(invoice)
        self.calculate_total_invoices_amount()
        # Opcija: Posalji notifikaciju klijentu o novoj fakturi (email, SMS, push notifikacija...)

    def calculate_total_invoices_amount(self):
        self.total_invoices_amount = sum(invoice.total for invoice in self.invoices)
        return self.total_invoices_amount

    def __str__(self):
        return f"Client({self.first_name} {self.last_name}, {self.postal_address}, {self.email}, {self.phone})"


class PostalAddress:
    def __init__(self, street, house_number, postal_code, city, country):
        self.street = street
        self.house_number = house_number
        self.postal_code = postal_code
        self.city = city
        self.country = country

    def __str__(self):
        return f"{self.street} {self.house_number}, {self.postal_code} {self.city}, {self.country}"


class Email:
    def __init__(self, email_address, email_type):
        self.email_address = email_address
        self.email_type = email_type

    def __str__(self):
        return f"{self.email_address} ({self.email_type})"


class Invoice:
    def __init__(self, invoice_number, invoice_date, due_date, client, items=[], tax_rate=0.25):
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


class InvoiceItem:
    def __init__(self, description, quantity, unit_price):
        self.description = description
        self.quantity = quantity
        self.unit_price = unit_price
        self.total_price = self.calcualte_total_price()

    def calcualte_total_price(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"- {self.description}, {self.quantity} x {self.unit_price:.2f} €, Total: {self.total_price:.2f} €"






















postal_address = PostalAddress("Ulica Primjera", "10A", "10000", "Zagreb", "Hrvatska")
email_address = Email("pero@email.com", "Work")
pero_peric = Client("Pero", "Peric", postal_address, email_address, "+38591234567")


invoice = Invoice(
    invoice_number="INV-1001",
    invoice_date="2024-06-15",
    due_date="2024-07-15",
    client=pero_peric,
    items=[
        InvoiceItem(description="Web Design Services", quantity=1, unit_price=1500.00),
        InvoiceItem(description="Hosting (12 months)", quantity=1, unit_price=240.00),
        InvoiceItem(description="Domain Registration (1 year)", quantity=1, unit_price=15.00)
    ],
    tax_rate=0.25
)
pero_peric.add_invoice(invoice)
invoice.add_item(InvoiceItem("SEO Services", 5, 300.00))


invoice_1 = Invoice(
    invoice_number="INV-1002",
    invoice_date="2024-06-20",
    due_date="2024-07-20",
    client=pero_peric,
    items=[
        InvoiceItem(description="Consulting Services", quantity=2, unit_price=800.00)
    ],
    tax_rate=0.25
)
pero_peric.add_invoice(invoice_1)


for invoice in pero_peric.invoices:
    invoice.print_invoice()
    print("\n" + "="*40 + "\n")

print(pero_peric.total_invoices_amount)

print()
print("\n" + "="*40 + "\n")
print()
pero_peric.invoices[0].print_invoice()