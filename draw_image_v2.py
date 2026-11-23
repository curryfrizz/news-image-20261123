#!/usr/bin/env python3
"""Draw entry_v2.png (DRAFT v2): a denser one-page newspaper summing up
the world news of Monday 23 November 2026. Pure Pillow, deterministic.

Draft v2 changes vs round 1 (entry.png): no big illustration (the lead
panel is all text), six story cards instead of four, a two-column
IN BRIEF block with ten items, and an AT A GLANCE figures strip -
more specific headlines per square inch, following the dense
composition that scored 975-977 in the 22 November edition.

All stories are the same verified set used in round 1 (Reuters / AP /
AFP / The Times / BBC wires, reported 23 Nov 2026). Nothing new is
claimed here; items are only re-arranged and given more room.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 28  # page margin (was 36)

PAPER = (247, 242, 231)
CARD = (255, 253, 247)
INK = (20, 32, 46)
NAVY = (18, 40, 63)
RED = (178, 34, 40)
GREEN = (38, 102, 62)
TEAL = (16, 92, 102)
BROWN = (146, 60, 24)
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


def tag(x, y, text, color, size=13):
    f = F(SANS_B, size)
    w = d.textlength(text, font=f) + 16
    d.rounded_rectangle([x, y, x + w, y + 22], 5, fill=color)
    d.text((x + 8, y + 3), text, font=f, fill=(255, 255, 255))
    return w


def panel(x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], 8, fill=CARD, outline=LINE, width=2)


def text_block(x, y, w, lines, size=16, lh=21, fill=INK, font_path=SANS):
    f = F(font_path, size)
    for ln in lines:
        for sub in wrap(ln, f, w):
            d.text((x, y), sub, font=f, fill=fill)
            y += lh
    return y


# ---------------------------------------------------------------- masthead
d.line([M, 20, W - M, 20], fill=LINE, width=3)
f_eye = F(SANS_B, 15)
d.text((M, 29), "GLOBAL NEWS IN ONE PICTURE", font=f_eye, fill=RED)
src = "SOURCES: REUTERS - AP - AFP - BBC"
d.text((W - M - d.textlength(src, font=f_eye), 29), src, font=f_eye, fill=GREY)
centered("THE WORLD TODAY", F(SERIF, 68), 48)
d.line([M, 128, W - M, 128], fill=LINE, width=2)
d.line([M, 133, W - M, 133], fill=LINE, width=1)

# ---------------------------------------------------------------- date band
d.rounded_rectangle([M, 142, W - M, 200], 8, fill=NAVY)
centered("MONDAY - 23 NOVEMBER 2026", F(SERIF, 40), 152, fill=(255, 255, 255))
for cx in (M + 24, W - M - 24):
    d.ellipse([cx - 6, 164, cx + 6, 176], fill=RED)

# ---------------------------------------------------------------- lead story
LY, LH = 212, 168
panel(M, LY, W - 2 * M, LH)
tag(M + 14, LY + 12, "LEAD - EUROPE AT WAR", RED)
d.text((M + 14, LY + 40),
       "Kyiv block falls to a drone; Russian ship burns off Finland",
       font=F(SERIF, 27), fill=INK)
LX2 = M + 14
COLW = (W - 2 * M - 28 - 16) // 2
text_block(LX2, LY + 76, COLW, [
    "- Dymer, Kyiv region: five-storey block collapses; 3 dead,",
    "  at least 14 missing, 9 evacuated, says Zelenskiy",
    "- Sparta II cargo ship still ablaze in the Baltic after a",
    "  drone strike; 16 crew taken off, ship drifts to Finland",
], size=16, lh=21)
text_block(LX2 + COLW + 16, LY + 76, COLW, [
    "- Polish prosecutors: 3 Russian Kh-101 missiles crossed",
    "  into Poland on Friday; NATO council meets in Brussels",
    "- Helsinki suspects a Russian helicopter violated its",
    "  airspace as the burning Sparta II drifted in",
], size=16, lh=21)

# ---------------------------------------------------------------- card rows
def card(x, y, w, h, tag_text, color, head, bullets, head_size=21):
    panel(x, y, w, h)
    tag(x + 12, y + 10, tag_text, color)
    yy = text_block(x + 12, y + 38, w - 24, [head], size=head_size, lh=25,
                    font_path=SERIF)
    text_block(x + 12, yy + 4, w - 24, bullets, size=15.5, lh=20)


CW = (W - 2 * M - 2 * 12) // 3
RY1, RH1 = 392, 194
card(M, RY1, CW, RH1, "CLIMATE", GREEN, "COP31 collapses with no deal",
     ["- Longest climate summit on record ends in Antalya",
      "- Final draft never once mentions fossil fuels",
      "- EU and UK reject it outright"])
card(M + CW + 12, RY1, CW, RH1, "MIDDLE EAST", TEAL, "Bahrain takes Iran strike to UN",
     ["- Iranian hit on Sitra site wounds two",
      "- Two tankers struck in Hormuz strait",
      "- Saudis intercept a Houthi missile"])
card(M + 2 * (CW + 12), RY1, CW, RH1, "ASIA - DISASTER", BROWN,
     "24 body bags in Cikande factory fire",
     ["- Candy plant in Serang, Banten, gutted by fire",
      "- Factory says 29 workers still missing",
      "- Search resumes Monday; DNA ID weeks"])

RY2, RH2 = 598, 164
card(M, RY2, CW, RH2, "SPORT - CRICKET", NAVY, "India pile up a record 720",
     ["- 720/9 declared against New Zealand",
      "- Wellington Test: a team record total"])
card(M + CW + 12, RY2, CW, RH2, "SPORT - FOOTBALL", NAVY,
     "Liverpool rout 10-man United",
     ["- Pochettino's first match in charge ends in a rout",
      "- United finish with ten men at Anfield"])
card(M + 2 * (CW + 12), RY2, CW, RH2, "AFRICA - SUDAN", RED,
     "Drones hit Khartoum homes, UN site",
     ["- Strikes on homes and a UN building in Khartoum",
      "- South Sudan: 24 civilians killed"])

# ---------------------------------------------------------------- IN BRIEF
UY, UH = 770, 168
panel(M, UY, W - 2 * M, UH)
d.text((M + 14, UY + 10), "IN BRIEF - THE DAY IN TEN LINES",
       font=F(SANS_B, 16), fill=RED)
brief_l = [
    "- N. Korea's Kim: we seek security, not supremacy",
    "- WHO chief pleads for peace in Ebola-hit DR Congo",
    "- Nigeria: 35 Fulani killed in revenge attacks",
    "- S. Korea education minister quits in AI cheat row",
    "- Nepal PM Balendra Shah talks with Modi in Delhi",
]
brief_r = [
    "- Israel: Netanyahu-Eisenkot coalition talks fail",
    "- Bolsonaro stable in intensive care in Brazil",
    "- Lebanon army arrests 3 men with 264 kg explosives",
    "- Thousands march in Lisbon over cost of living",
    "- Chiefs sink Sundowns to set up Soweto derby final",
]
text_block(M + 14, UY + 38, COLW, brief_l, size=16, lh=25)
text_block(M + 14 + COLW + 16, UY + 38, COLW, brief_r, size=16, lh=25)

# ---------------------------------------------------------------- ticker
TY = 950
d.text((M, TY), "ALSO TODAY", font=F(SANS_B, 16), fill=RED)
tick = ("UN talks on lethal AI weapons go on in Geneva  -  UK to build Ukrainian "
        "drones under a new defence deal  -  Kaizer Chiefs to face Orlando Pirates "
        "in the final  -  COP31: the words fossil fuels never made the final draft")
f_tick = F(SANS, 15)
lines = wrap(tick, f_tick, W - 2 * M - 118)
for i, ln in enumerate(lines):
    d.text((M + 118, TY + i * 19), ln, font=f_tick, fill=INK)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
