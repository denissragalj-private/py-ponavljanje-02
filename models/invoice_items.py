

class InvoiceItem:
    def __init__(self, description, quantity, unit_price):
        self.id = 1
        self.description = description
        self.quantity = quantity
        self.unit_price = unit_price
        self.total_price = self.calcualte_total_price()

    def calcualte_total_price(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"- {self.description}, {self.quantity} x {self.unit_price:.2f} €, Total: {self.total_price:.2f} €"


