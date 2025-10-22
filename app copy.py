"""
CRM Sustav za upravljanje klijentima i fakturama
Autor: [Tvoje ime]
Datum: 22.10.2025
Verzija: 1.0

TODO Lista:
- [ ] Implementirati validaciju podataka u add_invoice metodi
- [ ] Dodati notifikacijski sustav (email, SMS, push)
- [ ] Implementirati database integraciju (SQLite/MySQL)
- [ ] Dodati klasu za Company (podaci o tvrtki)
- [ ] Implementirati različite valute (EUR, USD, HRK)
- [ ] Dodati export u druge formate (Excel, XML)
- [ ] Implementirati sustav za praćenje plaćanja
- [ ] Dodati funkcionalnost za storniranje računa
- [ ] Kreirati dashboard za pregled svih računa
- [ ] Implementirati multi-language podršku
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
from datetime import datetime
import qrcode
from pdf417gen import encode, render_image
import base64


class Client:
    """
    Klasa za upravljanje podacima o klijentu
    
    Attributes:
        first_name (str): Ime klijenta
        last_name (str): Prezime klijenta
        postal_address (PostalAddress): Adresa klijenta
        email (Email): Email adresa klijenta
        phone (str): Telefonski broj klijenta
        invoices (list): Lista svih računa klijenta
        total_invoices_amount (float): Ukupan iznos svih računa
    """
    
    def __init__(self, first_name, last_name, postal_address, email, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.postal_address = postal_address
        self.email = email
        self.phone = phone
        self.invoices = []
        self.total_invoices_amount = 0.0


    def add_invoice(self, invoice):
        """
        Dodaje novu fakturu klijentu
        
        TODO:
        - Dodati validaciju invoice objekta (isinstance check)
        - Provjeriti da li invoice već postoji u listi
        - Validirati da je invoice.total > 0
        - Dodati try-except za error handling
        - Implementirati logging
        - Poslati notifikaciju klijentu (email/SMS)
        """
        # Napraviti provjeru dobivenih podataka!!! I samo ako je sve OK, dodati fakturu
        self.invoices.append(invoice)
        self.calculate_total_invoices_amount()
        # Opcija: Posalji notifikaciju klijentu o novoj fakturi (email, SMS, push notifikacija...)


    def calculate_total_invoices_amount(self):
        """Izračunava ukupan iznos svih računa klijenta"""
        self.total_invoices_amount = sum(invoice.total for invoice in self.invoices)
        return self.total_invoices_amount


    def get_unpaid_invoices(self):
        """
        TODO: Vraća listu neplaćenih računa
        - Implementirati property 'paid' u Invoice klasi
        - Dodati filtriranje po datumu dospijeća
        """
        pass


    def get_overdue_invoices(self):
        """
        TODO: Vraća listu računa s prošlim rokom plaćanja
        - Usporediti due_date s današnjim datumom
        - Sortirati po datumu
        """
        pass


    def __str__(self):
        return f"Client({self.first_name} {self.last_name}, {self.postal_address}, {self.email}, {self.phone})"



class PostalAddress:
    """
    Klasa za upravljanje poštanskom adresom
    
    TODO:
    - Dodati validaciju poštanskog broja (regex)
    - Implementirati Google Maps API integraciju
    - Dodati standardizaciju adresa
    """
    
    def __init__(self, street, house_number, postal_code, city, country):
        self.street = street
        self.house_number = house_number
        self.postal_code = postal_code
        self.city = city
        self.country = country


    def __str__(self):
        return f"{self.street} {self.house_number}, {self.postal_code} {self.city}, {self.country}"



class Email:
    """
    Klasa za upravljanje email adresom
    
    TODO:
    - Dodati validaciju email formata (regex)
    - Implementirati email verification
    - Dodati support za multiple email tipova (work, personal, billing)
    """
    
    def __init__(self, email_address, email_type):
        self.email_address = email_address
        self.email_type = email_type  # Work, Personal, Billing


    def validate_email(self):
        """TODO: Validira format email adrese"""
        pass


    def __str__(self):
        return f"{self.email_address} ({self.email_type})"



class PaymentDetails:
    """
    Klasa za upravljanje podacima o plaćanju
    
    Attributes:
        iban (str): IBAN broj bankovnog računa
        model (str): Model plaćanja (HR00, HR01, etc.)
        reference_number (str): Poziv na broj primatelja
        amount (float): Iznos plaćanja
        receiver_name (str): Naziv primatelja
        purpose (str): Svrha plaćanja
    """
    
    def __init__(self, iban, model, reference_number, amount, receiver_name, purpose):
        self.iban = iban
        self.model = model
        self.reference_number = reference_number
        self.amount = amount
        self.receiver_name = receiver_name
        self.purpose = purpose
    
    
    def validate_iban(self):
        """
        TODO: Validira IBAN broj
        - Provjeriti duljinu (21 znak za HR)
        - Provjeriti format (HR + 19 znamenki)
        - Izračunati i provjeriti kontrolni broj
        """
        pass
    
    
    def generate_hub3_string(self):
        """
        Generira HUB3 string za PDF417 barcode prema HUB3 standardu
        
        Returns:
            str: Formatirani HUB3 string
            
        TODO:
        - Dodati podršku za EUR valutu
        - Implementirati validaciju svih polja
        - Dodati support za dodatne opcije (hitno plaćanje, itd.)
        """
        # Format prema HUB3 standardu Hrvatske narodne banke
        hub3_data = (
            f"HRVHUB30\n"
            f"HRK\n"
            f"{self.amount:.2f}\n"
            f"{self.receiver_name}\n"
            f"{self.iban}\n"
            f"{self.model}\n"
            f"{self.reference_number}\n"
            f"\n"  # Pošiljatelj ime (prazno jer ga popunjava banka)
            f"\n"  # Pošiljatelj adresa
            f"\n"  # Pošiljatelj mjesto
            f"{self.purpose}\n"
        )
        return hub3_data



class Invoice:
    """
    Klasa za upravljanje računima
    
    Attributes:
        invoice_number (str): Jedinstveni broj računa
        invoice_date (str): Datum izdavanja računa
        due_date (str): Datum dospijeća plaćanja
        client (Client): Klijent kojem je račun izdan
        items (list): Lista stavki na računu
        tax_rate (float): Porezna stopa (default 0.25 = 25%)
        subtotal (float): Osnovica
        tax (float): Iznos poreza
        total (float): Ukupan iznos s porezom
    """
    
    def __init__(self, invoice_number, invoice_date, due_date, client, items=[], tax_rate=0.25):
        self.invoice_number = invoice_number
        self.invoice_date = invoice_date
        self.due_date = due_date
        self.client = client
        self.items = items
        self.tax_rate = tax_rate
        self.subtotal, self.tax, self.total = self.calculate_totals()
        self.qr_code = 'Ovo je QR Code'  # Placeholder for QR code generation
        
        # TODO: Dodati dodatne atribute
        # self.paid = False
        # self.payment_date = None
        # self.currency = "EUR"
        # self.notes = ""
        # self.discount = 0.0


    def calculate_totals(self):
        """
        Izračunava osnovicu, porez i ukupan iznos
        
        Returns:
            tuple: (subtotal, tax, total)
        """
        subtotal = sum(item.total_price for item in self.items)
        tax = subtotal * self.tax_rate
        total = subtotal + tax
        return subtotal, tax, total


    def generate_qr_code(self):
        """
        Generira QR kod za plaćanje računa
        
        Returns:
            PIL.Image: QR kod kao slika
            
        TODO:
        - Dodati više informacija u QR kod
        - Implementirati EPC QR standard za SEPA plaćanja
        - Dodati logo u sredinu QR koda
        """
        payment_data = (
            f"Invoice: {self.invoice_number}\n"
            f"Amount: {self.total:.2f} €\n"
            f"Due Date: {self.due_date}\n"
            f"Client: {self.client.first_name} {self.client.last_name}"
        )
        
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=4
        )
        qr.add_data(payment_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        return img


    def generate_hub3_barcode(self, payment_details):
        """
        Generira HUB3 PDF417 barcode za plaćanje
        
        Args:
            payment_details (PaymentDetails): Podaci za plaćanje
            
        Returns:
            PIL.Image: PDF417 barcode kao slika
            
        TODO:
        - Dodati error handling za neispravne podatke
        - Optimizirati veličinu barcode-a
        """
        hub3_string = payment_details.generate_hub3_string()
        
        # Generiraj PDF417 barcode prema HUB3 standardu
        codes = encode(hub3_string, columns=8, security_level=5)
        image = render_image(codes, scale=2, ratio=3)
        
        return image


    def save_payment_codes(self, payment_details, qr_filename="qr_code.png", hub3_filename="hub3_barcode.png"):
        """
        Sprema QR i HUB3 kodove kao slike
        
        Args:
            payment_details (PaymentDetails): Podaci za plaćanje
            qr_filename (str): Naziv datoteke za QR kod
            hub3_filename (str): Naziv datoteke za HUB3 barcode
            
        TODO:
        - Dodati folder strukturu za spremanje (invoices/2025/10/)
        - Implementirati kompresiju slika
        - Dodati watermark opciju
        """
        # Spremi QR kod
        qr_img = self.generate_qr_code()
        qr_img.save(qr_filename)
        
        # Spremi HUB3 barcode
        hub3_img = self.generate_hub3_barcode(payment_details)
        hub3_img.save(hub3_filename)
        
        print(f"QR kod spremljen kao: {qr_filename}")
        print(f"HUB3 barcode spremljen kao: {hub3_filename}")


    def export_to_pdf(self, payment_details, filename=None):
        """
        Izvozi račun u PDF format s QR i HUB3 kodovima
        
        Args:
            payment_details (PaymentDetails): Podaci za plaćanje
            filename (str): Naziv PDF datoteke
            
        Returns:
            str: Putanja do spremljenog PDF-a
            
        TODO:
        - Dodati profesionalni template/logo
        - Implementirati različite PDF teme
        - Dodati digitalni potpis na PDF
        - Implementirati PDF/A standard za arhiviranje
        - Dodati paginaciju za dugačke račune
        - Implementirati header i footer na svakoj stranici
        """
        if filename is None:
            filename = f"Invoice_{self.invoice_number}.pdf"
        
        # Kreiraj PDF
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        
        # === ZAGLAVLJE RAČUNA ===
        c.setFont("Helvetica-Bold", 16)
        c.drawString(30, height - 40, "RAČUN / INVOICE")
        
        # TODO: Dodati logo tvrtke u desnom kutu
        # c.drawImage("logo.png", width - 150, height - 60, width=120, height=40)
        
        # === OSNOVNI PODACI O RAČUNU ===
        c.setFont("Helvetica", 10)
        y_position = height - 70
        
        c.drawString(30, y_position, f"Broj računa: {self.invoice_number}")
        y_position -= 15
        c.drawString(30, y_position, f"Datum izdavanja: {self.invoice_date}")
        y_position -= 15
        c.drawString(30, y_position, f"Datum dospijeća: {self.due_date}")
        y_position -= 30
        
        # === PODACI O KLIJENTU ===
        c.setFont("Helvetica-Bold", 12)
        c.drawString(30, y_position, "Kupac:")
        y_position -= 15
        
        c.setFont("Helvetica", 10)
        c.drawString(30, y_position, f"{self.client.first_name} {self.client.last_name}")
        y_position -= 15
        c.drawString(30, y_position, str(self.client.postal_address))
        y_position -= 15
        c.drawString(30, y_position, f"Email: {self.client.email}")
        y_position -= 15
        c.drawString(30, y_position, f"Telefon: {self.client.phone}")
        y_position -= 30
        
        # TODO: Dodati podatke o tvrtki (izdavatelj računa) na desnu stranu
        
        # === STAVKE RAČUNA - TABLICA ===
        c.setFont("Helvetica-Bold", 12)
        c.drawString(30, y_position, "Stavke:")
        y_position -= 20
        
        # Zaglavlje tablice
        c.setFont("Helvetica-Bold", 9)
        c.drawString(30, y_position, "Opis")
        c.drawString(300, y_position, "Količina")
        c.drawString(370, y_position, "Cijena")
        c.drawString(450, y_position, "Ukupno")
        y_position -= 2
        c.line(30, y_position, width - 30, y_position)
        y_position -= 15
        
        # Stavke
        c.setFont("Helvetica", 9)
        for item in self.items:
            # Provjera za novu stranicu ako nema dovoljno prostora
            if y_position < 150:
                c.showPage()
                y_position = height - 40
                # TODO: Ponoviti header na novoj stranici
            
            # Skrati opis ako je predugačak
            c.drawString(30, y_position, item.description[:35])
            c.drawString(300, y_position, str(item.quantity))
            c.drawString(370, y_position, f"{item.unit_price:.2f} €")
            c.drawString(450, y_position, f"{item.total_price:.2f} €")
            y_position -= 15
        
        # Linija prije totalova
        y_position -= 5
        c.line(300, y_position, width - 30, y_position)
        y_position -= 15
        
        # === TOTALI ===
        c.setFont("Helvetica", 10)
        c.drawString(370, y_position, "Osnovica:")
        c.drawString(450, y_position, f"{self.subtotal:.2f} €")
        y_position -= 15
        
        c.drawString(370, y_position, f"PDV ({int(self.tax_rate * 100)}%):")
        c.drawString(450, y_position, f"{self.tax:.2f} €")
        y_position -= 15
        
        c.setFont("Helvetica-Bold", 11)
        c.drawString(370, y_position, "UKUPNO:")
        c.drawString(450, y_position, f"{self.total:.2f} €")
        y_position -= 40
        
        # === GENERIRAJ KODOVE U MEMORIJI ===
        qr_img = self.generate_qr_code()
        qr_buffer = BytesIO()
        qr_img.save(qr_buffer, format='PNG')
        qr_buffer.seek(0)
        
        hub3_img = self.generate_hub3_barcode(payment_details)
        hub3_buffer = BytesIO()
        hub3_img.save(hub3_buffer, format='PNG')
        hub3_buffer.seek(0)
        
        # Provjera za novu stranicu ako nema dovoljno prostora za kodove
        if y_position < 200:
            c.showPage()
            y_position = height - 40
        
        # === PODACI ZA PLAĆANJE ===
        c.setFont("Helvetica-Bold", 10)
        c.drawString(30, y_position, "Podaci za plaćanje:")
        y_position -= 15
        
        c.setFont("Helvetica", 9)
        c.drawString(30, y_position, f"IBAN: {payment_details.iban}")
        y_position -= 12
        c.drawString(30, y_position, f"Model: {payment_details.model}")
        y_position -= 12
        c.drawString(30, y_position, f"Poziv na broj: {payment_details.reference_number}")
        y_position -= 12
        c.drawString(30, y_position, f"Primatelj: {payment_details.receiver_name}")
        y_position -= 12
        c.drawString(30, y_position, f"Svrha: {payment_details.purpose}")
        y_position -= 25
        
        # === QR KOD (LIJEVO) ===
        c.drawString(30, y_position, "QR kod za plaćanje:")
        y_position -= 5
        c.drawImage(ImageReader(qr_buffer), 30, y_position - 100, width=100, height=100)
        
        # === HUB3 BARCODE (DESNO) ===
        c.drawString(width - 230, y_position + 105, "HUB3 barcode:")
        c.drawImage(ImageReader(hub3_buffer), width - 230, y_position - 100, width=200, height=100)
        
        # === FOOTER ===
        c.setFont("Helvetica", 8)
        c.drawString(30, 30, f"Generirano: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        c.drawString(width - 150, 30, "Hvala na suradnji!")
        
        # TODO: Dodati QR kod za kontakt podatke tvrtke
        # TODO: Dodati link na online payment portal
        
        c.save()
        print(f"PDF račun spremljen kao: {filename}")
        return filename


    def print_invoice(self):
        """
        Ispisuje račun u konzolu (za debugging)
        
        TODO:
        - Dodati pretty print formatiranje
        - Implementirati color coding
        """
        print(f"Invoice Number: {self.invoice_number}")
        print(f"Invoice Date: {self.invoice_date}")
        print(f"Due Date: {self.due_date}")
        print(f"Bill To: {self.client}")
        print(f"Address: {self.client.postal_address}\n")
        print(f"Email: {self.client.email}\n")
        print(f"Phone: {self.client.phone}\n")
        print("Items:")
        for item in self.items:
            print(item)
        print(f"\nSubtotal: {self.subtotal:.2f} €")
        print(f"Tax (25%): {self.tax:.2f} €")
        print(f"Total: {self.total:.2f} €")
        print("\n[QR Code and HUB3 Barcode available]")


    def add_item(self, item):
        """
        Dodaje novu stavku na račun i preračunava totale
        
        Args:
            item (InvoiceItem): Stavka za dodati
            
        TODO:
        - Dodati validaciju item objekta
        - Provjeriti da li stavka već postoji
        - Dodati logging
        """
        self.items.append(item)
        self.subtotal, self.tax, self.total = self.calculate_totals()


    def remove_item(self, item_description):
        """
        TODO: Uklanja stavku s računa po opisu
        - Implementirati uklanjanje stavke
        - Preračunati totale nakon uklanjanja
        """
        pass


    def send_email(self):
        """
        TODO: Šalje račun na email klijentu
        - Implementirati SMTP integraciju
        - Dodati PDF attachment
        - Kreirati email template
        """
        pass


    def __str__(self):
        return f"Invoice({self.invoice_number}, Total: {self.total:.2f} €)"



class InvoiceItem:
    """
    Klasa za pojedinačnu stavku na računu
    
    Attributes:
        description (str): Opis proizvoda/usluge
        quantity (int/float): Količina
        unit_price (float): Jedinična cijena
        total_price (float): Ukupna cijena stavke
    """
    
    def __init__(self, description, quantity, unit_price):
        self.description = description
        self.quantity = quantity
        self.unit_price = unit_price
        self.total_price = self.calcualte_total_price()
        
        # TODO: Dodati dodatne atribute
        # self.unit = "kom"  # komad, sat, m2, kg, itd.
        # self.discount = 0.0
        # self.tax_rate = 0.25


    def calcualte_total_price(self):
        """Izračunava ukupnu cijenu stavke"""
        return self.quantity * self.unit_price


    def apply_discount(self, discount_percentage):
        """
        TODO: Primjenjuje popust na stavku
        - Izračunati novu cijenu s popustom
        - Ažurirati total_price
        """
        pass


    def __str__(self):
        return f"- {self.description}, {self.quantity} x {self.unit_price:.2f} €, Total: {self.total_price:.2f} €"


# ============================================================================
# GLAVNI PROGRAM - PRIMJERI KORIŠTENJA
# ============================================================================

if __name__ == "__main__":
    print("=== CRM SUSTAV - PRIMJER KORIŠTENJA ===\n")
    
    # === KREIRANJE KLIJENTA ===
    postal_address = PostalAddress("Ulica Primjera", "10A", "10000", "Zagreb", "Hrvatska")
    email_address = Email("pero@email.com", "Work")
    pero_peric = Client("Pero", "Perić", postal_address, email_address, "+38591234567")
    
    print(f"Kreiran klijent: {pero_peric}\n")
    
    
    # === KREIRANJE PRVOG RAČUNA ===
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
    
    # Dodaj račun klijentu
    pero_peric.add_invoice(invoice)
    
    # Dodaj dodatnu stavku na račun
    invoice.add_item(InvoiceItem("SEO Services", 5, 300.00))
    
    print(f"Kreiran račun: {invoice}")
    print(f"Ukupan iznos: {invoice.total:.2f} €\n")
    
    
    # === KREIRANJE DRUGOG RAČUNA ===
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
    
    
    # === ISPIS SVIH RAČUNA U KONZOLU ===
    print("\n=== ISPIS SVIH RAČUNA ===\n")
    for inv in pero_peric.invoices:
        inv.print_invoice()
        print("\n" + "="*40 + "\n")
    
    
    # === PRIKAZ UKUPNOG IZNOSA SVIH RAČUNA ===
    print(f"Ukupan iznos svih računa za {pero_peric.first_name} {pero_peric.last_name}:")
    print(f"{pero_peric.total_invoices_amount:.2f} €")
    
    
    # === IZVOZ RAČUNA U PDF ===
    print("\n=== IZVOZ RAČUNA U PDF ===\n")
    
    for idx, inv in enumerate(pero_peric.invoices):
        # Kreiraj podatke za plaćanje
        payment_info = PaymentDetails(
            iban="HR1234567890123456789",
            model="HR00",
            reference_number=f"{inv.invoice_number}-2024",
            amount=inv.total,
            receiver_name="Steel Works d.o.o.",
            purpose=f"Plaćanje po računu {inv.invoice_number}"
        )
        
        # Izvezi u PDF
        pdf_file = inv.export_to_pdf(payment_info, filename=f"Racun_{inv.invoice_number}.pdf")
        print(f"✓ PDF {idx + 1} kreiran: {pdf_file}")
    
    
    # === SPREMANJE KODOVA KAO SLIKE (OPCIONO) ===
    print("\n=== SPREMANJE QR I HUB3 KODOVA ===\n")
    
    payment_info = PaymentDetails(
        iban="HR1234567890123456789",
        model="HR00",
        reference_number=f"{invoice.invoice_number}-2024",
        amount=invoice.total,
        receiver_name="Steel Works d.o.o.",
        purpose=f"Plaćanje po računu {invoice.invoice_number}"
    )
    
    invoice.save_payment_codes(
        payment_info,
        qr_filename=f"qr_{invoice.invoice_number}.png",
        hub3_filename=f"hub3_{invoice.invoice_number}.png"
    )
    
    
    print("\n=== PROGRAM ZAVRŠEN ===")
    print("\nKreirana dokumentacija:")
    print("- 2 PDF računa")
    print("- 2 QR koda")
    print("- 2 HUB3 barkoda")
    print(f"\nUkupno računa: {len(pero_peric.invoices)}")
    print(f"Ukupna vrijednost: {pero_peric.total_invoices_amount:.2f} €")


"""
=============================================================================
NAPOMENE ZA DALJNJI RAZVOJ:

1. BAZA PODATAKA
   - Implementirati SQLite ili MySQL za perzistentnost podataka
   - Kreirati tablice: clients, invoices, invoice_items, payments
   - Dodati ORM (SQLAlchemy ili peewee)

2. VALIDACIJA
   - Dodati pydantic za validaciju podataka
   - Implementirati custom validators za IBAN, email, telefon
   - Dodati error handling i try-except blokove

3. NOTIFIKACIJE
   - Email integracija (SMTP ili SendGrid API)
   - SMS integracija (Twilio ili Infobip)
   - Push notifikacije

4. SIGURNOST
   - Dodati autentifikaciju i autorizaciju
   - Implementirati šifriranje osjetljivih podataka
   - Digitalni potpisi na PDF-ovima

5. WEB INTERFACE
   - Kreirati Flask ili FastAPI backend
   - Implementirati REST API
   - Dodati React ili Vue.js frontend

6. IZVJEŠTAJI
   - Dashboard s grafovima (matplotlib, plotly)
   - Izvještaji o prodaji po periodima
   - Analitika plaćanja

7. INTEGRACIJE
   - Accounting software (ERPNext, Odoo)
   - Payment gateways (Stripe, PayPal)
   - Banking API-ji

=============================================================================
"""
