import base64
from io import BytesIO
from datetime import datetime
import qrcode
import barcode
from barcode.writer import ImageWriter
import pdf417
from PIL import Image, ImageChops


class MockDocument:
    """Klasa za simulaciju dokumenta s podacima"""

    def __init__(self, data: dict):
        self.doctype = data.get("doctype", "Sales Invoice")
        self.name = data.get("name", "ACC-SINV-2024-00001")
        self.company = data.get("company", "Moja Tvrtka d.o.o.")
        self.grand_total = data.get("grand_total", 1500.00)
        self.custom_odjel = data.get("custom_odjel", None)
        self.iban = data.get("iban", "HR1234567890123456789")
        self.bic = data.get("bic", "ZABAHR2XXXX")


def extract_reference_number(doc_name):
    """Izdvaja referentni broj iz naziva dokumenta"""
    parts = doc_name.split("-")
    if len(parts) >= 4:
        return f"{parts[1]}-{parts[2]}-{parts[3]}"
    elif len(parts) >= 3:
        return "-".join(parts[-3:])
    else:
        return doc_name[:10]


def get_document_type_label(doc):
    """Određuje oznaku dokumenta prema tipu"""
    if hasattr(doc, "doctype"):
        labels = {
            "Sales Invoice": "Račun br.",
            "Quotation": "Ponuda br.",
            "Purchase Order": "Narudžba br.",
            "Delivery Note": "Otpremnica br.",
        }
        return labels.get(doc.doctype, "Dokument br.")
    return "Dokument br."


def get_iban_by_department(doc):
    """Dohvaća IBAN ovisno o odjelu"""
    # Privremeno: koristi uvijek isti IBAN za testiranje
    return "HR9123600001503417252"

    # # Originalna logika (zakomentirana za testiranje):
    # if hasattr(doc, 'custom_odjel') and doc.custom_odjel == "Montaža":
    #     return "HR9123600001503417252"
    # return getattr(doc, 'iban', 'HR0000000000000000000')


def generate_hub30_payload(doc):
    """Generira HUB30 payload za 2D barkod"""
    iban = get_iban_by_department(doc)
    poziv_na_broj = extract_reference_number(doc.name)
    doc_label = get_document_type_label(doc)
    company = doc.company

    # Koristi ASCII-safe opis (bez hrvatskih znakova)
    description = f"Racun br. {poziv_na_broj}"
    company_street = "Racka 1C"  # Privremeno, može se prilagoditi
    company_postal_code_and_city = "10250 Ježdovec"  # Privremeno, može se prilagoditi
    lines = [
        "HRVHUB30",  # 1. Identifikator
        "EUR",  # 2. Valuta
        "{:015d}".format(int(doc.grand_total * 100)),  # 3. Iznos (u centima)
        "",  # 4. Ime platitelja
        "",  # 5. Ulica platitelja
        "",  # 6. broj pošte i mjesto platitelja
        company,  # 7. Naziv primatelja
        company_street,  # 8. Ulica primatelja
        company_postal_code_and_city,  # 9. Broj pošte i mjesto primatelja
        iban,  # 13. IBAN primatelja
        "HR00",  # 10. Model primatelja
        poziv_na_broj,  # 11. Poziv na broj primatelja
        "",  # 12. Šifra namjene     npr. COST
        description,  # 14. Opis plaćanja
        "",  # 15. Rezervirano
    ]
    return "\n".join(lines)


def generate_bcd_payload(doc):
    """Generira BCD (SEPA) payload za QR kod"""
    iban = get_iban_by_department(doc)
    bic = getattr(doc, "bic", "ZABAHR2XXXX")
    amount = f"EUR{doc.grand_total:.2f}".replace(",", ".")
    reference = extract_reference_number(doc.name)
    doc_label = get_document_type_label(doc)
    description = f"{doc_label} {reference}"
    company = doc.company

    lines = [
        "BCD",
        "002",
        "1",
        "SCT",
        bic,
        company,
        iban,
        amount,
        "",
        reference,
        "",
        description,
    ]
    return "\n".join(lines)


def auto_crop_white(img):
    """Obrezuje bijele rubove slike"""
    bg = Image.new(img.mode, img.size, "white")
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()
    if bbox:
        return img.crop(bbox)
    return img


def buffer_to_data_uri(buf: BytesIO) -> str:
    """Pretvara buffer u data URI"""
    return f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}"


def get_pdf417(data: str, scale: int = 3, ratio: float = 2.0) -> str:
    """Generira PDF417 2D barkod"""
    try:
        codes = pdf417.encode(str(data), columns=9, security_level=2)
        image = pdf417.render_image(codes, scale=scale, ratio=ratio)
        image = image.convert("RGB")
        image = auto_crop_white(image)
        buf = BytesIO()
        image.save(buf, format="PNG")
        return buffer_to_data_uri(buf)
    except Exception as e:
        print(f"PDF417 greška: {e}")
        return ""


def get_hub30_pdf417(doc, scale=3, ratio=2):
    """Generira HUB30 PDF417 barkod"""
    data = generate_hub30_payload(doc)
    return get_pdf417(data, scale=scale, ratio=ratio)


def get_barcode_image(data, barcode_type="code128", module_width=2, module_height=50):
    """Generira 1D barkod"""
    try:
        cls = barcode.get_barcode_class(barcode_type)
        code = cls(str(data), writer=ImageWriter())
        opts = {
            "module_width": module_width,
            "module_height": module_height,
            "quiet_zone": 6.5,
            "font_size": 10,
        }
        buf = BytesIO()
        code.write(buf, options=opts)
        return buffer_to_data_uri(buf)
    except Exception as e:
        print(f"Greška pri generiranju barkoda: {e}")
        return ""


def get_qr_code(data, box_size=10, border=1):
    """Generira QR kod"""
    try:
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=box_size,
            border=border,
        )
        qr.add_data(str(data))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img = img.convert("RGB")
        img = auto_crop_white(img)
        buf = BytesIO()
        img.save(buf, format="PNG")
        return buffer_to_data_uri(buf)
    except Exception as e:
        print(f"QR kod greška: {e}")
        return ""


def get_bcd_qr(doc, box_size=5):
    """Generira BCD QR kod za SEPA plaćanje"""
    bcd_data = generate_bcd_payload(doc)
    return get_qr_code(bcd_data, box_size=box_size, border=1)


def save_data_uri_to_file(data_uri: str, filename: str):
    """Sprema data URI u datoteku"""
    if data_uri.startswith("data:image/png;base64,"):
        base64_data = data_uri.split(",")[1]
        image_data = base64.b64decode(base64_data)
        with open(filename, "wb") as f:
            f.write(image_data)
        print(f"Slika spremljena: {filename}")


# Primjer korištenja
if __name__ == "__main__":
    # Simulirani podaci za standardni odjel
    test_data_standard = {
        "doctype": "Sales Invoice",
        "name": "005-2024-00123",
        "company": "Test Tvrtka d.o.o.",
        "grand_total": 2500.00,
        "custom_odjel": "Prodaja",
        "iban": "HR1234567890123456789",
        "bic": "ZABAHR2XXXX",
    }

    # Simulirani podaci za Montažu
    test_data_montaza = {
        "doctype": "Sales Invoice",
        "name": "005-2024-00456",
        "company": "Test Tvrtka d.o.o.",
        "grand_total": 3500.00,
        "custom_odjel": "Montaža",
        "iban": "HR9876543210987654321",
        "bic": "ZABAHR2XXXX",
    }

    # Kreiraj mock dokumente
    doc_standard = MockDocument(test_data_standard)
    doc_montaza = MockDocument(test_data_montaza)

    print("Generiranje barkodova za standardni dokument...")
    print(f"IBAN: {get_iban_by_department(doc_standard)}")

    # Generiraj različite tipove barkodova
    hub30_barcode = get_hub30_pdf417(doc_standard)
    bcd_qr = get_bcd_qr(doc_standard)
    simple_barcode = get_barcode_image(doc_standard.name)
    simple_qr = get_qr_code(doc_standard.name)

    # Spremi slike
    if hub30_barcode:
        save_data_uri_to_file(hub30_barcode, "./_OLD/Barcode/hub30_standard.png")
    if bcd_qr:
        save_data_uri_to_file(bcd_qr, "./_OLD/Barcode/bcd_qr_standard.png")
    if simple_barcode:
        save_data_uri_to_file(simple_barcode, "./_OLD/Barcode/barcode_standard.png")
    if simple_qr:
        save_data_uri_to_file(simple_qr, "./_OLD/Barcode/qr_standard.png")

    print("\nGeneriranje barkodova za Montažu...")
    print(f"IBAN: {get_iban_by_department(doc_montaza)}")

    # Generiraj za Montažu
    hub30_montaza = get_hub30_pdf417(doc_montaza)
    bcd_montaza = get_bcd_qr(doc_montaza)

    if hub30_montaza:
        save_data_uri_to_file(hub30_montaza, "./_OLD/Barcode/hub30_montaza.png")
    if bcd_montaza:
        save_data_uri_to_file(bcd_montaza, "./_OLD/Barcode/bcd_qr_montaza.png")

    print("\nGotovo! Provjerite generirane PNG datoteke.")

    # Ispis payloada za provjeru
    print("\n--- HUB30 Payload (Standard) ---")
    print(generate_hub30_payload(doc_standard))

    print("\n--- BCD Payload (Montaža) ---")
    print(generate_bcd_payload(doc_montaza))
