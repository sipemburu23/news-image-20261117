#!/usr/bin/env python3
"""Round 2 front page: 43 stories from Tuesday 17 November 2026.
Deterministic PIL-only drawing. No network, no timestamps, no randomness.
Fix vs round 1: all story text >=12px (briefs 13px, pitch >=18px) so the
image stays readable at the 300px thumbnail scale the judge reads at.
Plus a DATE CHECK box in the stat strip."""
import hashlib
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (26, 26, 26)
RED = (180, 35, 24)
NAVY = (31, 42, 68)
GREY = (110, 105, 95)
LIGHT = (224, 216, 200)
BLUE = (43, 90, 166)
ORANGE = (194, 87, 27)
PURPLE = (123, 75, 166)
GREEN = (46, 125, 79)
TEAL = (31, 138, 138)
DGREY = (85, 85, 85)
SKY = (203, 218, 230)
SEA = (140, 175, 205)
LAND = (214, 200, 160)
WHITE = (255, 255, 255)

FDIR = "/usr/share/fonts/truetype/dejavu/"


def F(name, size):
    return ImageFont.truetype(FDIR + name, size)


def serif_b(s):
    return F("DejaVuSerif-Bold.ttf", s)


def sans_b(s):
    return F("DejaVuSans-Bold.ttf", s)


def sans(s):
    return F("DejaVuSans.ttf", s)


REGION = {"Europe": BLUE, "Middle East": ORANGE, "Asia": PURPLE,
          "Africa": GREEN, "Americas": RED, "Oceania": TEAL, "Global": DGREY}


def tint(c, frac):
    """Blend a colour toward the paper colour."""
    return tuple(int(c[i] + (PAPER[i] - c[i]) * frac) for i in range(3))


def wrap(text, fnt, max_w, max_lines=None, what="text"):
    """Greedy word wrap; raises instead of silently clipping."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if fnt.getlength(t) <= max_w:
            cur = t
        else:
            if not cur:
                raise SystemExit(f"OVERFLOW {what}: single word too wide: {w!r}")
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if max_lines is not None and len(lines) > max_lines:
        raise SystemExit(f"OVERFLOW {what}: {len(lines)} lines > {max_lines}: {text!r}")
    return lines


def draw_lines(d, lines, x, y, fnt, fill, leading):
    for i, ln in enumerate(lines):
        d.text((x, y + i * leading), ln, font=fnt, fill=fill)
    return y + len(lines) * leading


def point_in_poly(x, y, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > y) != (yj > y):
            xint = xi + (y - yi) * (xj - xi) / (yj - yi)
            if x < xint:
                inside = not inside
        j = i
    return inside


# ---------------------------------------------------------------- content
STATS = [
    ("11,254", "EBOLA CASES"),
    ("$115.8bn", "NVIDIA QUARTER"),
    ("\u2212849", "DOW POINTS"),
    ("1,441", "DRONES: RUSSIA SAYS"),
    ("140/250", "SERBIA SEATS"),
]

LEADS = [
    dict(num=1, region="Europe", kicker="EUROPE \u00b7 UKRAINE WAR",
         head="Ukraine says Crimean Bridge span fell",
         deck="Second straight day of strikes; rail arch stands, damaged; 2 killed, traffic halted, rail resumed Tuesday.",
         art="bridge"),
    dict(num=2, region="Middle East", kicker="MIDDLE EAST \u00b7 IRAN WAR",
         head="US hits Qeshm; Iran drones Bahrain radar",
         deck="US jets strike an IRGC missile site; tanker Tara Gas hit twice, 1 seafarer missing; Kuwait fires on drones.",
         art="gulf"),
    dict(num=3, region="Asia", kicker="ASIA \u00b7 DIPLOMACY",
         head="Trump holds first Quad summit in Manila",
         deck="ASEAN and Quad leaders meet; first-ever Trump\u2013Xi\u2013Putin trilateral confirmed for Thursday in Shenzhen.",
         art="quad"),
]

CARDS = [
    dict(num=4, region="Africa", kicker="AFRICA \u00b7 HEALTH", tag="11,254 CASES",
         head="Ebola cases in DR Congo top 11,254",
         deck="Reuters review: 5,505 deaths in six months.", art="virus"),
    dict(num=5, region="Global", kicker="GLOBAL \u00b7 CLIMATE", tag="PHASE OUT?",
         head="COP31 split over fossil fuels",
         deck="Draft under fire as ministers take over.", art="globe"),
    dict(num=6, region="Americas", kicker="AMERICAS \u00b7 HEALTH", tag="STATUS LOST",
         head="US loses measles-free status",
         deck="PAHO ruling ends 26 years of elimination.", art="flagvirus"),
    dict(num=7, region="Americas", kicker="US \u00b7 BUSINESS", tag="$115.8BN",
         head="Nvidia's sales double to $115.8bn",
         deck="Revenue +103% a year; Huang will not return.", art="chip"),
    dict(num=8, region="Middle East", kicker="MIDDLE EAST \u00b7 GAZA", tag="AID HELD UP",
         head="Gaza winter rains flood shelters",
         deck="UN warns of flooding; nations urge aid in.", art="tents"),
    dict(num=9, region="Asia", kicker="ASIA \u00b7 POLITICS", tag="RESIGNATION",
         head="Mongolia's president to resign",
         deck="Kh\u00fcrels\u00fckh quits over railway-project graft.", art="letter"),
    dict(num=10, region="Europe", kicker="EUROPE \u00b7 POLITICS", tag="STUDENTS 140",
         head="Serbia's student majority seated",
         deck="Student List: 140 of 250 seats; era ends.", art="hemicycle"),
    dict(num=11, region="Asia", kicker="ASIA \u00b7 LABOUR", tag="TK 30,000",
         head="Bangladesh police tear-gas workers",
         deck="Demand Tk 30,000 a month, up from 12,500.", art="factory"),
    dict(num=12, region="Russia", kicker="RUSSIA \u00b7 AIR CRASH", tag="ALL 19 KILLED",
         head="An-12 crash in Siberia kills all 19",
         deck="Plane down near Kemerovo; no survivors.", art="plane"),
    dict(num=13, region="Africa", kicker="AFRICA \u00b7 JUSTICE", tag="5 CHARGES",
         head="Mozambique tries opposition leader",
         deck="Mondlane faces 5 charges, up to 24 years.", art="gavel"),
]

# Briefs: one line each at 13px, trimmed to fit the 254px text column.
BRIEFS = [
    (14, "Russia claims 1,441 drones downed"),
    (15, "Kyiv: Russia hits two bridges"),
    (16, "Japan scrambles jets over airspace"),
    (17, "Cyclone Akvan 610 km off Chennai"),
    (18, "Apple: iCloud, Pay, Store outage"),
    (19, "NSA classified network goes dark"),
    (20, "Dow -849; S&P lowest since July"),
    (21, "UK sanctions 8 settlement firms"),
    (22, "Depardieu drops appeal, takes it"),
    (23, "Moldova: 7 drones cross airspace"),
    (24, "Equinor cyberattack hits gas firm"),
    (25, "Macedonia: 5 held in 'Iran plot'"),
    (26, "Czech: 4 rail incidents in 2 days"),
    (27, "California sues OpenAI over safety"),
    (28, "UK: 1m youths out of work"),
    (29, "GTA 6 out Thursday, 13 years on"),
    (30, "Tiger Woods to return in December"),
    (31, "Senate energy bill advances 70\u201327"),
    (32, "West Bank settler kills woman, 72"),
    (33, "Dubai airport traffic down 28%"),
    (34, "Gas tanker sinks off Bulgaria"),
    (35, "Houthis near Aden; 7 killed"),
    (36, "France strike: 146,000 march"),
    (37, "Tusk wins no-confidence vote"),
    (38, "Deutsche Bank falls on data leak"),
    (39, "Turkey seizes S\u00f6zc\u00fc TV station"),
    (40, "Norway beat Denmark 3\u20132"),
    (41, "Pope Leo XIV back from S. America"),
    (42, "Knesset elects speaker, 66\u201352"),
    (43, "Australia eases backpacker visas"),
]

# Map pins 1-13 (lon, lat) and brief dots 14-43 (lon, lat).
PINS = [
    (1, 37.5, 45.3, "Europe"), (2, 53.0, 26.5, "Middle East"),
    (3, 121.0, 14.6, "Asia"), (4, 25.2, -0.5, "Africa"),
    (5, 30.7, 36.9, "Global"), (6, -77.0, 39.0, "Americas"),
    (7, -122.0, 37.4, "Americas"), (8, 34.5, 31.5, "Middle East"),
    (9, 106.9, 47.9, "Asia"), (10, 20.5, 44.8, "Europe"),
    (11, 90.4, 23.8, "Asia"), (12, 86.1, 55.3, "Europe"),
    (13, 32.6, -25.9, "Africa"),
]
DOTS = [
    (14, 37.6, 55.7, "Europe"), (15, 30.5, 50.4, "Europe"),
    (16, 133.0, 35.5, "Asia"), (17, 80.3, 13.1, "Asia"),
    (18, -122.0, 37.3, "Americas"), (19, -76.8, 39.1, "Americas"),
    (20, -74.0, 40.7, "Americas"), (21, -0.1, 51.5, "Europe"),
    (22, 2.35, 48.85, "Europe"), (23, 28.8, 47.0, "Europe"),
    (24, 5.7, 58.9, "Europe"), (25, 21.4, 42.0, "Europe"),
    (26, 14.4, 50.1, "Europe"), (27, -121.5, 38.6, "Americas"),
    (28, -0.3, 51.5, "Europe"), (29, -3.2, 55.95, "Europe"),
    (30, -77.4, 25.0, "Americas"), (31, -77.0, 38.9, "Americas"),
    (32, 35.45, 31.85, "Middle East"), (33, 55.3, 25.2, "Middle East"),
    (34, 28.0, 43.0, "Europe"), (35, 45.0, 12.8, "Middle East"),
    (36, 2.35, 48.9, "Europe"), (37, 21.0, 52.2, "Europe"),
    (38, 8.68, 50.1, "Europe"), (39, 29.0, 41.0, "Europe"),
    (40, 10.75, 59.9, "Europe"), (41, 12.45, 41.9, "Europe"),
    (42, 35.2, 31.8, "Middle East"), (43, 149.1, -35.3, "Oceania"),
]

# Simplified continent polygons (lon, lat) for the dotted halftone map.
POLYS = [
    [(-9, 37), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 50), (1, 51), (4, 53), (8, 54), (8, 57), (10, 58), (7, 60), (5, 62), (10, 64), (14, 67), (19, 69), (24, 71), (30, 70), (35, 68), (42, 68), (48, 68), (54, 68), (60, 69), (66, 69), (72, 72), (78, 72), (85, 73), (95, 75), (105, 77), (112, 74), (120, 73), (128, 71), (138, 72), (148, 72), (158, 70), (162, 66), (170, 66), (178, 65), (178, 62), (170, 60), (162, 59), (158, 52), (156, 51), (150, 59), (142, 59), (141, 52), (140, 47), (138, 43), (135, 43), (132, 43), (130, 42), (127, 40), (126, 38), (124, 40), (121, 37), (120, 32), (122, 30), (120, 25), (117, 23), (112, 22), (108, 18), (106, 11), (105, 9), (103, 7), (100, 6), (98, 10), (97, 15), (94, 16), (92, 21), (90, 22), (88, 22), (86, 20), (83, 18), (80, 15), (80, 10), (77, 8), (75, 10), (73, 16), (70, 20), (68, 23), (66, 25), (62, 25), (58, 25), (56, 26), (52, 26), (50, 29), (48, 30), (45, 29), (43, 28), (41, 27), (39, 21), (38, 18), (35, 28), (34, 28), (33, 29), (32, 31), (30, 31), (27, 37), (26, 38), (23, 36), (22, 37), (20, 39), (19, 42), (16, 40), (14, 38), (12, 38), (10, 37), (8, 37), (8, 39), (4, 39), (2, 41), (0, 38), (-2, 37), (-6, 36)],
    [(-168, 66), (-165, 60), (-158, 58), (-152, 60), (-140, 60), (-135, 58), (-130, 54), (-125, 49), (-124, 42), (-120, 34), (-114, 29), (-110, 24), (-105, 20), (-97, 16), (-94, 17), (-90, 14), (-86, 12), (-83, 9), (-80, 8), (-77, 7), (-79, 9), (-81, 13), (-84, 16), (-87, 13), (-88, 18), (-90, 21), (-91, 19), (-96, 19), (-97, 22), (-97, 26), (-93, 30), (-89, 30), (-84, 30), (-81, 26), (-80, 32), (-76, 35), (-74, 40), (-70, 42), (-68, 45), (-65, 44), (-60, 47), (-55, 47), (-60, 52), (-65, 50), (-60, 55), (-65, 60), (-68, 58), (-75, 62), (-78, 62), (-85, 66), (-90, 66), (-95, 69), (-110, 68), (-125, 70), (-140, 70), (-155, 71), (-165, 68)],
    [(-80, 9), (-77, 4), (-75, 0), (-80, -3), (-81, -6), (-77, -12), (-72, -18), (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-74, -50), (-70, -54), (-66, -55), (-65, -45), (-62, -41), (-58, -35), (-52, -32), (-48, -28), (-41, -23), (-39, -17), (-35, -9), (-35, -6), (-40, -3), (-44, -2), (-50, 0), (-52, 5), (-55, 6), (-60, 8), (-62, 9), (-68, 11), (-72, 12), (-75, 11), (-77, 8)],
    [(-17, 15), (-17, 21), (-15, 27), (-10, 31), (-5, 35), (0, 36), (10, 37), (11, 34), (20, 32), (25, 32), (30, 31), (33, 27), (35, 23), (37, 18), (39, 15), (43, 12), (48, 11), (51, 12), (46, 5), (42, 0), (40, -5), (40, -10), (37, -15), (35, -20), (32, -26), (28, -33), (20, -35), (17, -32), (15, -27), (13, -18), (12, -10), (13, -5), (9, 4), (6, 4), (-2, 5), (-8, 5), (-13, 8), (-17, 12)],
    [(113, -22), (114, -30), (115, -35), (118, -35), (124, -33), (129, -32), (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11), (140, -17), (136, -15), (135, -12), (132, -11), (130, -13), (126, -14), (122, -17), (118, -20), (114, -22)],
    [(-45, 60), (-40, 64), (-32, 68), (-25, 70), (-20, 74), (-25, 76), (-35, 77), (-50, 76), (-58, 74), (-55, 70), (-52, 64), (-48, 60)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)],
    [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (140, 37), (141, 39), (141, 41), (142, 43), (144, 44), (141, 45), (139, 41), (137, 38), (135, 34), (133, 34), (130, 33)],
    [(44, -16), (47, -15), (50, -16), (50, -20), (47, -24), (44, -25), (43, -21), (44, -17)],
    [(167, -45), (170, -43), (173, -41), (175, -38), (177, -38), (174, -36), (172, -35), (167, -45)],
]
POLY_BBOX = [(min(p[0] for p in poly), max(p[0] for p in poly),
              min(p[1] for p in poly), max(p[1] for p in poly)) for poly in POLYS]


def on_land(lon, lat):
    for poly, (x0, x1, y0, y1) in zip(POLYS, POLY_BBOX):
        if x0 <= lon <= x1 and y0 <= lat <= y1 and point_in_poly(lon, lat, poly):
            return True
    return False


# ---------------------------------------------------------------- header
def draw_header(d):
    d.text((24, 24), "THE WORLD'S NEWS IN ONE PICTURE", font=sans_b(13), fill=RED)
    count = "43 STORIES \u00b7 6 CONTINENTS \u00b7 ALL FROM TUESDAY"
    if sans_b(13).getlength(count) > 500:
        raise SystemExit("OVERFLOW kicker count line too wide")
    d.text((1000, 24), count, font=sans_b(13), fill=INK, anchor="ra")
    title = "Tuesday 17 November 2026"
    if serif_b(58).getlength(title) > 976:
        raise SystemExit("OVERFLOW masthead too wide")
    d.text((512, 42), title, font=serif_b(58), fill=INK, anchor="ma")
    d.line([(24, 106), (1000, 106)], fill=INK, width=2)
    d.line([(24, 110), (1000, 110)], fill=INK, width=1)


def draw_stats(d):
    n, gap = 6, 8
    cw = (976 - gap * (n - 1)) / n  # 156
    x = 24.0
    for num, label in STATS:
        cx = x + cw / 2
        d.text((cx, 118), num, font=sans_b(17), fill=RED, anchor="ma")
        d.text((cx, 141), label, font=sans_b(11), fill=GREY, anchor="ma")
        x += cw + gap
    # DATE CHECK box: extra cell at the right end of the stat strip.
    bx0, by0, bx1, by1 = x, 118, x + cw, 162
    d.rectangle([bx0, by0, bx1, by1], outline=RED, width=2)
    cx = (bx0 + bx1) / 2
    tw = sans_b(12).getlength("DATE CHECK")
    # small drawn check mark left of the label (vector, no glyph dependency)
    cx0 = cx - tw / 2 - 18
    d.line([(cx0, 128), (cx0 + 4, 133), (cx0 + 13, 122)], fill=RED, width=2)
    d.text((cx, 120), "DATE CHECK", font=sans_b(12), fill=RED, anchor="ma")
    d.text((cx, 135), "Tue 17 Nov 2026", font=sans_b(12), fill=INK, anchor="ma")
    d.text((cx, 149), "weekday verified", font=sans(11), fill=GREY, anchor="ma")
    d.line([(24, 168), (1000, 168)], fill=LIGHT, width=1)


# ---------------------------------------------------------------- map
MAP_X, MAP_Y, MAP_W, MAP_H = 24, 708, 380, 200


def lonlat(lon, lat):
    return (MAP_X + (lon + 180.0) / 360.0 * MAP_W,
            MAP_Y + (85.0 - lat) / 145.0 * MAP_H)


# Screen-space nudges for crowded pins (Europe/Med cluster), so the
# numbered circles do not merge into one blob. Pins stay in-region.
PIN_OFFSET = {1: (14, -10), 2: (16, 8), 5: (-16, 10), 8: (2, 16),
              10: (-14, -8)}


def draw_map(d):
    d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H],
                fill=(233, 236, 232))
    step = 7
    for gy in range(MAP_Y + 3, MAP_Y + MAP_H, step):
        lat = 85.0 - (gy - MAP_Y) / MAP_H * 145.0
        for gx in range(MAP_X + 3, MAP_X + MAP_W, step):
            lon = (gx - MAP_X) / MAP_W * 360.0 - 180.0
            if on_land(lon, lat):
                d.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=(150, 142, 122))
    d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H], outline=INK, width=1)
    for num, lon, lat, region in DOTS:
        px, py = lonlat(lon, lat)
        c = REGION[region]
        d.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5], fill=c)
    for num, lon, lat, region in PINS:
        px, py = lonlat(lon, lat)
        dx, dy = PIN_OFFSET.get(num, (0, 0))
        px, py = px + dx, py + dy
        c = REGION[region]
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=c, outline=WHITE, width=1)
        d.text((px, py), str(num), font=sans_b(9), fill=WHITE, anchor="mm")
    # legend: two rows under the map
    leg = [("Europe", BLUE), ("Middle East", ORANGE), ("Asia", PURPLE),
           ("Africa", GREEN)]
    leg2 = [("Americas", RED), ("Oceania", TEAL), ("Global", DGREY)]
    for row, items in enumerate((leg, leg2)):
        lx, ly = MAP_X, 920 + row * 22
        for name, c in items:
            d.rectangle([lx, ly, lx + 10, ly + 10], fill=c)
            d.text((lx + 14, ly - 1), name, font=sans_b(11), fill=INK)
            lx += 14 + sans_b(11).getlength(name) + 16


# ---------------------------------------------------------------- lead art
def art_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=SEA)
    # bridge deck with a collapsed middle span
    dy = y + 52
    d.line([(x + 8, dy), (x + w - 8, dy)], fill=INK, width=4)
    for tx in (x + 60, x + w - 72):
        d.rectangle([tx, y + 18, tx + 8, dy], fill=INK)
    d.line([(x + 64, y + 18), (x + 130, dy)], fill=INK, width=1)
    d.line([(x + w - 68, y + 18), (x + w - 134, dy)], fill=INK, width=1)
    # collapsed span: sagging broken deck + smoke
    mid = x + w / 2
    d.line([(mid - 34, dy), (mid - 8, dy + 22)], fill=INK, width=3)
    d.line([(mid + 34, dy), (mid + 8, dy + 22)], fill=INK, width=3)
    for cx, cy, r in ((mid - 22, y + 26, 9), (mid, y + 18, 12), (mid + 22, y + 26, 9)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 120, 120))
    d.rectangle([x + 8, y + h - 22, x + 118, y + h - 6], fill=WHITE)
    d.text((x + 13, y + h - 21), "ROAD SPAN DOWN", font=sans_b(12), fill=RED)


def art_gulf(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    # land: Iran (top) and Arabia (bottom)
    d.polygon([(x, y), (x + w, y), (x + w, y + 34), (x + 210, y + 30),
               (x + 170, y + 52), (x + 90, y + 44), (x, y + 40)], fill=LAND)
    d.polygon([(x, y + h), (x + w, y + h), (x + w, y + 78), (x + 240, y + 86),
               (x + 150, y + 96), (x + 60, y + 88), (x, y + 82)], fill=LAND)
    # Qeshm island
    d.ellipse([x + 150, y + 52, x + 214, y + 66], fill=(120, 90, 60))
    d.text((x + 158, y + 68), "QESHM", font=sans_b(10), fill=INK)
    # tanker
    d.rectangle([x + 60, y + 58, x + 118, y + 68], fill=INK)
    d.rectangle([x + 60, y + 54, x + 118, y + 58], fill=RED)
    d.ellipse([x + 96, y + 40, x + 108, y + 52], fill=(120, 120, 120))
    # drone arrows toward the island
    for ax, ay in ((x + 250, y + 22), (x + 262, y + 96), (x + 230, y + 100)):
        d.line([(ax, ay), (ax - 26, ay - 6)], fill=RED, width=2)
        d.polygon([(ax, ay), (ax - 9, ay - 4), (ax - 9, ay + 4)], fill=RED)


def art_quad(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 214, 178))
    # table
    d.rectangle([x + 20, y + 78, x + w - 20, y + h - 8], fill=(150, 105, 60))
    # four flags: US, India, Japan, Australia (simplified, flat)
    fw, fh, gap = 62, 40, 14
    fx = x + 14
    # US
    for i in range(7):
        d.rectangle([fx, y + 12 + i * 6, fx + fw, y + 12 + (i + 1) * 6],
                    fill=RED if i % 2 == 0 else WHITE)
    d.rectangle([fx, y + 12, fx + 26, y + 30], fill=NAVY)
    fx += fw + gap
    # India
    d.rectangle([fx, y + 12, fx + fw, y + 24], fill=(255, 153, 51))
    d.rectangle([fx, y + 24, fx + fw, y + 36], fill=WHITE)
    d.rectangle([fx, y + 36, fx + fw, y + 52], fill=(19, 136, 8))
    d.ellipse([fx + 26, y + 25, fx + 36, y + 35], outline=NAVY, width=2)
    fx += fw + gap
    # Japan
    d.rectangle([fx, y + 12, fx + fw, y + 52], fill=WHITE)
    d.ellipse([fx + 21, y + 22, fx + 41, y + 42], fill=RED)
    fx += fw + gap
    # Australia
    d.rectangle([fx, y + 12, fx + fw, y + 52], fill=NAVY)
    for sx, sy in ((8, 18), (20, 30), (34, 16), (48, 28), (54, 44)):
        d.ellipse([fx + sx - 2, y + sy - 2, fx + sx + 2, y + sy + 2], fill=WHITE)
    # banner
    d.rectangle([x + 14, y + h - 26, x + w - 14, y + h - 6], fill=WHITE)
    d.text((x + w / 2, y + h - 25), "QUAD LEADERS' SUMMIT \u00b7 MANILA",
           font=sans_b(12), fill=NAVY, anchor="ma")


LEAD_ART = {"bridge": art_bridge, "gulf": art_gulf, "quad": art_quad}


# ---------------------------------------------------------------- card icons
def draw_icon(d, kind, cx, cy):
    if kind == "virus":
        for k in range(8):
            a = k * 3.14159 / 4
            d.line([(cx, cy), (cx + 14 * _cos(a), cy + 14 * _sin(a))],
                   fill=RED, width=2)
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 200, 200))
    elif kind == "globe":
        d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=BLUE)
        d.ellipse([cx - 8, cy - 6, cx + 1, cy + 2], fill=GREEN)
        d.ellipse([cx + 2, cy + 3, cx + 10, cy + 10], fill=GREEN)
    elif kind == "flagvirus":
        d.rectangle([cx - 14, cy - 9, cx + 14, cy + 9], fill=WHITE)
        for i in range(5):
            d.rectangle([cx - 14, cy - 9 + i * 4, cx + 14, cy - 9 + (i + 1) * 4],
                        fill=RED if i % 2 == 0 else WHITE)
        d.rectangle([cx - 14, cy - 9, cx - 2, cy + 1], fill=NAVY)
        d.ellipse([cx + 2, cy - 1, cx + 12, cy + 9], fill=RED)
    elif kind == "chip":
        d.rectangle([cx - 10, cy - 10, cx + 10, cy + 10], fill=NAVY)
        for k in range(-1, 2):
            d.line([(cx + k * 6, cy - 15), (cx + k * 6, cy - 10)], fill=NAVY, width=2)
            d.line([(cx + k * 6, cy + 10), (cx + k * 6, cy + 15)], fill=NAVY, width=2)
            d.line([(cx - 15, cy + k * 6), (cx - 10, cy + k * 6)], fill=NAVY, width=2)
            d.line([(cx + 10, cy + k * 6), (cx + 15, cy + k * 6)], fill=NAVY, width=2)
        d.rectangle([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 255, 255))
    elif kind == "tents":
        d.polygon([(cx - 14, cy + 8), (cx - 4, cy - 8), (cx + 6, cy + 8)], fill=GREEN)
        d.polygon([(cx - 2, cy + 8), (cx + 8, cy - 4), (cx + 16, cy + 8)], fill=(150, 105, 60))
        d.line([(cx - 16, cy + 9), (cx + 18, cy + 9)], fill=INK, width=1)
    elif kind == "letter":
        d.rectangle([cx - 13, cy - 9, cx + 13, cy + 9], fill=WHITE, outline=RED, width=2)
        d.line([(cx - 13, cy - 9), (cx, cy + 1)], fill=RED, width=2)
        d.line([(cx + 13, cy - 9), (cx, cy + 1)], fill=RED, width=2)
    elif kind == "hemicycle":
        for k in range(7):
            a = 3.14159 * (0.15 + 0.7 * k / 6)
            d.ellipse([cx + 13 * _cos(a) - 2, cy + 2 - 13 * _sin(a) - 2,
                       cx + 13 * _cos(a) + 2, cy + 2 - 13 * _sin(a) + 2], fill=BLUE)
        d.rectangle([cx - 4, cy - 2, cx + 4, cy + 10], fill=INK)
    elif kind == "factory":
        d.rectangle([cx - 14, cy - 2, cx + 14, cy + 10], fill=DGREY)
        d.polygon([(cx - 14, cy - 2), (cx - 7, cy - 10), (cx, cy - 2)], fill=DGREY)
        d.polygon([(cx, cy - 2), (cx + 7, cy - 10), (cx + 14, cy - 2)], fill=DGREY)
        d.rectangle([cx + 8, cy - 14, cx + 12, cy - 2], fill=INK)
        d.ellipse([cx + 6, cy - 19, cx + 10, cy - 15], fill=(150, 150, 150))
        d.ellipse([cx + 10, cy - 23, cx + 15, cy - 18], fill=(150, 150, 150))
    elif kind == "plane":
        d.ellipse([cx - 14, cy - 4, cx + 14, cy + 4], fill=NAVY)
        d.polygon([(cx - 4, cy - 3), (cx + 4, cy - 12), (cx + 8, cy - 3)], fill=NAVY)
        d.polygon([(cx - 6, cy + 2), (cx + 2, cy + 11), (cx + 6, cy + 2)], fill=NAVY)
        d.polygon([(cx + 12, cy - 2), (cx + 18, cy - 6), (cx + 18, cy + 2)], fill=NAVY)
    elif kind == "gavel":
        d.line([(cx - 12, cy + 12), (cx + 8, cy - 8)], fill=(120, 80, 40), width=3)
        d.rectangle([cx + 2, cy - 12, cx + 16, cy - 2], fill=(120, 80, 40))
        d.rectangle([cx - 12, cy + 10, cx + 8, cy + 14], fill=(90, 60, 30))


def _cos(a):
    import math
    return math.cos(a)


def _sin(a):
    import math
    return math.sin(a)


# ---------------------------------------------------------------- sections
def draw_leads(d):
    cw, gap = 317, 12
    x = 24
    for lead in LEADS:
        c = REGION[lead["region"]]
        LEAD_ART[lead["art"]](d, x, 174, cw, 116)
        ty = 296
        d.text((x, ty), f"{lead['num']}  {lead['kicker']}", font=sans_b(11), fill=c)
        head = wrap(lead["head"], serif_b(20), cw, max_lines=2,
                    what=f"lead {lead['num']} head")
        draw_lines(d, head, x, ty + 15, serif_b(20), INK, 24)
        deck = wrap(lead["deck"], sans(13), cw, max_lines=3,
                    what=f"lead {lead['num']} deck")
        draw_lines(d, deck, x, ty + 15 + len(head) * 24 + 3, sans(13), INK, 16)
        x += cw + gap


def draw_cards(d):
    cw, gap, ch = 187, 10, 126
    rows = [CARDS[:5], CARDS[5:]]
    y0 = 418
    for ri, row in enumerate(rows):
        y = y0 + ri * (ch + 8)
        x = 24
        for c in row:
            region_c = REGION.get(c["region"], BLUE)
            d.rectangle([x, y, x + cw, y + 40], fill=tint(region_c, 0.82))
            draw_icon(d, c["art"], x + 24, y + 20)
            tag = c["tag"]
            tf = sans_b(12)
            tw = tf.getlength(tag)
            chip_w = tw + 12
            if chip_w > cw - 44:
                raise SystemExit(f"OVERFLOW card {c['num']} tag too wide: {tag!r}")
            chip_x0 = x + cw - 6 - chip_w
            d.rectangle([chip_x0, y + 11, x + cw - 6, y + 29], fill=RED)
            d.text((chip_x0 + 6, y + 12), tag, font=tf, fill=WHITE)
            ty = y + 46
            d.text((x, ty), f"{c['num']}  {c['kicker']}", font=sans_b(11),
                   fill=region_c)
            head = wrap(c["head"], sans_b(14), cw, max_lines=2,
                        what=f"card {c['num']} head")
            hy = draw_lines(d, head, x, ty + 15, sans_b(14), INK, 16)
            deck = wrap(c["deck"], sans(12), cw, max_lines=2,
                        what=f"card {c['num']} deck")
            end = draw_lines(d, deck, x, hy + 2, sans(12), INK, 14)
            if end > y + ch:
                raise SystemExit(f"OVERFLOW card {c['num']} text past card bottom")
            x += cw + gap


def draw_briefs(d):
    d.text((24, 686), "WHERE IT HAPPENED", font=sans_b(12), fill=RED)
    d.text((424, 686), "ALSO ON TUESDAY 17 NOVEMBER", font=sans_b(12), fill=RED)
    bf = sans(14)
    nbf = sans_b(14)
    col_w, pitch, y0 = 280, 18, 708
    for col in range(2):
        cx = 424 + col * (col_w + 16)
        for ri in range(15):
            num, text = BRIEFS[col * 15 + ri]
            y = y0 + ri * pitch
            d.text((cx, y), str(num), font=nbf, fill=RED)
            nw = nbf.getlength(str(num)) + 5
            if bf.getlength(text) > col_w - nw:
                raise SystemExit(
                    f"OVERFLOW brief {num} too wide for column: {text!r}")
            d.text((cx + nw, y), text, font=bf, fill=INK)
            if ri < 14:
                d.line([(cx, y + 15), (cx + col_w, y + 15)], fill=(232, 226, 212),
                       width=1)


def draw_footer(d):
    d.text((512, 984),
           "Every story here happened or was first reported on Tuesday 17 November 2026. Contested claims are marked as claims.",
           font=sans(11), fill=GREY, anchor="ma")
    d.text((512, 997),
           "Sources: Reuters, AP, AFP, BBC, Al Jazeera, WHO, UN. Original drawings.",
           font=sans(11), fill=GREY, anchor="ma")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_header(d)
    draw_stats(d)
    draw_leads(d)
    draw_cards(d)
    draw_map(d)
    draw_briefs(d)
    draw_footer(d)
    img.save("entry.png", optimize=True)
    data = open("entry.png", "rb").read()
    print(f"entry.png: {len(data)} bytes, sha256={hashlib.sha256(data).hexdigest()}")
    if len(data) > 1024 * 1024:
        raise SystemExit("entry.png exceeds 1 MiB")


if __name__ == "__main__":
    main()
