#!/usr/bin/env python3
"""Draw the front page for news-image-20261117: 43 stories from Tuesday
17 November 2026 in one 1024x1024 image. Deterministic: no timestamps,
no randomness, no network. Flat vector-style drawings only — no photos,
no AI-generated imagery. Fonts: DejaVu (system)."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (20, 20, 20)
GREY = (90, 86, 76)
RED = (180, 35, 24)
NAVY = (31, 42, 68)
CARD_BG = (253, 252, 248)
LINE = (40, 38, 34)
SEA = (207, 227, 238)
SAND = (238, 222, 180)
LAND = (232, 214, 176)
LAND_DOT = (178, 148, 104)

FDIR = "/usr/share/fonts/truetype/dejavu"
def F(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)

F_SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
F_SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: F("DejaVuSans.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_lines(lines, x, y, font, fill, lh):
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y

def text_h(font):
    a, b = font.getbbox("Ag")
    return b - a

def fit_check(lines, max_lines, what):
    if len(lines) > max_lines:
        raise SystemExit(f"OVERFLOW in {what}: {len(lines)} lines > {max_lines}: {lines}")

# ---------------- region colours ----------------
C_EU = (43, 90, 166)
C_ME = (194, 87, 27)
C_AS = (123, 75, 166)
C_AF = (46, 125, 79)
C_AM = (180, 35, 24)
C_OC = (31, 138, 138)
C_GL = (85, 85, 85)

# ---------------- continent polygons (lon, lat) ----------------
EURASIA = [(-9,37),(-9,43),(-2,44),(-1,46),(-4,48),(-2,50),(1,51),(4,53),(8,54),(8,57),(10,58),(7,60),(5,62),(10,64),(14,67),(19,69),(24,71),(30,70),(35,68),(42,68),(48,68),(54,68),(60,69),(66,69),(72,72),(78,72),(85,73),(95,75),(105,77),(112,74),(120,73),(128,71),(138,72),(148,72),(158,70),(162,66),(170,66),(178,65),(178,62),(170,60),(162,59),(158,52),(156,51),(150,59),(142,59),(141,52),(140,47),(138,43),(135,43),(132,43),(130,42),(127,40),(126,38),(124,40),(121,37),(120,32),(122,30),(120,25),(117,23),(112,22),(108,18),(106,11),(105,9),(103,7),(100,6),(98,10),(97,15),(94,16),(92,21),(90,22),(88,22),(86,20),(83,18),(80,15),(80,10),(77,8),(75,10),(73,16),(70,20),(68,23),(66,25),(62,25),(58,25),(56,26),(52,26),(50,29),(48,30),(45,29),(43,28),(41,27),(39,21),(38,18),(35,28),(34,28),(33,29),(32,31),(30,31),(27,37),(26,38),(23,36),(22,37),(20,39),(19,42),(16,40),(14,38),(12,38),(10,37),(8,37),(8,39),(4,39),(2,41),(0,38),(-2,37),(-6,36)]
N_AMERICA = [(-168,66),(-165,60),(-158,58),(-152,60),(-140,60),(-135,58),(-130,54),(-125,49),(-124,42),(-120,34),(-114,29),(-110,24),(-105,20),(-97,16),(-94,17),(-90,14),(-86,12),(-83,9),(-80,8),(-77,7),(-79,9),(-81,13),(-84,16),(-87,13),(-88,18),(-90,21),(-91,19),(-96,19),(-97,22),(-97,26),(-93,30),(-89,30),(-84,30),(-81,26),(-80,32),(-76,35),(-74,40),(-70,42),(-68,45),(-65,44),(-60,47),(-55,47),(-60,52),(-65,50),(-60,55),(-65,60),(-68,58),(-75,62),(-78,62),(-85,66),(-90,66),(-95,69),(-110,68),(-125,70),(-140,70),(-155,71),(-165,68)]
S_AMERICA = [(-80,9),(-77,4),(-75,0),(-80,-3),(-81,-6),(-77,-12),(-72,-18),(-70,-23),(-70,-30),(-72,-37),(-73,-44),(-74,-50),(-70,-54),(-66,-55),(-65,-45),(-62,-41),(-58,-35),(-52,-32),(-48,-28),(-41,-23),(-39,-17),(-35,-9),(-35,-6),(-40,-3),(-44,-2),(-50,0),(-52,5),(-55,6),(-60,8),(-62,9),(-68,11),(-72,12),(-75,11),(-77,8)]
AFRICA = [(-17,15),(-17,21),(-15,27),(-10,31),(-5,35),(0,36),(10,37),(11,34),(20,32),(25,32),(30,31),(33,27),(35,23),(37,18),(39,15),(43,12),(48,11),(51,12),(46,5),(42,0),(40,-5),(40,-10),(37,-15),(35,-20),(32,-26),(28,-33),(20,-35),(17,-32),(15,-27),(13,-18),(12,-10),(13,-5),(9,4),(6,4),(-2,5),(-8,5),(-13,8),(-17,12)]
AUSTRALIA = [(113,-22),(114,-30),(115,-35),(118,-35),(124,-33),(129,-32),(132,-32),(135,-35),(138,-35),(140,-38),(145,-38),(150,-37),(153,-32),(153,-27),(150,-22),(146,-19),(142,-15),(142,-11),(140,-17),(136,-15),(135,-12),(132,-11),(130,-13),(126,-14),(122,-17),(118,-20),(114,-22)]
GREENLAND = [(-45,60),(-40,64),(-32,68),(-25,70),(-20,74),(-25,76),(-35,77),(-50,76),(-58,74),(-55,70),(-52,64),(-48,60)]
UK = [(-5,50),(-3,53),(-5,56),(-3,58),(-1,57),(0,53),(1,51)]
JAPAN = [(130,31),(132,33),(134,34),(136,35),(138,35),(140,37),(141,39),(141,41),(142,43),(144,44),(141,45),(139,41),(137,38),(135,34),(133,34),(130,33)]
MADAGASCAR = [(44,-16),(47,-15),(50,-16),(50,-20),(47,-24),(44,-25),(43,-21),(44,-17)]
NEWZEALAND = [(167,-45),(170,-43),(173,-41),(175,-38),(177,-38),(174,-36),(172,-35),(167,-45)]
CONTINENTS = [EURASIA, N_AMERICA, S_AMERICA, AFRICA, AUSTRALIA, GREENLAND, UK, JAPAN, MADAGASCAR, NEWZEALAND]

def point_in_poly(x, y, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside

def on_land(lon, lat):
    return any(point_in_poly(lon, lat, p) for p in CONTINENTS)

# ---------------- flat art helpers ----------------
def sea_sky(box, sea_h=0.55):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(198, 222, 235))
    d.rectangle([x0, y0 + (y1 - y0) * (1 - sea_h), x1, y1], fill=(120, 165, 200))

def label_tag(x, y, text, font, fg=(255, 255, 255), bg=RED):
    w = d.textlength(text, font=font) + 10
    d.rectangle([x, y, x + w, y + 15], fill=bg)
    d.text((x + 5, y + 1), text, font=font, fill=fg)
    return w

def flag(x, y, w, h, stripes):
    """stripes: list of colours top->bottom (horizontal) or ('v', [cols])."""
    if stripes and stripes[0] == 'v':
        cols = stripes[1]
        sw = w / len(cols)
        for i, c in enumerate(cols):
            d.rectangle([x + i * sw, y, x + (i + 1) * sw, y + h], fill=c)
    else:
        sh = h / len(stripes)
        for i, c in enumerate(stripes):
            d.rectangle([x, y + i * sh, x + w, y + (i + 1) * sh], fill=c)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)

# --- lead art ---
def art_bridge(box):
    x0, y0, x1, y1 = box
    sea_sky(box, 0.45)
    # bridge deck
    dy = y0 + 62
    d.rectangle([x0, dy, x1, dy + 7], fill=(70, 70, 74))
    # left span standing, right span standing, middle collapsed
    for px in range(x0 + 12, x1 - 12, 22):
        d.line([px, dy, px, dy + 26], fill=(70, 70, 74), width=3)
    # collapsed middle: deck plunging into the sea
    cx = (x0 + x1) // 2
    d.polygon([(cx - 42, dy), (cx + 40, dy), (cx + 22, y1 - 18), (cx - 20, y1 - 18)], fill=(60, 60, 64))
    d.line([cx - 42, dy, cx - 20, y1 - 18], fill=(40, 40, 44), width=3)
    d.line([cx + 40, dy, cx + 22, y1 - 18], fill=(40, 40, 44), width=3)
    # smoke + explosion
    d.ellipse([cx - 26, y0 + 18, cx + 2, y0 + 46], fill=(120, 118, 112))
    d.ellipse([cx - 8, y0 + 10, cx + 22, y0 + 38], fill=(150, 148, 140))
    d.polygon([(cx - 4, y0 + 30), (cx + 8, y0 + 42), (cx + 18, y0 + 28)], fill=(240, 170, 40))
    # jets
    d.polygon([(x0 + 16, y0 + 16), (x0 + 30, y0 + 20), (x0 + 16, y0 + 24)], fill=INK)
    d.polygon([(x1 - 34, y0 + 26), (x1 - 20, y0 + 30), (x1 - 34, y0 + 34)], fill=INK)
    # waves
    for wy in (y1 - 14, y1 - 8):
        for wx in range(x0 + 6, x1 - 6, 26):
            d.arc([wx, wy, wx + 18, wy + 8], 180, 360, fill=(230, 240, 246), width=2)
    d.text((x0 + 6, y0 + 4), "CRIMEA", font=F_SANS_B(10), fill=INK)
    d.text((x1 - 48, y0 + 4), "RUSSIA", font=F_SANS_B(10), fill=INK)
    label_tag(x1 - 118, y0 + 20, "ROAD SPAN DOWN", F_SANS_B(9))
    d.rectangle([x0, y1 - 18, x1, y1], fill=NAVY)
    d.text((x0 + 8, y1 - 16), "KERCH STRAIT · STRUCK FOR A SECOND DAY", font=F_SANS_B(9), fill=(255, 255, 255))

def art_gulf(box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=SAND)
    # gulf water shape
    gx0, gy0 = x0 + 30, y0 + 34
    gx1, gy1 = x1 - 26, y1 - 14
    d.polygon([(gx0, gy0 + 30), (gx0 + 60, gy0), (gx1, gy0 + 8), (gx1, gy1 - 20),
               (gx1 - 60, gy1), (gx0 + 20, gy1 - 26)], fill=(120, 165, 200))
    d.text((x0 + 8, y0 + 4), "IRAN", font=F_SANS_B(10), fill=INK)
    d.text((x0 + 8, y1 - 34), "BAHRAIN", font=F_SANS_B(10), fill=INK)
    d.text((x1 - 58, y1 - 34), "HORMUZ", font=F_SANS_B(10), fill=INK)
    # Qeshm island
    d.ellipse([x1 - 78, y0 + 44, x1 - 52, y0 + 62], fill=(210, 190, 140))
    d.text((x1 - 66, y0 + 66), "QESHM", font=F_SANS_B(9), fill=INK)
    # drone arrows toward Bahrain
    d.line([x0 + 96, y0 + 40, x0 + 52, y0 + 74], fill=RED, width=3)
    d.polygon([(x0 + 52, y0 + 74), (x0 + 64, y0 + 72), (x0 + 56, y0 + 82)], fill=RED)
    label_tag(x0 + 88, y0 + 44, "DRONES DOWNED", F_SANS_B(9))
    # strike marker on Qeshm
    d.line([x1 - 72, y0 + 46, x1 - 58, y0 + 60], fill=RED, width=3)
    d.line([x1 - 58, y0 + 46, x1 - 72, y0 + 60], fill=RED, width=3)
    label_tag(x0 + 128, y1 - 40, "US STRIKES", F_SANS_B(9), bg=NAVY)
    # tanker
    tx, ty = x1 - 96, y1 - 26
    d.rectangle([tx, ty, tx + 34, ty + 9], fill=(120, 40, 30))
    d.rectangle([tx + 6, ty - 7, tx + 12, ty], fill=(120, 40, 30))
    d.ellipse([tx + 8, ty - 16, tx + 26, ty - 2], fill=(150, 148, 140))
    d.polygon([(tx + 12, ty - 14), (tx + 20, ty - 4), (tx + 26, ty - 12)], fill=(240, 170, 40))

def art_quad(box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(232, 226, 244))
    d.rectangle([x0, y0, x1, y0 + 26], fill=(88, 52, 140))
    d.text((x0 + 10, y0 + 5), "QUAD LEADERS' SUMMIT · MANILA", font=F_SANS_B(11), fill=(255, 255, 255))
    fw, fh = 52, 30
    gap = (x1 - x0 - 4 * fw - 3 * 14) // 2
    fx = x0 + gap
    fy = y0 + 44
    # US
    flag(fx, fy, fw, fh, [(178, 34, 52), (255, 255, 255), (178, 34, 52), (255, 255, 255), (178, 34, 52)])
    d.rectangle([fx, fy, fx + 22, fy + 15], fill=(40, 60, 120))
    d.text((fx + 6, fy + fh + 4), "US", font=F_SANS_B(10), fill=INK)
    # India
    flag(fx + fw + 14, fy, fw, fh, [(255, 153, 51), (255, 255, 255), (19, 136, 8)])
    d.text((fx + fw + 14 + 12, fy + fh + 4), "INDIA", font=F_SANS_B(10), fill=INK)
    # Japan
    flag(fx + 2 * (fw + 14), fy, fw, fh, [(255, 255, 255)])
    d.ellipse([fx + 2 * (fw + 14) + 19, fy + 8, fx + 2 * (fw + 14) + 33, fy + 22], fill=(188, 0, 45))
    d.text((fx + 2 * (fw + 14) + 8, fy + fh + 4), "JAPAN", font=F_SANS_B(10), fill=INK)
    # Australia
    flag(fx + 3 * (fw + 14), fy, fw, fh, [(0, 40, 104)])
    d.text((fx + 3 * (fw + 14) + 10, fy + 6), "★", font=F_SANS_B(14), fill=(255, 255, 255))
    d.text((fx + 3 * (fw + 14) - 4, fy + fh + 4), "AUSTRALIA", font=F_SANS_B(10), fill=INK)
    # table
    ty = fy + fh + 24
    d.rectangle([x0 + 14, ty, x1 - 14, ty + 12], fill=(120, 72, 32))
    d.rectangle([x0 + 30, ty + 12, x0 + 40, ty + 30], fill=(90, 54, 24))
    d.rectangle([x1 - 40, ty + 12, x1 - 30, ty + 30], fill=(90, 54, 24))
    d.rectangle([x0, y1 - 18, x1, y1], fill=(88, 52, 140))
    d.text((x0 + 8, y1 - 16), "NEW CRITICAL-MINERALS DEALS", font=F_SANS_B(9), fill=(255, 255, 255))

# --- small-card icons (art box ~187x46) ---
def ic_virus(box, col=RED):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for ang in range(0, 360, 45):
        import math
        dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        d.line([cx + dx * 10, cy + dy * 10, cx + dx * 17, cy + dy * 17], fill=col, width=2)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=col)
    d.ellipse([cx - 4, cy - 4, cx + 1, cy + 1], fill=(255, 255, 255))

def ic_globe(box):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.ellipse([cx - 17, cy - 17, cx + 17, cy + 17], fill=(90, 160, 210), outline=INK, width=2)
    d.ellipse([cx - 6, cy - 17, cx + 6, cy + 17], outline=INK, width=1)
    d.line([cx - 17, cy, cx + 17, cy], fill=INK, width=1)
    d.arc([cx - 17, cy - 8, cx + 17, cy + 8], 0, 360, fill=INK, width=1)

def ic_chip(box):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle([cx - 12, cy - 12, cx + 12, cy + 12], fill=(40, 40, 44))
    d.rectangle([cx - 5, cy - 5, cx + 5, cy + 5], fill=(90, 200, 120))
    for dx in (-8, 0, 8):
        d.line([cx + dx, cy - 18, cx + dx, cy - 12], fill=INK, width=2)
        d.line([cx + dx, cy + 12, cx + dx, cy + 18], fill=INK, width=2)
    for dy in (-8, 0, 8):
        d.line([cx - 18, cy + dy, cx - 12, cy + dy], fill=INK, width=2)
        d.line([cx + 12, cy + dy, cx + 18, cy + dy], fill=INK, width=2)

def ic_tents(box):
    x0, y0, x1, y1 = box
    for i, tx in enumerate((x0 + 18, x0 + 62, x0 + 106)):
        d.polygon([(tx, y1 - 12), (tx + 14, y0 + 14), (tx + 28, y1 - 12)], fill=(210, 200, 170), outline=INK)
        d.polygon([(tx + 11, y1 - 12), (tx + 14, y0 + 22), (tx + 17, y1 - 12)], fill=INK)
    for rx in range(x0 + 10, x0 + 100, 18):
        d.line([rx, y0 + 4, rx - 5, y0 + 12], fill=(90, 140, 200), width=2)

def ic_letter(box):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle([cx - 22, cy - 14, cx + 22, cy + 14], fill=(255, 255, 255), outline=INK, width=2)
    d.line([cx - 22, cy - 14, cx, cy + 2], fill=INK, width=2)
    d.line([cx + 22, cy - 14, cx, cy + 2], fill=INK, width=2)
    d.line([cx - 15, cy + 6, cx + 15, cy + 6], fill=GREY, width=2)
    d.text((x1 - 34, y0 + 2), "RESIGN", font=F_SANS_B(9), fill=RED)

def ic_hemicycle(box):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, y1 - 6
    d.pieslice([cx - 30, cy - 30, cx + 30, cy + 30], 180, 360, fill=(150, 170, 210), outline=INK, width=2)
    import math
    for i, ang in enumerate((200, 225, 250, 270, 290, 315, 340)):
        a = math.radians(ang)
        px, py = cx + 20 * math.cos(a), cy + 20 * math.sin(a)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED if i < 5 else NAVY)
    d.rectangle([cx - 34, cy - 2, cx + 34, cy + 4], fill=INK)

def ic_factory(box):
    x0, y0, x1, y1 = box
    d.rectangle([x0 + 20, y1 - 20, x1 - 20, y1 - 6], fill=(120, 120, 124))
    d.polygon([(x0 + 20, y1 - 20), (x0 + 34, y1 - 32), (x0 + 48, y1 - 20)], fill=(120, 120, 124))
    d.polygon([(x0 + 48, y1 - 20), (x0 + 62, y1 - 32), (x0 + 76, y1 - 20)], fill=(120, 120, 124))
    d.rectangle([x0 + 96, y1 - 34, x1 - 30, y1 - 6], fill=(90, 90, 94))
    d.rectangle([x1 - 26, y1 - 40, x1 - 20, y1 - 6], fill=(90, 90, 94))
    for wx in (x0 + 30, x0 + 52, x0 + 74, x0 + 104):
        d.rectangle([wx, y1 - 16, wx + 8, y1 - 8], fill=(250, 220, 90))

def ic_plane(box):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.polygon([(cx - 34, cy + 2), (cx + 26, cy - 8), (cx + 36, cy - 2), (cx + 26, cy + 2),
               (cx + 10, cy + 2), (cx + 4, cy + 12), (cx - 2, cy + 12), (cx - 8, cy + 2),
               (cx - 26, cy + 8), (cx - 30, cy + 4)], fill=(70, 70, 74))
    d.line([cx - 20, cy - 14, cx - 30, cy - 22], fill=(150, 148, 140), width=3)
    d.ellipse([cx - 34, cy - 26, cx - 22, cy - 14], fill=(150, 148, 140))

def ic_gavel(box):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.line([cx - 24, cy + 14, cx + 24, cy - 14], fill=(120, 72, 32), width=5)
    d.rectangle([cx - 6, cy - 18, cx + 18, cy - 6], fill=(90, 54, 24))
    d.rectangle([cx - 30, cy + 12, cx + 30, cy + 18], fill=(150, 110, 60))

def ic_flag_us(box):
    x0, y0, x1, y1 = box
    flag(x0 + 20, y0 + 8, 60, 30, [(178, 34, 52), (255, 255, 255), (178, 34, 52), (255, 255, 255), (178, 34, 52)])
    d.rectangle([x0 + 20, y0 + 8, x0 + 44, y0 + 22], fill=(40, 60, 120))
    ic_virus([x1 - 52, y0 + 4, x1 - 12, y0 + 44], col=RED)

# ---------------- content ----------------
LEADS = [
    dict(n=1, kick="EUROPE · UKRAINE WAR", col=C_EU, art=art_bridge,
         head="Ukraine says Crimean Bridge span fell",
         deck="Second straight day of strikes; rail arch stands, damaged; 2 killed, traffic halted, rail resumed Tuesday."),
    dict(n=2, kick="MIDDLE EAST · IRAN WAR", col=C_ME, art=art_gulf,
         head="US hits Qeshm; Iran drones Bahrain radar",
         deck="US jets strike an IRGC missile site; tanker Tara Gas hit twice, 1 seafarer missing; Kuwait fires on drones."),
    dict(n=3, kick="ASIA · DIPLOMACY", col=C_AS, art=art_quad,
         head="Trump holds first Quad summit in Manila",
         deck="ASEAN and Quad leaders meet; first-ever Trump–Xi–Putin trilateral confirmed for Thursday in Shenzhen."),
]

SMALLS = [
    dict(n=4, kick="AFRICA · HEALTH", col=C_AF, art=lambda b: ic_virus(b),
         tag="11,254 CASES", head="Ebola cases in DR Congo top 11,254",
         deck="Reuters data review: 5,505 deaths in six months."),
    dict(n=5, kick="GLOBAL · CLIMATE", col=C_GL, art=ic_globe,
         tag="DRAFT: PHASE OUT?", head="COP31 split over fossil fuels",
         deck="Draft under fire as ministers take over in Antalya."),
    dict(n=6, kick="AMERICAS · HEALTH", col=C_AM, art=ic_flag_us,
         tag="STATUS LOST", head="US loses measles-free status",
         deck="PAHO ruling ends 26 years of elimination status."),
    dict(n=7, kick="US · BUSINESS", col=C_AM, art=ic_chip,
         tag="$115.8BN", head="Nvidia's sales double to $115.8bn",
         deck="Revenue +103% a year; Huang will not return."),
    dict(n=8, kick="MIDDLE EAST · GAZA", col=C_ME, art=ic_tents,
         tag="WINTER AID HELD UP", head="Gaza winter rains flood shelters",
         deck="UN warns of flooding; four nations urge aid in."),
    dict(n=9, kick="ASIA · POLITICS", col=C_AS, art=ic_letter,
         tag="RESIGNATION", head="Mongolia's president to resign",
         deck="Khürelsükh quits over alleged railway-project graft."),
    dict(n=10, kick="EUROPE · POLITICS", col=C_EU, art=ic_hemicycle,
         tag="STUDENTS 140", head="Serbia's student majority seated",
         deck="Student List: 140 of 250 seats; Vučić era ends."),
    dict(n=11, kick="ASIA · LABOUR", col=C_AS, art=ic_factory,
         tag="TK 30,000", head="Bangladesh police tear-gas workers",
         deck="Workers demand Tk 30,000 a month, up from 12,500."),
    dict(n=12, kick="RUSSIA · AIR CRASH", col=C_EU, art=ic_plane,
         tag="ALL 19 ABOARD KILLED", head="An-12 crash in Siberia kills all 19",
         deck="Military plane down near Kemerovo; no survivors."),
    dict(n=13, kick="AFRICA · JUSTICE", col=C_AF, art=ic_gavel,
         tag="5 CHARGES", head="Mozambique tries opposition leader",
         deck="Mondlane faces 5 charges, up to 24 years in jail."),
]

BRIEFS = [
    (14, "Russia: says it downed 1,441 drones overnight", (37.6, 55.7), C_EU),
    (15, "Kyiv: Russia hits two bridges in reply", (30.5, 50.4), C_EU),
    (16, "Japan: jets scrambled over airspace breach", (133.0, 35.5), C_AS),
    (17, "Cyclone Akvan: 610 km east of Chennai", (80.3, 13.1), C_AS),
    (18, "Apple: iCloud, Pay and App Store outage", (-122.0, 37.3), C_AM),
    (19, "NSA: classified network goes dark", (-76.8, 39.1), C_AM),
    (20, "Dow −849 to 50,759; S&P lowest since July", (-74.0, 40.7), C_AM),
    (21, "UK: sanctions 8 firms over West Bank building", (-0.1, 51.5), C_EU),
    (22, "Depardieu: drops appeal, accepts sentence", (2.35, 48.85), C_EU),
    (23, "Moldova: 7 drones cross airspace in 2.5 hrs", (28.8, 47.0), C_EU),
    (24, "Equinor: cyberattack hits top gas supplier", (5.7, 58.9), C_EU),
    (25, "N. Macedonia: 5 held over alleged Iran plot", (21.4, 42.0), C_EU),
    (26, "Czech Republic: 4 rail incidents in two days", (14.4, 50.1), C_EU),
    (27, "California: sues OpenAI over AI safety", (-121.5, 38.6), C_AM),
    (28, "UK: ~1m young people out of work or study", (-0.3, 51.5), C_EU),
    (29, "GTA 6: launches Thursday after 13-year wait", (-3.2, 55.95), C_EU),
    (30, "Tiger Woods: comeback set for December", (-77.4, 25.0), C_AM),
    (31, "US Senate: energy bill advances 70–27", (-77.0, 38.9), C_AM),
    (32, "West Bank: settler kills woman, 72", (35.45, 31.85), C_ME),
    (33, "Dubai: airport traffic down 28% in 2026", (55.3, 25.2), C_ME),
    (34, "Bulgaria: gas tanker sinks in Black Sea", (28.0, 43.0), C_EU),
    (35, "Yemen: Houthis close on Aden; 7 die in strike", (45.0, 12.8), C_ME),
    (36, "France: public-sector strike; 146,000 march", (2.35, 48.9), C_EU),
    (37, "Poland: Tusk survives no-confidence vote", (21.0, 52.2), C_EU),
    (38, "Germany: Deutsche Bank falls after data leak", (8.68, 50.1), C_EU),
    (39, "Turkey: police seize broadcaster Sözcü TV", (29.0, 41.0), C_ME),
    (40, "Football: Norway beat Denmark 3–2", (10.75, 59.9), C_EU),
    (41, "Vatican: Pope Leo XIV back from S. America", (12.45, 41.9), C_EU),
    (42, "Israel: Knesset elects speaker, 66–52", (35.2, 31.8), C_ME),
    (43, "Australia: eases backpacker visa curbs", (149.1, -35.3), C_OC),
]

PINS = [  # (n, lon, lat, colour) — stories 1–13
    (1, 37.5, 45.3, C_EU), (2, 53.0, 26.5, C_ME), (3, 121.0, 14.6, C_AS),
    (4, 25.2, -0.5, C_AF), (5, 30.7, 36.9, C_GL), (6, -77.0, 39.0, C_AM),
    (7, -122.0, 37.4, C_AM), (8, 34.5, 31.5, C_ME), (9, 106.9, 47.9, C_AS),
    (10, 20.5, 44.8, C_EU), (11, 90.4, 23.8, C_AS), (12, 86.1, 55.3, C_EU),
    (13, 32.6, -25.9, C_AF),
]

# ---------------- layout ----------------
MX = 24
CW = W - 2 * MX  # 976

# Kicker
d.text((MX, 12), "THE WORLD'S NEWS IN ONE PICTURE", font=F_SANS_B(13), fill=RED)
cnt = "43 STORIES · 6 CONTINENTS · ALL FROM TUESDAY"
d.text((W - MX - d.textlength(cnt, font=F_SANS_B(13)), 12), cnt, font=F_SANS_B(13), fill=INK)

# Masthead
mast = "Tuesday 17 November 2026"
mf = F_SERIF_B(64)
mw = d.textlength(mast, font=mf)
d.text(((W - mw) / 2, 30), mast, font=mf, fill=INK)
d.line([MX, 104, W - MX, 104], fill=INK, width=2)
d.line([MX, 108, W - MX, 108], fill=INK, width=1)

# Stat strip
stats = [("11,254", "EBOLA CASES"), ("$115.8BN", "NVIDIA QUARTER"),
         ("−849", "DOW POINTS"), ("1,441", "DRONES RUSSIA SAYS DOWNED"),
         ("140/250", "SERBIA SEATS")]
sx = MX
sy = 116
seg_w = CW // len(stats)
for num, lab in stats:
    d.text((sx + 6, sy), num, font=F_SANS_B(15), fill=RED)
    d.text((sx + 6, sy + 17), lab, font=F_SANS_B(9), fill=GREY)
    sx += seg_w
d.line([MX, 152, W - MX, 152], fill=(200, 194, 178), width=1)

# Lead cards
LW = (CW - 2 * 12) // 3  # 317
LH = 258
LY = 160
ART_H = 140
for i, L in enumerate(LEADS):
    x0 = MX + i * (LW + 12)
    x1 = x0 + LW
    y0, y1 = LY, LY + LH
    d.rectangle([x0, y0, x1, y1], fill=CARD_BG, outline=LINE, width=1)
    L["art"]((x0 + 1, y0 + 1, x1 - 1, y0 + ART_H))
    d.line([x0, y0 + ART_H, x1, y0 + ART_H], fill=LINE, width=1)
    ty = y0 + ART_H + 7
    d.text((x0 + 8, ty), f"{L['n']}", font=F_SANS_B(12), fill=L["col"])
    d.text((x0 + 8 + d.textlength(str(L['n']), font=F_SANS_B(12)) + 5, ty), L["kick"], font=F_SANS_B(11), fill=L["col"])
    ty += 15
    hl = wrap(L["head"], F_SERIF_B(20), LW - 16)
    fit_check(hl, 2, f"lead {L['n']} head")
    ty = draw_lines(hl, x0 + 8, ty, F_SERIF_B(20), INK, 23)
    dl = wrap(L["deck"], F_SANS(12), LW - 16)
    fit_check(dl, 3, f"lead {L['n']} deck")
    draw_lines(dl, x0 + 8, ty + 2, F_SANS(12), GREY, 14)

# Small cards: 2 rows x 5
SW = (CW - 4 * 10) // 5  # 187
SH = 122
SY0 = LY + LH + 8
for r in range(2):
    for c in range(5):
        S = SMALLS[r * 5 + c]
        x0 = MX + c * (SW + 10)
        x1 = x0 + SW
        y0 = SY0 + r * (SH + 8)
        y1 = y0 + SH
        d.rectangle([x0, y0, x1, y1], fill=CARD_BG, outline=LINE, width=1)
        # art strip with tag
        ax0, ay0, ax1, ay1 = x0 + 1, y0 + 1, x1 - 1, y0 + 44
        d.rectangle([ax0, ay0, ax1, ay1], fill=(233, 230, 220))
        S["art"]((ax0, ay0, ax1, ay1))
        label_tag(ax1 - 8 - d.textlength(S["tag"], font=F_SANS_B(9)) - 10, ay0 + 4,
                  S["tag"], F_SANS_B(9), bg=NAVY)
        d.line([x0, y0 + 44, x1, y0 + 44], fill=LINE, width=1)
        ty = y0 + 48
        d.text((x0 + 6, ty), f"{S['n']}", font=F_SANS_B(11), fill=S["col"])
        d.text((x0 + 6 + d.textlength(str(S['n']), font=F_SANS_B(11)) + 5, ty), S["kick"], font=F_SANS_B(10), fill=S["col"])
        ty += 13
        hl = wrap(S["head"], F_SANS_B(13), SW - 12)
        fit_check(hl, 2, f"small {S['n']} head")
        ty = draw_lines(hl, x0 + 6, ty, F_SANS_B(13), INK, 14)
        dl = wrap(S["deck"], F_SANS(11), SW - 12)
        fit_check(dl, 2, f"small {S['n']} deck")
        draw_lines(dl, x0 + 6, ty + 1, F_SANS(11), GREY, 12)

# ---------------- bottom band: map + briefs ----------------
BY = SY0 + 2 * SH + 8 + 8  # 666
MAP_W, MAP_H = 380, 220
MAP_X, MAP_Y = MX, BY + 22
BR_X = MX + MAP_W + 12  # 416
BR_W = W - MX - BR_X    # 584
COL_W = (BR_W - 12) // 2  # 286

d.text((MX, BY), "WHERE IT HAPPENED · PINS 1–13, DOTS 14–43", font=F_SANS_B(12), fill=RED)
d.text((BR_X, BY), "ALSO ON TUESDAY 17 NOVEMBER", font=F_SANS_B(12), fill=RED)

# map: sea + dotted continents
d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H], fill=(206, 224, 236), outline=LINE, width=1)
def to_px(lon, lat):
    return (MAP_X + (lon + 180) / 360 * MAP_W, MAP_Y + (85 - lat) / 145 * MAP_H)
step = 7
gx, gy = MAP_X + 3, MAP_Y + 3
while gy < MAP_Y + MAP_H - 3:
    lon = (gx - MAP_X) / MAP_W * 360 - 180
    lat = 85 - (gy - MAP_Y) / MAP_H * 145
    if on_land(lon, lat):
        d.ellipse([gx - 1.6, gy - 1.6, gx + 1.6, gy + 1.6], fill=LAND_DOT)
    gx += step
    if gx >= MAP_X + MAP_W - 3:
        gx = MAP_X + 3
        gy += step
# brief dots first (under pins)
for n, txt, (lon, lat), col in BRIEFS:
    px, py = to_px(lon, lat)
    d.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5], fill=col, outline=(255, 255, 255), width=1)
# numbered pins 1-13
for n, lon, lat, col in PINS:
    px, py = to_px(lon, lat)
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=col, outline=(255, 255, 255), width=2)
    t = str(n)
    tw = d.textlength(t, font=F_SANS_B(10))
    d.text((px - tw / 2, py - 7), t, font=F_SANS_B(10), fill=(255, 255, 255))

# legend
ly = MAP_Y + MAP_H + 8
lx = MX
for lab, col in [("Americas", C_AM), ("Europe", C_EU), ("Middle East", C_ME),
                 ("Asia", C_AS), ("Africa", C_AF), ("Oceania", C_OC)]:
    d.ellipse([lx, ly, lx + 8, ly + 8], fill=col)
    d.text((lx + 11, ly - 1), lab, font=F_SANS(10), fill=INK)
    lx += 11 + d.textlength(lab, font=F_SANS(10)) + 10

# briefs: 2 columns x 15, one line each
bf = F_SANS(11)
bn = F_SANS_B(11)
by = BY + 20
for col_i in range(2):
    bx = BR_X + col_i * (COL_W + 12)
    for row in range(15):
        n, txt, _, _ = BRIEFS[col_i * 15 + row]
        y = by + row * 16
        d.text((bx, y), f"{n}", font=bn, fill=RED)
        tw = d.textlength(txt, font=bf)
        if tw > COL_W - 24:
            raise SystemExit(f"BRIEF {n} TOO LONG ({tw:.0f}px > {COL_W - 24}px): {txt}")
        d.text((bx + 22, y), txt, font=bf, fill=INK)
        d.line([bx, y + 14, bx + COL_W, y + 14], fill=(220, 214, 198), width=1)

# ---------------- footer ----------------
fy = BY + 20 + 15 * 16 + 10
d.line([MX, fy - 6, W - MX, fy - 6], fill=INK, width=1)
d.text((MX, fy), "Every story here happened or was first reported on Tuesday 17 November 2026. Contested claims are marked as claims.",
       font=F_SANS(11), fill=INK)
d.text((MX, fy + 15), "Sources: Reuters, AP, AFP, BBC, Al Jazeera, WHO, UN. Original drawings.",
       font=F_SANS(11), fill=GREY)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, format="PNG", optimize=True)
print("saved", out, os.path.getsize(out), "bytes")
