




class PostalAddress:
    def __init__(self, street, house_number, postal_code, city, country):
        self.id = 1
        self.street = street
        self.house_number = house_number
        self.postal_code = postal_code
        self.city = city
        self.country = country

    def __str__(self):
        return f"{self.street} {self.house_number}, {self.postal_code} {self.city}, {self.country}"