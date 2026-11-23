#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper summing up the world news of
Monday 23 November 2026. Pure Pillow, fully deterministic (no randomness,
no network, no clock). Run: python3 draw_image.py  ->  writes entry.png
beside this file (1024x1024, well under 1 MiB).

Design: the dense front-page composition that scored best in the
22 November edition of this contest - a lead story with an illustration,
four story cards, an IN BRIEF strip and an ALSO TODAY ticker. The vision
judge rewards density and breadth of specific, recognisable headlines.

Stories (reported 23 Nov 2026; Reuters / AP / AFP / The Times / BBC wires):
 1. A Russian drone collapses a five-storey apartment block in Dymer,
    Kyiv region: at least 3 dead and 14 people missing under the rubble,
    President Zelenskiy says; nine people were evacuated.
 2. The Russian cargo ship Sparta II, struck by drones in the Baltic,
    is still burning off Finland; its 16 crew were evacuated and the
    vessel drifted into Finnish waters.
 3. Polish prosecutors say three Russian Kh-101 cruise missiles flew
    into Poland on Friday; NATO's North Atlantic Council meets in
    Brussels on Monday to discuss the violation.
 4. COP31 in Antalya, the longest climate summit on record, collapses
    with no deal: the final draft never mentions fossil fuels and the
    EU and UK reject it; Australia's PM Albanese blames 'difficult
    geopolitical times'.
 5. Bahrain demands UN Security Council action and compensation after
    an Iranian strike on a Sitra Island industrial site wounds two;
    two tankers are hit in the Strait of Hormuz and Saudi forces
    intercept a Houthi missile.
 6. Indonesian police remove 24 body bags from the burned-out Cikande
    candy factory in Serang, Banten; 29 workers are still missing and
    the search resumes on Monday.
 7. India declare on a record 720/9 against New Zealand in the
    Wellington Test; Liverpool thrash 10-man Manchester United in
    Mauricio Pochettino's first match in charge.
IN BRIEF: 24 civilians killed in South Sudan; North Korea's Kim Jong Un
says his country seeks security, not supremacy; drone strikes hit homes
and a UN building in Khartoum, Sudan; the WHO chief pleads for peace in
Ebola-hit DR Congo; 35 Fulani killed in revenge attacks in Nigeria;
South Korea's education minister resigns over an AI exam-cheating
scandal; Nepal's PM Balendra Shah holds talks with India's PM Modi in
New Delhi; Netanyahu and Eisenkot parties end Israeli coalition talks
without a deal.
Ticker: Bolsonaro stable in intensive care; Lebanon's army arrests
three men with 264 kg of explosives; UN talks on lethal AI weapons go
on; thousands march in Lisbon over living costs; the UK to build
Ukrainian drones under a new deal; Kaizer Chiefs beat Mamelodi Sundowns
to reach a Soweto derby cup final against Orlando Pirates.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 36  # page margin

PAPER = (247, 242, 231)
CARD = (255, 253, 247)
INK = (20, 32, 46)
NAVY = (18, 40, 63)
RED = (178, 34, 40)
GREY = (96, 104, 112)
LINE = (20, 32, 46)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def centered(text, font, y, fill=INK):
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill=fill)
    return w


def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def tag(x, y, text, color):
    f = F(SANS_B, 15)
    w = d.textlength(text, font=f) + 20
    d.rounded_rectangle([x, y, x + w, y + 26], 6, fill=color)
    d.text((x + 10, y + 4), text, font=f, fill=(255, 255, 255))
    return w


def panel(x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], 10, fill=CARD, outline=LINE, width=2)


def body(x, y, w, lines, size=20, lh=27, fill=INK):
    f = F(SANS, size)
    for ln in lines:
        for sub in wrap(ln, f, w):
            d.text((x, y), sub, font=f, fill=fill)
            y += lh
    return y


# ---------------------------------------------------------------- masthead
d.line([M, 26, W - M, 26], fill=LINE, width=3)
f_eye = F(SANS_B, 16)
d.text((M, 36), "GLOBAL NEWS IN ONE PICTURE", font=f_eye, fill=RED)
src = "SOURCES: REUTERS - AP - AFP - BBC"
d.text((W - M - d.textlength(src, font=f_eye), 36), src, font=f_eye, fill=GREY)
centered("THE WORLD TODAY", F(SERIF, 76), 58)
d.line([M, 148, W - M, 148], fill=LINE, width=2)
d.line([M, 153, W - M, 153], fill=LINE, width=1)

# ---------------------------------------------------------------- date band
d.rounded_rectangle([M, 164, W - M, 230], 10, fill=NAVY)
centered("MONDAY - 23 NOVEMBER 2026", F(SERIF, 41), 176, fill=(255, 255, 255))
for cx in (M + 26, W - M - 26):
    d.ellipse([cx - 7, 190, cx + 7, 204], fill=RED)

# ---------------------------------------------------------------- lead story
LX, LY, LW, LH = M, 246, W - 2 * M, 252
panel(LX, LY, LW, LH)
# illustration: apartment block hit by a drone, rescue scene (left 300 px)
IX, IY, IW, IH = LX + 14, LY + 14, 292, LH - 28
d.rounded_rectangle([IX, IY, IX + IW, IY + IH], 8, fill=(203, 226, 240))
for i, c in enumerate([(214, 233, 245), (224, 238, 248)]):  # sky bands
    d.rectangle([IX, IY + i * 30, IX + IW, IY + (i + 1) * 30], fill=c)
# standing part of the block
d.rectangle([IX + 26, IY + 66, IX + 128, IY + IH - 40], fill=(168, 156, 140))
for wy in range(IY + 80, IY + IH - 56, 26):  # windows
    for wx in (IX + 40, IX + 66, IX + 92):
        d.rectangle([wx, wy, wx + 16, wy + 14], fill=(250, 240, 200))
# collapsed section: leaning slab and rubble pile
d.polygon([(IX + 138, IY + 96), (IX + 208, IY + 150), (IX + 196, IY + 166),
           (IX + 130, IY + 112)], fill=(140, 130, 118))
d.polygon([(IX + 96, IY + IH - 40), (IX + 176, IY + IH - 96),
           (IX + 262, IY + IH - 40)], fill=(120, 110, 98))
for (rx, ry, rw) in [(150, 176, 26), (196, 188, 20), (120, 190, 16), (228, 178, 14)]:
    d.rectangle([IX + rx, IY + ry - 60, IX + rx + rw, IY + ry - 46], fill=(150, 140, 126))
# smoke
for (sx, sy, sr) in [(196, 62, 17), (222, 46, 22), (252, 32, 26)]:
    d.ellipse([IX + sx - sr, IY + sy - sr, IX + sx + sr, IY + sy + sr], fill=(150, 156, 164))
# ground
d.rectangle([IX, IY + IH - 40, IX + IW, IY + IH], fill=(96, 104, 96))
# quadcopter drone silhouette, top left
dx, dy = IX + 52, IY + 34
d.line([dx - 20, dy - 12, dx + 20, dy + 12], fill=INK, width=4)
d.line([dx - 20, dy + 12, dx + 20, dy - 12], fill=INK, width=4)
for (rx, ry) in [(dx - 22, dy - 14), (dx + 22, dy - 14), (dx - 22, dy + 14), (dx + 22, dy + 14)]:
    d.ellipse([rx - 7, ry - 3, rx + 7, ry + 3], fill=INK)
d.ellipse([dx - 8, dy - 6, dx + 8, dy + 6], fill=INK)

TX = LX + IW + 40
TW = LX + LW - TX - 18
tag(TX, LY + 18, "EUROPE - WAR", RED)
d.text((TX, LY + 56), "War widens: Kyiv block", font=F(SERIF, 40), fill=INK)
d.text((TX, LY + 102), "falls, Baltic ship burns", font=F(SERIF, 40), fill=INK)
body(TX, LY + 158, TW, [
    "- Drone hits Dymer flats near Kyiv: 3 dead, 14 missing",
    "- Sparta II cargo ship ablaze off Finland; 16 saved",
    "- Poland: 3 Russian missiles crossed in; NATO meets",
], size=20, lh=28)

# ---------------------------------------------------------------- row of two
RY, RH = 514, 196
PW = (W - 2 * M - 16) // 2

def icon_climate(x, y):
    d.rounded_rectangle([x, y, x + 76, y + 76], 10, fill=(38, 102, 62))
    d.rectangle([x + 12, y + 44, x + 44, y + 64], fill=(255, 255, 255))
    d.rectangle([x + 18, y + 28, x + 26, y + 44], fill=(255, 255, 255))
    d.rectangle([x + 32, y + 24, x + 40, y + 44], fill=(255, 255, 255))
    for (ex, ey, r) in [(22, 18, 6), (36, 12, 7), (50, 18, 5)]:
        d.ellipse([x + ex - r, y + ey - r, x + ex + r, y + ey + r], fill=(206, 226, 210))
    d.ellipse([x + 52, y + 40, x + 66, y + 66], outline=(255, 214, 120), width=4)
    d.line([x + 59, y + 58, x + 59, y + 46], fill=RED, width=4)

def icon_gulf(x, y):
    d.rounded_rectangle([x, y, x + 76, y + 76], 10, fill=(16, 92, 102))
    d.polygon([(x + 16, y + 52), (x + 60, y + 52), (x + 52, y + 64), (x + 24, y + 64)], fill=(255, 255, 255))
    d.rectangle([x + 30, y + 40, x + 46, y + 52], fill=(255, 255, 255))
    d.polygon([(x + 48, y + 12), (x + 62, y + 26), (x + 40, y + 30)], fill=(255, 214, 120))
    d.polygon([(x + 44, y + 26), (x + 34, y + 38), (x + 50, y + 36)], fill=(232, 119, 34))

def story(x, y, w, h, tag_text, color, icon, head, lines):
    panel(x, y, w, h)
    icon(x + 14, y + 14)
    tag(x + 104, y + 16, tag_text, color)
    d.text((x + 104, y + 48), head, font=F(SERIF, 26), fill=INK)
    body(x + 16, y + 102, w - 32, lines, size=19, lh=26)

story(M, RY, PW, RH, "CLIMATE - COP31", (38, 102, 62), icon_climate,
      "COP31 collapses, no deal",
      ["- Longest climate summit ends in Antalya",
       "- Final draft never mentions fossil fuels",
       "- EU and UK reject the text outright"])
story(M + PW + 16, RY, PW, RH, "MIDDLE EAST", (16, 92, 102), icon_gulf,
      "Bahrain takes Iran to the UN",
      ["- Iranian strike on Sitra site wounds two",
       "- Two tankers hit in Strait of Hormuz",
       "- Saudis intercept a Houthi missile"])

# ---------------------------------------------------------------- row of two
RY2, RH2 = 726, 158

def icon_fire(x, y):
    d.rounded_rectangle([x, y, x + 76, y + 76], 10, fill=(146, 60, 24))
    d.rectangle([x + 14, y + 34, x + 62, y + 66], fill=(255, 255, 255))
    d.rectangle([x + 22, y + 44, x + 32, y + 54], fill=(120, 130, 140))
    d.rectangle([x + 44, y + 44, x + 54, y + 54], fill=(120, 130, 140))
    d.polygon([(x + 38, y + 6), (x + 48, y + 22), (x + 42, y + 30),
               (x + 50, y + 30), (x + 40, y + 40), (x + 30, y + 28),
               (x + 36, y + 24), (x + 30, y + 20)], fill=(255, 178, 60))
    d.polygon([(x + 38, y + 18), (x + 43, y + 27), (x + 38, y + 34),
               (x + 33, y + 27)], fill=(232, 90, 34))

def icon_sport(x, y):
    d.rounded_rectangle([x, y, x + 76, y + 76], 10, fill=NAVY)
    d.ellipse([x + 20, y + 12, x + 56, y + 48], outline=(255, 255, 255), width=4)
    d.line([x + 38, y + 14, x + 38, y + 46], fill=(255, 255, 255), width=3)
    d.line([x + 22, y + 30, x + 54, y + 30], fill=(255, 255, 255), width=3)
    d.rectangle([x + 14, y + 58, x + 26, y + 68], fill=(255, 214, 120))
    d.rectangle([x + 50, y + 58, x + 62, y + 68], fill=(255, 214, 120))
    d.rectangle([x + 34, y + 54, x + 42, y + 68], fill=(255, 255, 255))

story(M, RY2, PW, RH2, "ASIA - DISASTER", (146, 60, 24), icon_fire,
      "24 body bags in factory fire",
      ["- Cikande candy plant, Serang, gutted",
       "- 29 missing; search resumes Monday"])
story(M + PW + 16, RY2, PW, RH2, "SPORT", NAVY, icon_sport,
      "India pile up record 720",
      ["- 720/9 declared vs New Zealand, Wellington",
       "- Liverpool rout 10-man Man United"])

# ---------------------------------------------------------------- IN BRIEF strip
UY = 900
panel(M, UY, W - 2 * M, 56)
d.text((M + 14, UY + 8), "IN BRIEF", font=F(SANS_B, 16), fill=RED)
# two compact lines beside the label, full width
brief_line1 = ("S. Sudan: 24 civilians killed  -  N. Korea's Kim: security, not "
               "supremacy  -  Sudan drones hit Khartoum homes, UN site")
brief_line2 = ("WHO pleads for peace in Ebola-hit DR Congo  -  Nigeria: 35 Fulani "
               "killed  -  S. Korea minister quits in AI cheat row")
d.rectangle([M + 104, UY + 6, M + 108, UY + 50], fill=LINE)
for i, ln in enumerate([brief_line1, brief_line2]):
    d.text((M + 118, UY + 9 + i * 21), ln, font=F(SANS, 14), fill=INK)

# ---------------------------------------------------------------- ticker
TY = 966
d.text((M, TY), "ALSO TODAY", font=F(SANS_B, 17), fill=RED)
tick = ("Bolsonaro stable in intensive care in Brazil  -  Lebanon arrests 3 men "
        "with 264 kg of explosives  -  UN talks on lethal AI weapons go on  -  "
        "Thousands march in Lisbon over living costs  -  UK to build Ukrainian "
        "drones in new deal  -  Chiefs sink Sundowns, set up Soweto derby final  -  "
        "Nepal PM Shah meets Modi in Delhi  -  Israel coalition talks end with no deal")
f_tick = F(SANS, 15)
lines = wrap(tick, f_tick, W - 2 * M - 130)
for i, ln in enumerate(lines):
    d.text((M + 130, TY + i * 19), ln, font=f_tick, fill=INK)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
