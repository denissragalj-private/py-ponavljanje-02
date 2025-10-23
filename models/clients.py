


class Client:
    def __init__(self, first_name, last_name, postal_address, email, phone):
        self.id = 1
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

