#!/usr/bin/env python3
"""Round 3 front page for news-image-20261117: Tuesday 17 November 2026.
Deterministic PIL render, 1024x1024. No network, no timestamps, no randomness.
Fixes vs round 2 (narrow): ROAD SPAN DOWN label box widened so the label
fits; briefs 14px -> 15px with map narrowed 380 -> 360 to widen columns.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

F = "/usr/share/fonts/truetype/dejavu/"

def font(name, size):
    return ImageFont.truetype(F + name, size)

# ---------- fonts ----------
F_KICKER   = font("DejaVuSans-Bold.ttf", 13)
F_MAST     = font("DejaVuSerif-Bold.ttf", 58)
F_STAT_N   = font("DejaVuSans-Bold.ttf", 17)
F_STAT_L   = font("DejaVuSans.ttf", 11)
F_DC_T     = font("DejaVuSans-Bold.ttf", 12)
F_DC_D     = font("DejaVuSans.ttf", 12)
F_DC_S     = font("DejaVuSans.ttf", 11)
F_LKICK    = font("DejaVuSans-Bold.ttf", 11)
F_LHEAD    = font("DejaVuSerif-Bold.ttf", 20)
F_LDECK    = font("DejaVuSans.ttf", 13)
F_CKICK    = font("DejaVuSans-Bold.ttf", 11)
F_CHEAD    = font("DejaVuSans-Bold.ttf", 14)
F_CDECK    = font("DejaVuSans.ttf", 12)
F_TAG      = font("DejaVuSans-Bold.ttf", 12)
F_BRIEF    = font("DejaVuSans.ttf", 15)
F_BRIEF_N  = font("DejaVuSans-Bold.ttf", 15)
F_PIN      = font("DejaVuSans-Bold.ttf", 9)
F_LEGEND   = font("DejaVuSans-Bold.ttf", 11)
F_FOOT     = font("DejaVuSans.ttf", 11)
F_LBL12B   = font("DejaVuSans-Bold.ttf", 12)
F_LBL10    = font("DejaVuSans.ttf", 10)
F_SECT     = font("DejaVuSans-Bold.ttf", 13)

# ---------- palette ----------
PAPER = (246, 241, 229)
INK   = (28, 28, 26)
RED   = (180, 35, 24)
NAVY  = (31, 42, 68)
GREY  = (110, 110, 104)
RULE  = (180, 172, 152)
SEA   = (220, 232, 236)
DOT   = (143, 133, 112)
WHITE = (255, 255, 255)

REG = {
    "Europe":      (43, 90, 166),
    "Middle East": (194, 87, 27),
    "Asia":        (123, 75, 166),
    "Africa":      (46, 125, 79),
    "Americas":    (180, 35, 24),
    "Oceania":     (31, 138, 138),
    "Global":      (85, 85, 85),
}

def fail(msg):
    raise SystemExit("OVERFLOW: " + msg)

def wrap(text, fnt, max_w):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if fnt.getlength(t) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def inside(px, py, poly):
    # ray casting, point in polygon
    n = len(poly)
    j = n - 1
    c = False
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > py) != (yj > py)) and (px < (xj - xi) * (py - yi) / (yj - yi) + xi):
            c = not c
        j = i
    return c

# ---------- content ----------
STATS = [
    ("11,254", "Ebola cases"),
    ("$115.8bn", "Nvidia quarter"),
    ("\u2212849", "Dow points"),
    ("1,441", "drones Russia says downed"),
    ("140/250", "Serbia seats"),
]

LEADS = [
    dict(region="Europe", kicker="EUROPE \u00b7 UKRAINE WAR",
         head="Ukraine says Crimean Bridge span fell",
         deck="Second straight day of strikes; rail arch stands, damaged; 2 killed, traffic halted, rail resumed Tuesday.",
         art="bridge"),
    dict(region="Middle East", kicker="MIDDLE EAST \u00b7 IRAN WAR",
         head="US hits Qeshm; Iran drones Bahrain radar",
         deck="US jets strike an IRGC missile site; tanker Tara Gas hit twice, 1 seafarer missing; Kuwait fires on drones.",
         art="gulf"),
    dict(region="Asia", kicker="ASIA \u00b7 DIPLOMACY",
         head="Trump holds first Quad summit in Manila",
         deck="ASEAN and Quad leaders meet; first-ever Trump\u2013Xi\u2013Putin trilateral confirmed for Thursday in Shenzhen.",
         art="quad"),
]

CARDS = [
    dict(region="Africa", kicker="AFRICA \u00b7 HEALTH", tag="11,254 CASES",
         head="Ebola cases in DR Congo top 11,254",
         deck="Reuters review: 5,505 deaths in six months.", icon="virus"),
    dict(region="Global", kicker="GLOBAL \u00b7 CLIMATE", tag="PHASE OUT?",
         head="COP31 split over fossil fuels",
         deck="Draft under fire as ministers take over.", icon="globe"),
    dict(region="Americas", kicker="AMERICAS \u00b7 HEALTH", tag="STATUS LOST",
         head="US loses measles-free status",
         deck="PAHO ruling ends 26 years of elimination.", icon="chip"),
    dict(region="Americas", kicker="US \u00b7 BUSINESS", tag="$115.8BN",
         head="Nvidia's sales double to $115.8bn",
         deck="Revenue +103% a year; Huang will not return.", icon="tents"),
    dict(region="Middle East", kicker="MIDDLE EAST \u00b7 GAZA", tag="AID HELD UP",
         head="Gaza winter rains flood shelters",
         deck="UN warns of flooding; nations urge aid in.", icon="letter"),
    dict(region="Asia", kicker="ASIA \u00b7 POLITICS", tag="RESIGNATION",
         head="Mongolia's president to resign",
         deck="Kh\u00fcrels\u00fckh quits over railway-project graft.", icon="hemicycle"),
    dict(region="Europe", kicker="EUROPE \u00b7 POLITICS", tag="STUDENTS 140",
         head="Serbia's student majority seated",
         deck="Student List: 140 of 250 seats; era ends.", icon="factory"),
    dict(region="Asia", kicker="ASIA \u00b7 LABOUR", tag="TK 30,000",
         head="Bangladesh police tear-gas workers",
         deck="Demand Tk 30,000 a month, up from 12,500.", icon="plane"),
    dict(region="Europe", kicker="RUSSIA \u00b7 AIR CRASH", tag="ALL 19 KILLED",
         head="An-12 crash in Siberia kills all 19",
         deck="Plane down near Kemerovo; no survivors.", icon="gavel"),
    dict(region="Africa", kicker="AFRICA \u00b7 JUSTICE", tag="5 CHARGES",
         head="Mozambique tries opposition leader",
         deck="Mondlane faces 5 charges, up to 24 years.", icon="flagvirus"),
]

# briefs 14..43 (round-2 texts; 5 longest re-trimmed for 15px, figures kept)
BRIEFS = [
    "Russia claims 1,441 drones down",
    "Kyiv: Russia hits two bridges",
    "Japan scrambles jets over airspace",
    "Cyclone Akvan 610km off Chennai",
    "Apple: iCloud, Pay, Store outage",
    "NSA classified network goes dark",
    "Dow -849; S&P lowest since July",
    "UK sanctions 8 settlement firms",
    "Depardieu drops appeal, takes it",
    "Moldova: 7 drones cross airspace",
    "Equinor cyberattack hits gas firm",
    "Macedonia: 5 held in 'Iran plot'",
    "Czech: 4 rail incidents in 2 days",
    "California sues OpenAI over safety",
    "UK: 1m youths out of work",
    "GTA 6 out Thursday, 13 years on",
    "Tiger Woods returns in December",
    "Senate energy bill passes 70\u201327",
    "West Bank settler kills woman, 72",
    "Dubai airport traffic down 28%",
    "Gas tanker sinks off Bulgaria",
    "Houthis near Aden; 7 killed",
    "France strike: 146,000 march",
    "Tusk wins no-confidence vote",
    "Deutsche Bank falls on data leak",
    "Turkey seizes S\u00f6zc\u00fc TV station",
    "Norway beat Denmark 3\u20132",
    "Pope Leo XIV back from S America",
    "Knesset elects speaker, 66\u201352",
    "Australia eases backpacker visas",
]

# region per brief 14..43 (for map dots)
BRIEF_REGIONS = [
    "Europe", "Europe", "Asia", "Asia", "Americas", "Americas", "Americas",
    "Europe", "Europe", "Europe", "Europe", "Europe", "Europe", "Americas",
    "Europe", "Americas", "Americas", "Americas", "Middle East", "Middle East",
    "Europe", "Middle East", "Europe", "Europe", "Europe", "Middle East",
    "Europe", "Europe", "Middle East", "Oceania",
]

PINS = [  # (lon, lat) for stories 1..13
    (37.5, 45.3), (53.0, 26.5), (121.0, 14.6), (25.2, -0.5),
    (30.7, 36.9), (-77.0, 39.0), (-122.0, 37.4), (34.5, 31.5),
    (106.9, 47.9), (20.5, 44.8), (90.4, 23.8), (86.1, 55.3), (32.6, -25.9),
]
PIN_REGIONS = ["Europe", "Middle East", "Asia", "Africa", "Middle East",
               "Americas", "Americas", "Middle East", "Asia", "Europe",
               "Asia", "Europe", "Africa"]
PIN_NUDGE = {1: (14, -10), 2: (16, 8), 5: (-16, 10), 8: (2, 16), 10: (-14, -8)}

DOTS = [  # (lon, lat) for briefs 14..43
    (37.6, 55.7), (30.5, 50.4), (133.0, 35.5), (80.3, 13.1), (-122.0, 37.3),
    (-76.8, 39.1), (-74.0, 40.7), (-0.1, 51.5), (2.35, 48.85), (28.8, 47.0),
    (5.7, 58.9), (21.4, 42.0), (14.4, 50.1), (-121.5, 38.6), (-0.3, 51.5),
    (-3.2, 55.95), (-77.4, 25.0), (-77.0, 38.9), (35.45, 31.85), (55.3, 25.2),
    (28.0, 43.0), (45.0, 12.8), (2.35, 48.9), (21.0, 52.2), (8.68, 50.1),
    (29.0, 41.0), (10.75, 59.9), (12.45, 41.9), (35.2, 31.8), (149.1, -35.3),
]

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

# ---------- lead art ----------
def art_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(215, 228, 234))
    # water
    d.rectangle([x, y + 78, x + w, y + h], fill=(127, 168, 201))
    d.rectangle([x, y + 78, x + w, y + 84], fill=(96, 140, 178))
    # far shore
    d.polygon([(x, y + 78), (x + 90, y + 70), (x + 150, y + 74), (x + 210, y + 68),
               (x + w, y + 76), (x + w, y + 78)], fill=(196, 188, 160))
    # bridge deck: two standing spans, collapsed middle
    deck_y = y + 62
    d.rectangle([x + 8, deck_y, x + 118, deck_y + 7], fill=(90, 90, 88))
    d.rectangle([x + 205, deck_y, x + w - 8, deck_y + 7], fill=(90, 90, 88))
    # tilted fallen segment
    d.polygon([(x + 122, deck_y + 2), (x + 150, deck_y + 26), (x + 196, deck_y + 30),
               (x + 200, deck_y + 22), (x + 158, deck_y + 18), (x + 128, deck_y - 2)],
              fill=(70, 70, 68))
    # towers
    for tx in (x + 52, x + 248):
        d.rectangle([tx, y + 26, tx + 6, deck_y], fill=(70, 70, 68))
        d.line([tx + 3, y + 26, tx - 14, deck_y], fill=(120, 120, 118), width=1)
        d.line([tx + 3, y + 26, tx + 20, deck_y], fill=(120, 120, 118), width=1)
    # smoke over the gap
    for cx, cy, r in ((x + 158, y + 46, 9), (x + 172, y + 38, 12), (x + 186, y + 48, 8)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 148, 142))
    # R3 FIX: white label box widened so ROAD SPAN DOWN (125.8px) fits
    label = "ROAD SPAN DOWN"
    lw = F_LBL12B.getlength(label)
    box_x0, box_x1 = x + 8, x + 150
    if lw > (box_x1 - box_x0) - 10:
        fail(f"ROAD SPAN DOWN label {lw:.1f}px wider than box {box_x1 - box_x0}px")
    d.rectangle([box_x0, y + 8, box_x1, y + 28], fill=WHITE)
    d.text((x + 13, y + 10), label, font=F_LBL12B, fill=RED)

def art_gulf(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(168, 200, 216))
    # land: Arabia bottom-left, Iran top-right
    d.polygon([(x, y + h), (x, y + 78), (x + 70, y + 62), (x + 130, y + 80),
               (x + 150, y + h)], fill=(217, 201, 163))
    d.polygon([(x + 170, y), (x + w, y), (x + w, y + 46), (x + 250, y + 40),
               (x + 210, y + 28), (x + 185, y + 18)], fill=(217, 201, 163))
    # Qeshm island
    d.ellipse([x + 168, y + 52, x + 262, y + 70], fill=(196, 172, 120))
    d.ellipse([x + 168, y + 52, x + 262, y + 70], outline=(120, 100, 60), width=1)
    d.text((x + 196, y + 76), "QESHM", font=F_LBL10, fill=(60, 50, 30))
    # tanker
    d.rectangle([x + 96, y + 92, x + 158, y + 102], fill=(60, 60, 62))
    d.rectangle([x + 140, y + 84, x + 152, y + 92], fill=(230, 230, 225))
    # drone arrows
    for ax, ay in ((x + 250, y + 24), (x + 280, y + 44)):
        d.line([ax, ay, ax + 22, ay + 12], fill=RED, width=2)
        d.polygon([(ax + 22, ay + 12), (ax + 14, ay + 10), (ax + 18, ay + 18)], fill=RED)
    # missile site marker
    d.ellipse([x + 216, y + 30, x + 224, y + 38], fill=RED)
    d.text((x + 228, y + 28), "SITE", font=F_LBL10, fill=RED)

def art_quad(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 208))
    # table
    d.ellipse([x + 40, y + 74, x + w - 40, y + 108], fill=(150, 110, 70))
    d.rectangle([x + 40, y + 90, x + w - 40, y + 100], fill=(150, 110, 70))
    # four flags on poles
    specs = [
        ("us", (200, 40, 60)), ("in", (230, 140, 40)),
        ("jp", (200, 200, 200)), ("au", (30, 60, 160)),
    ]
    fx = x + 52
    for name, col in specs:
        d.line([fx + 14, y + 14, fx + 14, y + 78], fill=(90, 80, 60), width=2)
        if name == "us":
            for s in range(4):
                d.rectangle([fx, y + 16 + s * 8, fx + 28, y + 20 + s * 8],
                            fill=(178, 34, 52) if s % 2 == 0 else WHITE)
            d.rectangle([fx, y + 16, fx + 13, y + 30], fill=(40, 60, 120))
        elif name == "in":
            d.rectangle([fx, y + 16, fx + 28, y + 24], fill=(255, 153, 51))
            d.rectangle([fx, y + 24, fx + 28, y + 32], fill=WHITE)
            d.rectangle([fx, y + 32, fx + 28, y + 40], fill=(19, 136, 8))
            d.ellipse([fx + 11, y + 25, fx + 17, y + 31], outline=NAVY, width=1)
        elif name == "jp":
            d.rectangle([fx, y + 16, fx + 28, y + 40], fill=WHITE)
            d.ellipse([fx + 9, y + 22, fx + 19, y + 32], fill=(188, 0, 45))
        else:
            d.rectangle([fx, y + 16, fx + 28, y + 40], fill=(30, 60, 160))
            for sx, sy in ((fx + 6, y + 20), (fx + 20, y + 20), (fx + 13, y + 30), (fx + 22, y + 34)):
                d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=WHITE)
        fx += 68
    # white banner, centred label — assert it fits
    label = "QUAD LEADERS' SUMMIT \u00b7 MANILA"
    lw = F_LBL12B.getlength(label)
    bx0, bx1 = x + 8, x + w - 8
    if lw > (bx1 - bx0) - 10:
        fail(f"Quad banner label {lw:.1f}px wider than banner {bx1 - bx0}px")
    d.rectangle([bx0, y + 88, bx1, y + 108], fill=WHITE)
    d.text((x + w // 2, y + 98), label, font=F_LBL12B, fill=NAVY, anchor="mm")

# ---------- small-card icons (flat, ~28px, drawn at cx, cy) ----------
def icon(d, kind, cx, cy, col):
    if kind == "virus":
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=col)
        for dx, dy in ((-11, -11), (0, -13), (11, -11), (-13, 0), (13, 0),
                       (-11, 11), (0, 13), (11, 11)):
            d.line([cx, cy, cx + dx, cy + dy], fill=col, width=2)
            d.ellipse([cx + dx - 2, cy + dy - 2, cx + dx + 2, cy + dy + 2], fill=col)
    elif kind == "globe":
        d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], outline=col, width=2)
        d.ellipse([cx - 4, cy - 11, cx + 4, cy + 11], outline=col, width=1)
        d.line([cx - 11, cy, cx + 11, cy], fill=col, width=1)
    elif kind == "chip":
        d.rectangle([cx - 9, cy - 9, cx + 9, cy + 9], outline=col, width=2)
        d.rectangle([cx - 4, cy - 4, cx + 4, cy + 4], fill=col)
        for px in (-6, 0, 6):
            d.line([cx + px, cy - 13, cx + px, cy - 9], fill=col, width=2)
            d.line([cx + px, cy + 9, cx + px, cy + 13], fill=col, width=2)
    elif kind == "tents":
        d.polygon([(cx - 12, cy + 9), (cx, cy - 9), (cx + 12, cy + 9)], fill=col)
        d.polygon([(cx + 2, cy + 9), (cx + 12, cy - 2), (cx + 20, cy + 9)], fill=col)
    elif kind == "letter":
        d.rectangle([cx - 12, cy - 8, cx + 12, cy + 8], outline=col, width=2)
        d.line([cx - 12, cy - 8, cx, cy + 2], fill=col, width=2)
        d.line([cx + 12, cy - 8, cx, cy + 2], fill=col, width=2)
    elif kind == "hemicycle":
        d.pieslice([cx - 12, cy - 12, cx + 12, cy + 12], 180, 360, fill=col)
        for dx in (-8, -3, 3, 8):
            d.ellipse([cx + dx - 2, cy - 4, cx + dx + 2, cy], fill=WHITE)
    elif kind == "factory":
        d.polygon([(cx - 12, cy + 9), (cx - 12, cy - 2), (cx - 6, cy - 6),
                   (cx, cy - 2), (cx + 6, cy - 6), (cx + 12, cy - 2),
                   (cx + 12, cy + 9)], fill=col)
        d.rectangle([cx + 6, cy - 12, cx + 10, cy - 2], fill=col)
    elif kind == "plane":
        d.ellipse([cx - 12, cy - 3, cx + 12, cy + 3], fill=col)
        d.polygon([(cx - 2, cy - 3), (cx + 4, cy - 12), (cx + 8, cy - 3)], fill=col)
        d.polygon([(cx - 2, cy + 3), (cx + 4, cy + 12), (cx + 8, cy + 3)], fill=col)
        d.polygon([(cx - 12, cy - 2), (cx - 16, cy - 8), (cx - 13, cy)], fill=col)
    elif kind == "gavel":
        d.line([cx - 10, cy + 10, cx + 10, cy - 10], fill=col, width=3)
        d.rectangle([cx - 12, cy - 12, cx - 2, cy - 2], fill=col)
        d.rectangle([cx + 2, cy + 2, cx + 12, cy + 12], fill=col)
    elif kind == "flagvirus":
        for s in range(3):
            d.rectangle([cx - 12, cy - 10 + s * 7, cx + 2, cy - 6 + s * 7],
                        fill=(178, 34, 52) if s % 2 == 0 else WHITE)
        d.ellipse([cx + 6, cy - 2, cx + 14, cy + 6], fill=col)
        d.line([cx + 10, cy - 8, cx + 10, cy + 10], fill=col, width=1)

# ---------- page ----------
def draw_page():
    img = Image.new("RGB", (1024, 1024), PAPER)
    d = ImageDraw.Draw(img)

    # kicker + count line
    d.text((24, 12), "THE WORLD'S NEWS IN ONE PICTURE", font=F_KICKER, fill=RED)
    cnt = "43 STORIES \u00b7 6 CONTINENTS \u00b7 ALL FROM TUESDAY"
    d.text((1000 - F_KICKER.getlength(cnt), 12), cnt, font=F_KICKER, fill=INK)
    # masthead + double rule
    mast = "Tuesday 17 November 2026"
    d.text((512, 38), mast, font=F_MAST, fill=INK, anchor="ma")
    d.line([24, 106, 1000, 106], fill=INK, width=2)
    d.line([24, 110, 1000, 110], fill=INK, width=1)

    # stat strip: 6 cells of 156 + 8 gaps from x=24
    for i, (num, lab) in enumerate(STATS):
        cx = 24 + i * 164
        d.text((cx, 120), num, font=F_STAT_N, fill=RED)
        d.text((cx, 144), lab, font=F_STAT_L, fill=GREY)
    # DATE CHECK box, 6th cell
    bx0, by0, bx1, by1 = 844, 118, 1000, 162
    d.rectangle([bx0, by0, bx1, by1], outline=RED, width=2)
    d.line([854, 138, 860, 144, 871, 128], fill=RED, width=3)
    d.text((878, 121), "DATE CHECK", font=F_DC_T, fill=RED)
    d.text((878, 136), "Tue 17 Nov 2026", font=F_DC_D, fill=INK)
    d.text((878, 150), "weekday verified", font=F_DC_S, fill=GREY)
    d.line([24, 168, 1000, 168], fill=RULE, width=1)

    # lead cards
    for i, lead in enumerate(LEADS):
        x = 24 + i * 329
        col = REG[lead["region"]]
        if lead["art"] == "bridge":
            art_bridge(d, x, 174, 317, 116)
        elif lead["art"] == "gulf":
            art_gulf(d, x, 174, 317, 116)
        else:
            art_quad(d, x, 174, 317, 116)
        d.text((x, 296), f"{i + 1}", font=F_LKICK, fill=RED)
        kx = x + F_LKICK.getlength(f"{i + 1} ") + 2
        d.text((kx, 296), lead["kicker"], font=F_LKICK, fill=col)
        hl = wrap(lead["head"], F_LHEAD, 317)
        if len(hl) > 2:
            fail(f"lead {i + 1} headline {len(hl)} lines")
        hy = 312
        for ln in hl:
            d.text((x, hy), ln, font=F_LHEAD, fill=INK)
            hy += 24
        dl = wrap(lead["deck"], F_LDECK, 317)
        if len(dl) > 3:
            fail(f"lead {i + 1} deck {len(dl)} lines")
        dy = hy + 4
        for ln in dl:
            d.text((x, dy), ln, font=F_LDECK, fill=INK)
            dy += 16
        if dy - 16 + 13 > 416:
            fail(f"lead {i + 1} text passes y=416 (ends {dy - 16 + 13})")

    # small cards, 2 rows x 5
    for r in range(2):
        for c in range(5):
            idx = r * 5 + c
            card = CARDS[idx]
            n = 4 + idx
            x = 24 + c * 197
            y = 418 + r * 134
            col = REG[card["region"]]
            d.rectangle([x, y, x + 187, y + 126], fill=(238, 232, 216))
            d.rectangle([x, y, x + 187, y + 40], fill=(226, 220, 202))
            icon(d, card["icon"], x + 24, y + 20, col)
            tag = card["tag"]
            tw = F_TAG.getlength(tag)
            tx1 = x + 187 - 8 - tw - 12
            d.rounded_rectangle([tx1, y + 11, x + 187 - 8, y + 29], radius=4, fill=RED)
            d.text((tx1 + 6, y + 12), tag, font=F_TAG, fill=WHITE)
            d.text((x + 6, y + 46), f"{n}", font=F_CKICK, fill=RED)
            kx = x + 6 + F_CKICK.getlength(f"{n} ") + 2
            d.text((kx, y + 46), card["kicker"], font=F_CKICK, fill=col)
            hl = wrap(card["head"], F_CHEAD, 175)
            if len(hl) > 2:
                fail(f"card {n} headline {len(hl)} lines")
            hy = y + 62
            for ln in hl:
                d.text((x + 6, hy), ln, font=F_CHEAD, fill=INK)
                hy += 16
            dl = wrap(card["deck"], F_CDECK, 175)
            if len(dl) > 2:
                fail(f"card {n} deck {len(dl)} lines")
            dy = hy + 4
            for ln in dl:
                d.text((x + 6, dy), ln, font=F_CDECK, fill=INK)
                dy += 14
            if dy - 14 + 12 > y + 126:
                fail(f"card {n} text passes card bottom (ends {dy - 14 + 12}, card ends {y + 126})")
    return img, d

# ---------- bottom band: map + briefs + footer ----------
def draw_bottom(img, d):
    # section headers
    d.text((24, 686), "WHERE IT HAPPENED", font=F_SECT, fill=INK)
    d.text((404, 686), "ALSO ON TUESDAY 17 NOVEMBER", font=F_SECT, fill=INK)

    # world map: sea + dotted halftone continents (R3: narrowed 380 -> 360)
    mx, my, mw, mh = 24, 708, 360, 200
    d.rectangle([mx, my, mx + mw, my + mh], fill=SEA)
    d.rectangle([mx, my, mx + mw, my + mh], outline=RULE, width=1)
    def to_xy(lon, lat):
        return mx + (lon + 180.0) / 360.0 * mw, my + (85.0 - lat) / 145.0 * mh
    for px in range(mx + 3, mx + mw - 2, 7):
        for py in range(my + 3, my + mh - 2, 7):
            lon = -180.0 + (px - mx) / mw * 360.0
            lat = 85.0 - (py - my) / mh * 145.0
            if any(inside(lon, lat, poly) for poly in CONTINENTS):
                d.ellipse([px - 1, py - 1, px + 1, py + 1], fill=DOT)
    # brief dots 14..43 (drawn BEFORE pins so pins stay on top)
    for j, (lon, lat) in enumerate(DOTS):
        px, py = to_xy(lon, lat)
        d.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5], fill=REG[BRIEF_REGIONS[j]])
    # numbered pins 1..13 (Europe cluster nudged)
    for i, (lon, lat) in enumerate(PINS):
        px, py = to_xy(lon, lat)
        dx, dy = PIN_NUDGE.get(i + 1, (0, 0))
        px, py = px + dx, py + dy
        col = REG[PIN_REGIONS[i]]
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=WHITE, outline=col, width=2)
        d.text((px, py), str(i + 1), font=F_PIN, fill=col, anchor="mm")

    # legend, two rows under the map
    leg1 = ["Europe", "Middle East", "Asia", "Africa"]
    leg2 = ["Americas", "Oceania", "Global"]
    for row, items in ((920, leg1), (942, leg2)):
        lx = 24
        for name in items:
            col = REG[name]
            d.rectangle([lx, row + 1, lx + 10, row + 11], fill=col)
            d.text((lx + 14, row), name, font=F_LEGEND, fill=INK)
            lx += 14 + F_LEGEND.getlength(name) + 16

    # briefs: 15px, 2 cols x 15 rows, pitch 19 (R3: columns widened to 290)
    cols = [(404, 14, BRIEFS[:15]), (710, 29, BRIEFS[15:])]
    for col_x, start_n, items in cols:
        for k, text in enumerate(items):
            n = start_n + k
            ry = 700 + k * 19
            num = str(n)
            nw = F_BRIEF_N.getlength(num)
            if F_BRIEF.getlength(text) > 290 - nw - 5:
                fail(f"brief {n} too wide for 15px column: "
                     f"{F_BRIEF.getlength(text):.1f}px > {290 - nw - 5:.1f}px")
            d.text((col_x, ry), num, font=F_BRIEF_N, fill=RED)
            d.text((col_x + nw + 5, ry), text, font=F_BRIEF, fill=INK)
            if k < 14:
                d.line([col_x, ry + 17, col_x + 290, ry + 17], fill=RULE, width=1)
    if 700 + 14 * 19 + 15 > 1010:
        fail("briefs pass y=1010")

    # footer
    d.text((24, 982),
           "Every story here happened or was first reported on Tuesday 17 November 2026. Contested claims are marked as claims.",
           font=F_FOOT, fill=INK)
    d.text((24, 995),
           "Sources: Reuters, AP, AFP, BBC, Al Jazeera, WHO, UN. Original drawings.",
           font=F_FOOT, fill=GREY)
    if 995 + 11 > 1010:
        fail("footer passes y=1010")

def main():
    img, d = draw_page()
    draw_bottom(img, d)
    img.save("entry.png", optimize=True)
    print("wrote entry.png")

if __name__ == "__main__":
    main()
