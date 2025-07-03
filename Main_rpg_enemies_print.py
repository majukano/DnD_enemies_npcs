from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas

# umrechnung von cm in punktwerte
cm2point = 28.35


def my_enemie_size(en_size, cm2point):
    if en_size == "klein":
        en_width = 2 * cm2point  # cm
        en_height = 3 * cm2point  # cm
    elif en_size == "mittel":
        en_width = 2.5 * cm2point  # cm
        en_height = 4 * cm2point  # cm
    elif en_size == "groß":
        en_width = 5 * cm2point  # cm
        en_height = 8 * cm2point  # cm
    elif en_size == "rießig":
        en_width = 7.5 * cm2point  # cm
        en_height = 10 * cm2point  # cm
    elif en_size == "gigantisch":
        en_width = 10 * cm2point  # cm
        en_height = 12 * cm2point  # cm
    return en_width, en_height


# Lege den Dateinamen der PDF fest
filename = "my_rpg_enemies.pdf"
en_size = "mittel"

# Erstelle ein Canvas-Objekt für die PDF
c = canvas.Canvas(
    filename, pagesize=landscape(A4)
)  # Hier wird das Querformat festgelegt

page_width, page_height = landscape(A4)
en_width, en_height = my_enemie_size(en_size, cm2point)

x_pos = 2 * cm2point
y_pos = 2 * cm2point


i = 0
print_width = x_pos + en_width
while print_width < page_width - x_pos:
    i += 1
    print_width = print_width + en_width
    r_height = en_width / 2
    c.rect(x_pos + ((en_width * (i - 1))), y_pos, en_width, r_height)  # Fuss Teil 1
    r_height = r_height + en_height
    c.rect(x_pos + ((en_width * (i - 1))), y_pos, en_width, r_height)  # Körper Teil 1
    r_height = r_height + en_height
    c.rect(x_pos + ((en_width * (i - 1))), y_pos, en_width, r_height)  # Körper Teil 2
    r_height = r_height + en_width / 2
    c.rect(x_pos + ((en_width * (i - 1))), y_pos, en_width, r_height)  # Fuss Teil 2
    r_height = r_height + en_width
    c.rect(x_pos + ((en_width * (i - 1))), y_pos, en_width, r_height)  # Fuss Teil 3


# Speichere die leere Seite
c.showPage()  # Fügt eine Seite hinzu
c.save()  # Speichert das Dokument

print("========================= THE END ============================")
