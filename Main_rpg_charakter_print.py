from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

# Erstelle ein PDF im Querformat
page_width, page_height = landscape(A4)
c = canvas.Canvas("gruppen_din_a4_quer.pdf", pagesize=(page_width, page_height))

# Definition der Gruppen-Geometrie
gruppen_breite = 6 * cm
gruppen_hoehe = 15 * cm

# Abstände
horizontaler_abstand = 2 * cm
start_x = (page_width - (3 * gruppen_breite + 2 * horizontaler_abstand)) / 2
start_y = (page_height - gruppen_hoehe) / 2


# Hilfsfunktion zum Zeichnen einer Gruppe
def zeichne_gruppe(c, x, y):
    # Bereich A
    c.rect(x, y + 20 * cm, 6 * cm, 1 * cm, stroke=1, fill=0)
    c.drawString(x + 0.2 * cm, y + 20.2 * cm, "A")

    # Bereich B
    c.rect(x, y + 12 * cm, 6 * cm, 6 * cm, stroke=1, fill=0)
    c.drawString(x + 0.2 * cm, y + 12.2 * cm, "B")

    # Bereich C
    c.rect(x, y + 10 * cm, 8 * cm, 2 * cm, stroke=1, fill=0)
    c.drawString(x + 0.2 * cm, y + 10.2 * cm, "C")

    # Bereich D
    c.rect(x, y, 8 * cm, 10 * cm, stroke=1, fill=0)
    c.drawString(x + 0.2 * cm, y + 0.2 * cm, "D")


# Zeichne 3 Gruppen nebeneinander
for i in range(3):
    x_pos = start_x + i * (gruppen_breite + horizontaler_abstand)
    zeichne_gruppe(c, x_pos, start_y)

c.save()
