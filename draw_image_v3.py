#!/usr/bin/env python3
"""Draw entry_v3.png (DRAFT v3): an even denser one-page newspaper
summing up the world news of Monday 23 November 2026. Pure Pillow,
deterministic. Draft only - not the submitted entry.

V3 changes vs the active V2 (round 2: rank 485/9,643, win rate
684.211): V2's cards were half empty, so V3 fills the page - a
THE DAY IN NUMBERS strip, three mini-cards with their own headlines
(Asia-Pacific / Europe / Americas-Mideast) where V2 had bare IN BRIEF
lines, more fact lines per card (41 vs ~31), and every verified
detail from the research set (children among the Dymer dead, four
Cikande workers in hospital, Albanese's 'difficult geopolitical
times', NATO's Monday meeting split out as its own line).

All stories are the same verified set used in rounds 1-2 (Reuters /
AP / AFP / The Times / BBC wires, reported 23 Nov 2026).
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 24  # page margin

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
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def centered(text, font, y, fill=INK):
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill=fill)


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


def tag(x, y, text, color, size=12):
    f = F(SANS_B, size)
    w = d.textlength(text, font=f) + 14
    d.rounded_rectangle([x, y, x + w, y + 20], 5, fill=color)
    d.text((x + 7, y + 3), text, font=f, fill=(255, 255, 255))


def panel(x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], 8, fill=CARD, outline=LINE, width=2)


def text_block(x, y, w, lines, size=15, lh=19, font_path=SANS):
    f = F(font_path, size)
    for ln in lines:
        for sub in wrap(ln, f, w):
            d.text((x, y), sub, font=f, fill=INK)
            y += lh
    return y


def card(x, y, w, h, tag_text, color, head, bullets, head_size=20):
    panel(x, y, w, h)
    tag(x + 11, y + 9, tag_text, color)
    yy = text_block(x + 11, y + 34, w - 22, [head], size=head_size, lh=24,
                    font_path=SERIF)
    text_block(x + 11, yy + 3, w - 22, bullets, size=15, lh=19)


# ---------------------------------------------------------------- masthead
d.line([M, 16, W - M, 16], fill=LINE, width=3)
f_eye = F(SANS_B, 14)
d.text((M, 24), "GLOBAL NEWS IN ONE PICTURE", font=f_eye, fill=RED)
src = "SOURCES: REUTERS - AP - AFP - BBC"
d.text((W - M - d.textlength(src, font=f_eye), 24), src, font=f_eye, fill=GREY)
centered("THE WORLD TODAY", F(SERIF, 62), 42)
d.line([M, 114, W - M, 114], fill=LINE, width=2)
d.line([M, 119, W - M, 119], fill=LINE, width=1)

# ---------------------------------------------------------------- date band
d.rounded_rectangle([M, 128, W - M, 182], 8, fill=NAVY)
centered("MONDAY - 23 NOVEMBER 2026", F(SERIF, 38), 137, fill=(255, 255, 255))
for cx in (M + 22, W - M - 22):
    d.ellipse([cx - 6, 149, cx + 6, 161], fill=RED)

# ---------------------------------------------------------------- lead story
LY, LH = 194, 134
panel(M, LY, W - 2 * M, LH)
tag(M + 12, LY + 10, "LEAD - EUROPE AT WAR", RED)
d.text((M + 12, LY + 34),
       "Drone fells Kyiv block; Russian ship burns; missiles enter Poland",
       font=F(SERIF, 24), fill=INK)
COLW = (W - 2 * M - 24 - 14) // 2
text_block(M + 12, LY + 68, COLW, [
    "- Dymer: block collapses, 3 dead incl. children reports",
    "- At least 14 missing, 9 evacuated, says Zelenskiy",
    "- Sparta II ablaze off Finland; 16 crew taken off",
], size=15, lh=20)
text_block(M + 12 + COLW + 14, LY + 68, COLW, [
    "- Poland: 3 Russian Kh-101 missiles crossed in Friday",
    "- NATO's North Atlantic Council meets Monday, Brussels",
    "- Helsinki suspects Russian helicopter airspace breach",
], size=15, lh=20)

# ---------------------------------------------------------------- numbers strip
NY = 336
panel(M, NY, W - 2 * M, 44)
d.text((M + 12, NY + 13), "THE DAY IN NUMBERS", font=F(SANS_B, 15), fill=RED)
nums = ("3 dead in Dymer - 14 missing - 24 body bags at Cikande - 29 workers "
        "missing - 264 kg of explosives seized - 720/9 by India - 35 killed "
        "in Nigeria - 24 killed in South Sudan")
f_num = F(SANS, 15)
lines = wrap(nums, f_num, W - 2 * M - 196)
for i, ln in enumerate(lines):
    d.text((M + 196, NY + 4 + i * 19), ln, font=f_num, fill=INK)

# ---------------------------------------------------------------- card row A
CW = (W - 2 * M - 2 * 12) // 3
RY1, RH1 = 388, 196
card(M, RY1, CW, RH1, "CLIMATE", GREEN, "COP31 collapses with no deal",
     ["- Longest climate summit on record, Antalya",
      "- Final draft never mentions fossil fuels",
      "- EU and UK reject the text outright",
      "- Albanese: 'difficult geopolitical times'"])
card(M + CW + 12, RY1, CW, RH1, "MIDDLE EAST", TEAL, "Bahrain takes Iran strike to UN",
     ["- Iranian hit on Sitra site wounds two",
      "- Bahrain demands UN action, compensation",
      "- Two tankers struck in Hormuz strait",
      "- Saudis intercept a Houthi missile"])
card(M + 2 * (CW + 12), RY1, CW, RH1, "ASIA - DISASTER", BROWN,
     "24 body bags in Cikande factory fire",
     ["- Candy plant in Serang, Banten, gutted",
      "- Factory says 29 workers still missing",
      "- Four in hospital; search resumes Monday",
      "- DNA identification may take 2-3 weeks"])

# ---------------------------------------------------------------- card row B
RY2, RH2 = 592, 140
card(M, RY2, CW, RH2, "SPORT - CRICKET", NAVY, "India pile up a record 720",
     ["- 720/9 declared against New Zealand",
      "- Wellington Test: a team record total"], head_size=19)
card(M + CW + 12, RY2, CW, RH2, "SPORT - FOOTBALL", NAVY,
     "Liverpool rout 10-man United",
     ["- Pochettino's first match ends in a rout",
      "- United finish with ten men at Anfield"], head_size=19)
card(M + 2 * (CW + 12), RY2, CW, RH2, "AFRICA - SUDAN", RED,
     "Drones hit Khartoum homes, UN site",
     ["- Strikes on homes and a UN building",
      "- South Sudan: 24 civilians killed"], head_size=19)

# ---------------------------------------------------------------- mini cards row C
RY3, RH3 = 740, 148
card(M, RY3, CW, RH3, "ASIA-PACIFIC", TEAL, "Kim: security, not supremacy",
     ["- Seoul minister quits in AI cheat row",
      "- Nepal PM Shah talks with Modi in Delhi"],
     head_size=18)
card(M + CW + 12, RY3, CW, RH3, "EUROPE", GREEN,
     "Lisbon marches on living costs",
     ["- Thousands march over living costs",
      "- UN lethal-AI talks go on, Geneva"],
     head_size=18)
card(M + 2 * (CW + 12), RY3, CW, RH3, "AMERICAS - MIDEAST", BROWN,
     "Bolsonaro stable in ICU",
     ["- Lebanon: 3 held with 264 kg explosives",
      "- Israel coalition talks end, no deal"],
     head_size=18)

# ---------------------------------------------------------------- IN BRIEF
UY, UH = 896, 92
panel(M, UY, W - 2 * M, UH)
d.text((M + 12, UY + 8), "IN BRIEF", font=F(SANS_B, 15), fill=RED)
text_block(M + 12, UY + 32, COLW, [
    "- WHO chief pleads for peace in Ebola-hit DR Congo",
    "- Nigeria: 35 Fulani killed in revenge attacks",
    "- UK to build Ukrainian drones in new defence deal",
], size=15, lh=20)
text_block(M + 12 + COLW + 14, UY + 32, COLW, [
    "- Chiefs sink Sundowns to reach the cup final",
    "- Soweto derby final: Chiefs v Orlando Pirates",
    "- Cikande: four workers still in hospital",
], size=15, lh=20)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
