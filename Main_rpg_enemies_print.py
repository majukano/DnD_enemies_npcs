import os
from PIL import Image, ImageOps
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas


# =============================================================
# ======================= Functions ===========================
# =============================================================


# Gebe Bildgröße der Gegner aus
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
    temp_path_1 = "_img_temp_1.png"
    temp_path_2 = "_img_temp_2.png"
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
image_folder = "images"


# =============================================================
# ======================== Setup ==============================
# =============================================================


# Lege den Dateinamen der PDF fest
filename = "my_rpg_enemies.pdf"
en_size = "mittel"


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
y_pos = 2 * cm2point

i = 0
print_width = x_pos + en_width
while print_width < page_width - x_pos:
    i += 1
    print_width = print_width + en_width
    r_height = en_width / 2
    r_h_fuss = en_width / 2
    c.rect(x_pos + ((en_width * (i - 1))), y_pos, en_width, r_height)  # Fuss Teil 1

    # Körper Teil 1
    r_height = r_height + en_height
    x_start = x_pos + ((en_width * (i - 1)))
    c.rect(x_start, y_pos, en_width, r_height)  # Körper Teil 1
    img_data = prep_images(image_path_list, en_width, en_height, i)
    img_width, img_height = get_img_size(img_data[2], en_width, en_height)
    y_start = y_pos + r_h_fuss + en_height - img_height
    c.drawImage(img_data[0], x_start, y_start, img_width, img_height)

    # Körper Teil 2
    r_height = r_height + en_height
    c.rect(x_pos + ((en_width * (i - 1))), y_pos, en_width, r_height)  # Körper Teil 2
    c.drawImage(
        img_data[1], x_start, y_pos + r_h_fuss + en_height, img_width, img_height
    )

    r_height = r_height + en_width / 2
    c.rect(x_pos + ((en_width * (i - 1))), y_pos, en_width, r_height)  # Fuss Teil 2
    r_height = r_height + en_width
    c.rect(x_pos + ((en_width * (i - 1))), y_pos, en_width, r_height)  # Fuss Teil 3


# Speichere die leere Seite
c.showPage()  # Fügt eine Seite hinzu
c.save()  # Speichert das Dokument

print("========================= THE END ============================")
