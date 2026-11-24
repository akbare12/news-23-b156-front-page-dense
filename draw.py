#!/usr/bin/env python3
"""Draw the front page for news-23 b156 (front-page-dense).
31 stories from Monday 23 November 2026. Output: entry.png 1024x1024.
Run: python3 draw.py  -> writes entry.png next to this file (build-time only).
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (250, 248, 243)
INK = (18, 18, 18)
RED = (178, 34, 34)
NAVY = (16, 32, 64)
GOLD = (201, 162, 39)
GREY = (110, 110, 110)
LIGHT = (238, 234, 226)

FD = "/usr/share/fonts/truetype/dejavu/"
FL = "/usr/share/fonts/truetype/liberation/"


def font(size, bold=False, italic=False):
    if italic:
        return ImageFont.truetype(FL + "LiberationSans-Italic.ttf", size)
    if bold:
        return ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", size)
    return ImageFont.truetype(FD + "DejaVuSans.ttf", size)


def wrap(d, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, fnt, fill, maxw, lh=None, max_lines=None):
    lines = wrap(d, text, fnt, maxw)
    if max_lines:
        lines = lines[:max_lines]
    lh = lh or int(fnt.size * 1.25)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def chip(d, x, y, label, fill):
    f = font(9, bold=True)
    w = int(d.textlength(label, font=f) + 10)
    d.rounded_rectangle([x, y, x + w, y + 14], radius=3, fill=fill)
    d.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return w


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# ---------- masthead ----------
d.text((10, 10), "THE WORLD TODAY", font=font(40, bold=True), fill=INK)
d.text((1024 - 10 - d.textlength("MONDAY 23 NOVEMBER 2026", font=font(15, bold=True)), 16),
       "MONDAY 23 NOVEMBER 2026", font=font(15, bold=True), fill=RED)
d.text((1024 - 10 - d.textlength("GLOBAL EDITION", font=font(11)), 38),
       "GLOBAL EDITION", font=font(11), fill=GREY)
d.line([10, 62, 1014, 62], fill=INK, width=3)

# ---------- kicker ----------
d.text((10, 68), "AI rout hits Asia  ·  Guterres calls for AI rules  ·  US lead over China at record low",
       font=font(13, italic=True), fill=(60, 60, 60))

# ---------- number strip ----------
nums = [
    ("-3.3%", "KOSPI"), ("5.3", "POWER GAP"), ("11,762", "EBOLA CASES DRC"),
    ("10T won", "SEOUL FUND"), ("2%", "BILLIONAIRE TAX"),
    ("$450M", "SKUBAL DEAL"), ("165", "MISSILES / WEEK"),
    ("12,000", "CLEARED MANCHESTER"), ("264 kg", "EXPLOSIVES SEIZED"),
    ("$107.3B", "ANTHROPIC IPO"),
]
d.rectangle([10, 88, 1014, 150], outline=(200, 196, 188), width=1)
for i, (v, lab) in enumerate(nums):
    col, row = i % 5, i // 5
    x = 10 + col * 201
    y = 90 + row * 30
    d.text((x + 8, y), v, font=font(17, bold=True), fill=RED if i == 0 else INK)
    d.text((x + 8, y + 18), lab, font=font(8, bold=True), fill=GREY)

# ---------- region bar ----------
d.rectangle([10, 154, 1014, 172], fill=NAVY)
d.text((18, 158), "ASIA-PACIFIC 7    ·    AMERICAS 8    ·    MIDDLE EAST 6    ·    EUROPE 5    ·    AFRICA 3    ·    WORLD 2",
       font=font(11, bold=True), fill=(255, 255, 255))

# ---------- section bar ----------
d.rectangle([10, 176, 1014, 196], fill=INK)
d.text((18, 180), "THE DAY'S BIG STORIES", font=font(13, bold=True), fill=(255, 255, 255))

# ---------- heroes ----------
HX = [10, 348, 686]
HW = 328
heroes = [
    dict(kind="kospi", head="AI ROUT HITS ASIA",
         body="Kospi falls 3.3% to 4,708.54, shedding 161 points; intraday slide hits 5.8%. Samsung -3.1%, SK Hynix -2.5%.",
         src="SEOUL MARKETS"),
    dict(kind="guterres", head="GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
         body="UN chief urges binding rules at the Bridgetown summit as 150 delegates back a risk framework — a blueprint, not a treaty.",
         src="BRIDGETOWN, BARBADOS"),
    dict(kind="power", head="US LEAD OVER CHINA AT RECORD LOW",
         body="Asia Power Index 2026: US 78.9, China 73.6 — a 5.3 gap, the narrowest since 2018. India third at 40.5.",
         src="ASIA POWER INDEX 2026"),
]
for x, h in zip(HX, heroes):
    # scene panel y200-318
    d.rectangle([x, 200, x + HW, 318], fill=NAVY)
    if h["kind"] == "kospi":
        # lit buildings
        for bx, bh in [(x + 14, 58), (x + 44, 82), (x + 76, 66), (x + 108, 96),
                       (x + 140, 74), (x + 172, 88), (x + 204, 62), (x + 236, 78),
                       (x + 268, 70), (x + 296, 58)]:
            d.rectangle([bx, 318 - bh, bx + 24, 318], fill=(28, 52, 96))
            for wy in range(318 - bh + 8, 312, 16):
                d.rectangle([bx + 5, wy, bx + 9, wy + 5], fill=(255, 214, 120))
                d.rectangle([bx + 15, wy, bx + 19, wy + 5], fill=(255, 214, 120))
        # falling orange chart line, kept clear of the big number (top-left)
        pts = [(x + 150, 218), (x + 180, 226), (x + 210, 222), (x + 240, 238),
               (x + 270, 246), (x + 300, 262), (x + 322, 276)]
        d.line(pts, fill=(255, 140, 40), width=3)
        for px, py in pts:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 140, 40))
        d.text((x + 12, 206), "-3.3%", font=font(30, bold=True), fill=(255, 255, 255))
        # solid caption band at the bottom of the scene so the gold text
        # is never crossed by building tops or windows
        d.rectangle([x, 290, x + HW, 318], fill=NAVY)
        d.text((x + 12, 296), "KOSPI 4,708.54 · -161 PTS", font=font(10, bold=True), fill=(255, 214, 120))
    elif h["kind"] == "guterres":
        # globe, kept to the right so the text column on the left stays clear
        cx, cy, r = x + 258, 256, 42
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(38, 90, 150))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 214, 120), width=2)
        for ang in range(0, 360, 60):
            a = math.radians(ang)
            d.arc([cx - r, cy - r, cx + r, cy + r], ang, ang + 40, fill=(120, 180, 220), width=2)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=GOLD)
        d.text((x + 12, 206), "150", font=font(30, bold=True), fill=GOLD)
        d.text((x + 12, 242), "DELEGATES", font=font(11, bold=True), fill=(255, 255, 255))
        d.text((x + 12, 258), "BACK A RISK", font=font(11, bold=True), fill=(255, 255, 255))
        d.text((x + 12, 274), "FRAMEWORK", font=font(11, bold=True), fill=(255, 255, 255))
        d.text((x + 12, 296), "BRIDGETOWN SUMMIT", font=font(10, bold=True), fill=(255, 214, 120))
    else:
        # power bars
        bars = [("US", 78.9, (255, 255, 255)), ("CHINA", 73.6, (255, 140, 40)),
                ("INDIA", 40.5, GOLD)]
        d.text((x + 12, 206), "GAP 5.3", font=font(24, bold=True), fill=(255, 255, 255))
        d.text((x + 130, 212), "NARROWEST SINCE 2018", font=font(10, bold=True), fill=(255, 214, 120))
        for i, (lab, val, col) in enumerate(bars):
            by = 240 + i * 26
            bw = int(val * 2.6)
            d.rectangle([x + 12, by, x + 12 + bw, by + 16], fill=col)
            # labels sit on the navy background past the bar end: always white
            d.text((x + 18 + bw, by + 1), f"{val}  {lab}", font=font(11, bold=True),
                   fill=(255, 255, 255))
    # headline + body + source/chip (headline kept below the scene panel)
    y = text_block(d, x, 324, h["head"], font(14, bold=True), INK, HW, lh=17, max_lines=2)
    y = text_block(d, x, y + 2, h["body"], font(11), (50, 50, 50), HW, lh=14, max_lines=2)
    d.text((x, 404), h["src"], font=font(9, bold=True), fill=GREY)
    chip(d, x + HW - 62, 402, "REPORTED", (30, 120, 60))

# ---------- cards ----------
d.line([10, 424, 1014, 424], fill=INK, width=2)
d.text((10, 429), "MORE OF THE DAY", font=font(11, bold=True), fill=INK)
cards = [
    ("BESSENT DEMANDS NVIDIA ANSWERS", "Presses chipmaker over China sales.", "WASHINGTON", False),
    ("FBI PROBES NCIC POLICE-DATABASE HACK", "Bureau probes a breach of the crime DB.", "WASHINGTON", False),
    ("TRUMP: IRAN STRIKES MAY RESUME", "President says strikes could return.", "WASHINGTON", False),
    ("NASDAQ FUTURES JUMP 3%", "Holiday-week rally lifts US futures.", "NEW YORK", False),
    ("SKUBAL'S $450M METS DEAL", "Cy Young winner signs nine years.", "NEW YORK", False),
    ("TOM JACKSON DIES AT 75", "Former NFL star and broadcaster dies.", "DENVER", False),
    ("STATES SUE SPACEX OVER AI SAFETY", "Attorneys general challenge AI safety.", "WASHINGTON", False),
    ("ANTHROPIC IPO AT $107.3B", "Priced at $83; debut close $97.17.", "NEW YORK", False),
    ("POLAND: 3 MISSILES CROSSED AIRSPACE", "Three Kh-101s entered Polish skies.", "WARSAW", True),
    ("INTEL WARNS OF RUSSIAN NUCLEAR SATELLITE", "US intelligence flags a satellite threat.", "WASHINGTON", True),
]
CW, CG = 196, 6
for i, (head, body, src, claim) in enumerate(cards):
    col, row = i % 5, i // 5
    x = 10 + col * (CW + CG)
    y = 448 + row * 58
    d.rectangle([x, y, x + CW, y + 54], outline=(210, 206, 198), width=1)
    text_block(d, x + 5, y + 3, head, font(10, bold=True), INK, CW - 10, lh=12, max_lines=2)
    text_block(d, x + 5, y + 27, body, font(9), (70, 70, 70), CW - 10, lh=11, max_lines=1)
    d.text((x + 5, y + 41), src, font=font(8, bold=True), fill=GREY)
    chip(d, x + CW - 58, y + 40, "CLAIM" if claim else "REPORTED",
         (178, 34, 34) if claim else (30, 120, 60))

# ---------- map + ALSO ----------
d.rectangle([10, 568, 1014, 586], fill=INK)
d.text((18, 572), "WHERE IT HAPPENED", font=font(11, bold=True), fill=(255, 255, 255))
# map blobs (stylised continents)
mx0, my0 = 10, 592
d.rectangle([mx0, my0, mx0 + 340, my0 + 190], fill=(226, 232, 222))
# Americas blob
d.polygon([(30, 620), (70, 600), (110, 612), (120, 660), (100, 720), (70, 760),
           (45, 730), (25, 680)], fill=(196, 210, 190))
# Eurasia blob
d.polygon([(150, 610), (330, 600), (345, 640), (320, 690), (270, 700), (220, 720),
           (180, 700), (150, 660)], fill=(196, 210, 190))
# Africa blob
d.polygon([(180, 700), (230, 700), (250, 740), (235, 775), (200, 772), (185, 735)],
          fill=(196, 210, 190))
pins = [
    (1, 300, 640), (2, 92, 700), (3, 320, 632), (4, 62, 660), (5, 78, 640),
    (6, 268, 640), (7, 236, 648), (8, 218, 632), (9, 252, 628), (10, 206, 616),
    (11, 296, 668), (12, 282, 682), (13, 224, 736),
]
for n, px, py in pins:
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
    d.text((px - 3 if n < 10 else px - 6, py - 6), str(n), font=font(9, bold=True),
           fill=(255, 255, 255))
d.text((mx0, 786), "Pins 1-13: Seoul · Bridgetown · Beijing · Washington · New York · Kyiv · Paris ·",
       font=font(9), fill=GREY)
d.text((mx0, 798), "London · Warsaw · Manchester · Beirut · Gaza · Khartoum",
       font=font(9), fill=GREY)

# ALSO list, 2 columns x 9
also = [
    "Paris: 100+ back 2% billionaire tax",
    "Manchester: 12,000 cleared after scare",
    "Zelenskyy: 165 Russian missiles in a week",
    "COP31: the day after Antalya pact rejected",
    "Israel unity talks resume",
    "Gaza: two killed in Israeli strike",
    "West Bank settler attacks",
    "Iran war: no deal in sight",
    "Lebanon seizes 264 kg explosives",
    "Bahrain: Iranian strike hits plant, 2 hurt",
    "Benghazi: UN demands probe of port attacks [CLAIM]",
    "Sudan: air defences down drones over Khartoum [CLAIM]",
    "DRC: fighting traps Ebola teams",
    "Bangladesh: Hasina jailed if she returns",
    "Seoul minister quits over AI exam chaos",
    "SK Telecom -7.3%",
    "China eases margin rules, cuts to 80%",
    "Seoul readies 10T-won stabilisation fund",
]
d.text((370, 592), "ALSO ON MONDAY", font=font(11, bold=True), fill=INK)
for i, item in enumerate(also):
    col, row = i // 9, i % 9
    x = 370 + col * 325
    y = 610 + row * 20
    num = f"{14 + i}."
    d.text((x, y), num, font=font(10, bold=True), fill=RED)
    label = item.replace(" [CLAIM]", "")
    claim = "[CLAIM]" in item
    tw = d.textlength(label, font=font(10))
    d.text((x + 26, y), label, font=font(10), fill=INK)
    if claim:
        d.text((x + 26 + tw + 4, y), "[CLAIM]", font=font(10, bold=True), fill=RED)

# ---------- DATE CHECK ----------
d.rectangle([10, 824, 1014, 936], outline=RED, width=2)
d.rectangle([10, 824, 1014, 846], fill=RED)
d.text((18, 829), "DATE CHECK — LEFT OUT (NOT 23 NOVEMBER)", font=font(12, bold=True),
       fill=(255, 255, 255))
d.text((18, 852), "Democrats reach 258 (22 Nov)  ·  Sparta II fire (22 Nov)  ·  El Chapo Isidro captured (22 Nov)",
       font=font(11), fill=INK)
d.text((18, 870), "EU–Indonesia pact (21 Nov)  ·  Nigeria boat (21 Nov)  ·  ICJ Myanmar ruling (19 Nov)",
       font=font(11), fill=INK)
d.text((18, 892), "NOT YET:  Dymer search continues (14 missing)  ·  4 House races uncalled  ·  COP32 venue not set",
       font=font(11, bold=True), fill=INK)
d.text((18, 910), "WHO evacuating trapped Ebola staff", font=font(11, bold=True), fill=INK)

# ---------- footer ----------
d.line([10, 944, 1014, 944], fill=INK, width=2)
d.text((10, 950), "Sources: AP · Reuters · Bloomberg · WSJ · Lowy Institute · UN",
       font=font(10), fill=GREY)
d.text((10, 968), "REPORTED = confirmed by wires   ·   CLAIM = one side's claim   ·   ~ = approximate time",
       font=font(10), fill=GREY)
d.text((10, 988), "THE WORLD TODAY — Monday 23 November 2026 — 31 stories",
       font=font(10, bold=True), fill=INK)

img.save("entry.png")
print("saved entry.png", img.size)
