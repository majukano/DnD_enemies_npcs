import os
from PIL import Image, ImageOps
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.utils import ImageReader

# =============================================================
# ======================= Functions ===========================
# =============================================================


# Gebe Bildgröße der Gegner aus
def my_enemie_size(en_size, cm2point):
    if en_size == "klein":
        en_width = 2 * cm2point  # cm
        en_height = 3 * cm2point  # cm
    elif en_size == "mittel":
        en_width = 12 * cm2point  # cm
        en_height = 7 * cm2point  # cm
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


# Gebe Dateipfade zu Bildern aus
def get_image_paths(image_folder):
    image_path_list = []
    for image_name in os.listdir(image_folder):
        path = os.path.join(image_folder, image_name)
        if os.path.isfile(path):
            image_path_list.append(path)
    return image_path_list


def prep_images(image_path_list, en_width, en_height, i):
    while i > len(image_path_list):
        i = i - len(image_path_list)
    image_path = image_path_list[i - 1]
    img = Image.open(image_path)
    img_width_px, img_height_px = img.size
    img_ratio = img_width_px / img_height_px
    img_2 = ImageOps.flip(img)
    temp_path_1 = "_img_chr_temp_1.png"
    temp_path_2 = "_img_chr_temp_2.png"
    img.save(temp_path_1)
    img_2.save(temp_path_2)
    img_data = [temp_path_1, temp_path_2, img_ratio]
    return img_data
    # Umrechnung auf Punktmaßstab (1 Punkt = 1/72 Zoll)
    # dpi = img.info.get("dpi", (72,72))[0] # Fallback: 72 DPI
    # img_width_pt = img_width_px * 72 / dpi
    # img_height_pt = img_height_px * 72 /dpi


def get_img_size(img_ratio, en_width, en_height):
    en_ratio = en_width / en_height
    if img_ratio > en_ratio:
        img_width = en_width
        img_height = en_width / img_ratio
    else:
        img_height = en_height
        img_width = en_height * img_ratio
    return img_width, img_height


# umrechnung von cm in punktwerte
cm2point = 28.35
image_folder = "images_chr"


# =============================================================
# ======================== Setup ==============================
# =============================================================


# Lege den Dateinamen der PDF fest
filename = "my_rpg_charakter.pdf"
en_size = "mittel"
name_text_h = 20

name_int = ["Modernder Schlürfer", "Grick", "Name Int 3", "Name Int 4"]
name_ext = ["Modernder Schlürfer", "Grick", "Name Ext 3", "Name Ext 4"]

text_1 = "RK: 15<br/>TP: 136<br/> Immun Blitz - wird durch Schaden geheilt<br/> Angriff: Mehrfachangriff (2) Schlag +7 Tr: 13<br/> wenn Trifft SG14 Verschligen:<br/>Ziel festgesetzt und geblendet. Jede Runde SG14-Konst. Tr. 13"

text_2 = "RK: 14<br/>TP: 27<br/>Tarnung +4 (Versteinert SG15 Warnehmung)<br/> Angriff: Tentakel +4 Tr: 7 Wenn trifft +:<br/> Schnabel +4 Tr: 5"
text_3 = "Hallo text 3"
text_4 = "Hallo text 4"

text_par = [text_1, text_2, text_3, text_4]


# =============================================================
# =================== Text Setup ==============================
# =============================================================

par_name_ext = ParagraphStyle(
    name="MeinStil",
    fontName="Helvetica",
    fontSize=name_text_h,  
    leading=20,
)

par_text = ParagraphStyle(
    name="MeinStil",
    fontName="Helvetica",
    fontSize=12,  #  Schriftgröße in Punkt
    leading=20,  #  Zeilenabstand (optional)
)

par_name_int = ParagraphStyle(
    name="MeinStil",
    fontName="Helvetica",
    fontSize=name_text_h,  #  Schriftgröße in Punkt
    leading=20,  #  Zeilenabstand (optional)
)


# =============================================================
# ========================== images ===========================
# =============================================================


image_path_list = get_image_paths(image_folder)

# =============================================================
# =================== PDF Generator ===========================
# =============================================================


# Erstelle ein Canvas-Objekt für die PDF
c = canvas.Canvas(
    filename, pagesize=landscape(A4)
)  # Hier wird das Querformat festgelegt

page_width, page_height = landscape(A4)
en_width, en_height = my_enemie_size(en_size, cm2point)

x_pos = 2 * cm2point
y_pos_s = 2 * cm2point

i = 0
print_width = x_pos + en_width
while print_width < page_width - x_pos:
    i += 1
    print_width = print_width + en_width

    # Textbereich Intern
    r_height = name_text_h * 1.8
    y_pos = y_pos_s
    x_start = x_pos + ((en_width * (i - 1)))
    r_h_fuss = en_width / 2
    c.rect(x_start, y_pos, en_width, r_height)  # Fuss Teil 1
    abs_name_int = Paragraph(name_int[i - 1], par_name_int)
    frame_name_int = Frame(x_start, y_pos, en_width, r_height)
    frame_name_int.addFromList([abs_name_int], c)

    # Körper Teil 1
    y_pos = y_pos + r_height
    r_height = en_height
    # Rechteck einzeichnen
    c.rect(x_start, y_pos, en_width, r_height)  # Körper Teil 1
    img_data = prep_images(image_path_list, en_width, en_height, i)
    img_width, img_height = get_img_size(img_data[2], en_width * 0.3, en_height)
    y_start = y_pos + r_height - img_height
    # Bild einzeichnen
    img = ImageReader(img_data[0])
    c.drawImage(img, x_start, y_start, img_width, img_height)
    abs_text = Paragraph(text_par[i - 1], par_text)
    frame_text = Frame(
        x_start + en_width * 0.3, y_pos, en_width - en_width * 0.3, en_height
    )
    frame_text.addFromList([abs_text], c)

    # Faltmarke
    fm_height = 1 * cm2point
    y_pos = y_pos + en_height
    c.rect(x_start, y_pos, en_width, fm_height)  # Faltmarke

    # Körper Teil 2
    r_height = r_height + en_height
    y_pos = y_pos + fm_height
    # Rechteck Zeichnen
    c.rect(x_pos + ((en_width * (i - 1))), y_pos, en_width, en_height)  # Körper Teil 2
    img_width, img_height = get_img_size(img_data[2], en_width, en_height)
    # Bild einzeichnen
    img = ImageReader(img_data[1])
    c.drawImage(img, x_start, y_pos, img_width, img_height)

    # Textbereich 2
    r_height = name_text_h * 1.8
    y_pos = y_pos + en_height
    # Text rechteck zeichnen
    c.rect(x_start, y_pos, en_width, r_height)
    abs_name_ext = Paragraph(name_ext[i - 1], par_name_int)
    c.saveState()
    c.translate(x_start + en_width / 2, y_pos + r_height / 2)
    c.rotate(180)
    frame_name_ext = Frame(-en_width / 2, -r_height / 2, en_width, r_height)
    # Text einzeichnen
    frame_name_ext.addFromList([abs_name_ext], c)
    c.restoreState()

# Speichere die leere Seite
c.showPage()  # Fügt eine Seite hinzu
c.save()  # Speichert das Dokument

print("========================= THE END ============================")
