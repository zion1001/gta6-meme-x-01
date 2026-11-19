#!/usr/bin/env python3
"""Draw the GTA 6 meme: 'WAITED 13 YEARS FOR GTA 6'.

A flat-illustration living room at night. A tired gamer slumps on the couch
in front of a TV glowing with a Vice City sunset; make.fun's white ghost
mascot sits on the couch beside him, holding its magenta star coin, with a
small pile of gold coins next to it. Huge outlined type top and bottom so the
joke reads even when the picture is shrunk to 480x480.

The ghost comes from entry/ghost.png: the official make.fun mark with the
magenta disc flood-filled away, leaving only the ghost (see extract_ghost.py
and cleanup_ghost.py in the work root).
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
GHOST = HERE / "ghost.png"
OUT = HERE / "meme.png"

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# Palette.
BAND = (21, 15, 30)          # near-black headline bands
MAGENTA = (196, 28, 131)     # make.fun magenta
PINK = (255, 94, 138)
ORANGE = (255, 154, 61)
WALL_TOP = (38, 27, 63)
WALL_BOT = (24, 18, 46)
FLOOR = (74, 50, 38)
COUCH = (124, 66, 50)
COUCH_DARK = (93, 47, 36)
COUCH_LIGHT = (138, 74, 56)
SKIN = (234, 185, 140)
HAIR = (43, 33, 24)
HOODIE = (61, 110, 106)
JEANS = (51, 80, 122)
GOLD = (247, 201, 72)
GOLD_DARK = (166, 124, 0)
WHITE = (255, 255, 255)
BLACK = (10, 8, 14)


def font(size):
    return ImageFont.truetype(BOLD, size)


def fit_font(text, max_width, start_size):
    """Largest bold size (down to 24) whose text fits max_width."""
    size = start_size
    while size > 24:
        f = font(size)
        if f.getlength(text) <= max_width:
            return f
        size -= 2
    return font(24)


def outlined_text(draw, xy, text, fnt, fill, stroke_width):
    draw.text(xy, text, font=fnt, fill=fill, anchor="mm",
              stroke_width=stroke_width, stroke_fill=BLACK)


def vgrad(size, top, bottom):
    """Vertical gradient image."""
    w, h = size
    base = Image.new("RGB", (1, h))
    px = base.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        px[0, y] = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    return base.resize((w, h))


def sunset_screen(draw, box):
    """Neon Vice City sunset inside the TV screen box."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    grad = vgrad((w, h), (255, 170, 80), (123, 47, 190))
    screen = grad.convert("RGBA")
    sd = ImageDraw.Draw(screen)
    # Low sun.
    sd.ellipse([w * 0.38, h * 0.42, w * 0.62, h * 0.82], fill=(255, 233, 168, 255))
    # Sea / horizon glow.
    sd.rectangle([0, h * 0.72, w, h], fill=(70, 20, 90, 255))
    # Palm silhouettes.
    palm = (28, 16, 48, 255)

    def palm_tree(bx, by, s):
        # Trunk: slightly curved, drawn as a thick polyline.
        pts = [(bx, by), (bx + 6 * s, by - 55 * s), (bx + 2 * s, by - 105 * s)]
        sd.line(pts, fill=palm, width=max(6, int(10 * s)), joint="curve")
        top = (bx + 2 * s, by - 105 * s)
        # Fronds: thick curves that arc out and droop down at the tip.
        for ang in (-160, -120, -80, -40, 0):
            a = math.radians(ang)
            mid = (top[0] + 34 * s * math.cos(a),
                   top[1] + 34 * s * math.sin(a) * 0.55 - 6 * s)
            end = (top[0] + 58 * s * math.cos(a),
                   top[1] + 58 * s * math.sin(a) * 0.55 + 12 * s)
            sd.line([top, mid, end], fill=palm, width=max(5, int(8 * s)),
                    joint="curve")

    palm_tree(w * 0.10, h * 0.98, 0.9)
    palm_tree(w * 0.88, h * 0.98, 1.1)
    return screen


def main():
    img = Image.new("RGB", (W, H), BAND)
    d = ImageDraw.Draw(img)

    # --- Top headline band -------------------------------------------------
    d.rectangle([0, 0, W, 168], fill=BAND)
    d.rectangle([0, 164, W, 170], fill=MAGENTA)
    f_top = fit_font("WAITED 13 YEARS", 940, 92)
    outlined_text(d, (W // 2, 56), "WAITED 13 YEARS", f_top, WHITE, 7)
    f_top2 = fit_font("FOR GTA 6", 940, 92)
    outlined_text(d, (W // 2, 132), "FOR GTA 6", f_top2, WHITE, 7)

    # --- Wall --------------------------------------------------------------
    wall = vgrad((W, 632), WALL_TOP, WALL_BOT)
    img.paste(wall, (0, 170))
    d = ImageDraw.Draw(img)
    # A few faint stars.
    for (sx, sy, r) in [(90, 210, 2), (150, 300, 2), (950, 240, 2),
                        (880, 330, 2), (60, 420, 2), (980, 470, 2)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(200, 190, 230))

    # --- Wall clock: 3 AM, he has been waiting all night --------------------
    cx, cy, cr = 905, 235, 36
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(240, 235, 225),
              outline=BLACK, width=4)
    d.line([cx, cy, cx, cy - 22], fill=BLACK, width=4)
    d.line([cx, cy, cx + 18, cy], fill=BLACK, width=4)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=BLACK)

    # --- TV glow + TV --------------------------------------------------------
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([150, 150, 874, 560], fill=(255, 120, 80, 70))
    glow = glow.filter(ImageFilter.GaussianBlur(45))
    img.paste(Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB"),
              (0, 0))
    d = ImageDraw.Draw(img)
    # Bezel and stand.
    d.rounded_rectangle([196, 196, 828, 524], radius=14, fill=(12, 10, 16))
    screen = sunset_screen(d, (212, 212, 812, 508))
    img.paste(screen, (212, 212))
    d = ImageDraw.Draw(img)
    f_tv = fit_font("GTA VI", 560, 118)
    outlined_text(d, (512, 350), "GTA VI", f_tv, WHITE, 8)
    # Console under the TV.
    d.rounded_rectangle([330, 524, 694, 552], radius=8, fill=(30, 24, 40))

    # --- Floor ---------------------------------------------------------------
    d.rectangle([0, 770, W, 800], fill=FLOOR)
    d.line([0, 784, W, 784], fill=(58, 38, 28), width=2)

    # --- Couch ---------------------------------------------------------------
    # Back, seat, armrests.
    d.rounded_rectangle([60, 556, 964, 700], radius=26, fill=COUCH)
    d.rounded_rectangle([88, 580, 500, 692], radius=20, fill=COUCH_LIGHT)
    d.rounded_rectangle([524, 580, 936, 692], radius=20, fill=COUCH_LIGHT)
    d.rounded_rectangle([60, 688, 964, 782], radius=22, fill=COUCH_DARK)
    d.rounded_rectangle([84, 694, 500, 778], radius=16, fill=COUCH)
    d.rounded_rectangle([524, 694, 940, 778], radius=16, fill=COUCH)
    d.rounded_rectangle([60, 636, 122, 782], radius=18, fill=COUCH_DARK)
    d.rounded_rectangle([902, 636, 964, 782], radius=18, fill=COUCH_DARK)
    # Little wooden feet.
    d.rectangle([86, 782, 104, 794], fill=(40, 26, 18))
    d.rectangle([920, 782, 938, 794], fill=(40, 26, 18))

    # --- Gamer, slumped on the left ------------------------------------------
    # Legs stretched along the couch.
    d.rounded_rectangle([372, 712, 560, 748], radius=16, fill=JEANS)
    d.rounded_rectangle([372, 748, 552, 780], radius=14, fill=(43, 68, 104))
    # Shoes.
    d.rounded_rectangle([548, 706, 612, 742], radius=10, fill=(24, 22, 28))
    d.rounded_rectangle([544, 742, 606, 778], radius=10, fill=(24, 22, 28))
    d.line([548, 736, 612, 736], fill=WHITE, width=3)
    d.line([544, 772, 606, 772], fill=WHITE, width=3)
    # Hoodie body, leaning left against the armrest.
    d.rounded_rectangle([196, 648, 392, 770], radius=30, fill=HOODIE)
    d.ellipse([232, 632, 312, 690], fill=(49, 88, 84))  # hood behind head
    # Arms down to the controller.
    d.rounded_rectangle([214, 690, 258, 748], radius=16, fill=(49, 88, 84))
    d.rounded_rectangle([330, 690, 374, 748], radius=16, fill=(49, 88, 84))
    # Controller in his lap.
    d.rounded_rectangle([272, 726, 372, 762], radius=12, fill=(28, 26, 34))
    d.ellipse([288, 736, 304, 752], fill=(90, 90, 100))
    d.ellipse([340, 736, 356, 752], fill=(90, 90, 100))
    for (bx, by, col) in [(318, 734, (90, 200, 90)), (330, 734, (230, 60, 60)),
                          (318, 746, (60, 120, 230)), (330, 746, (240, 200, 60))]:
        d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=col)
    # Hands on the controller.
    d.ellipse([282, 748, 306, 768], fill=SKIN)
    d.ellipse([344, 748, 368, 768], fill=SKIN)
    # Head, tilted, half asleep.
    d.ellipse([218, 556, 322, 660], fill=SKIN)
    # Hair cap.
    d.pieslice([214, 548, 326, 640], start=180, end=360, fill=HAIR)
    # Tired closed eyes.
    d.arc([238, 600, 262, 618], start=200, end=340, fill=BLACK, width=4)
    d.arc([278, 600, 302, 618], start=200, end=340, fill=BLACK, width=4)
    # Flat mouth.
    d.line([258, 640, 282, 640], fill=BLACK, width=4)
    # Little "z z" — asleep on the job of waiting.
    d.text((340, 560), "z z", font=font(34), fill=(154, 147, 184))

    # --- Ghost, sitting on the couch beside him ------------------------------
    ghost = Image.open(GHOST).convert("RGBA")
    gh = 235
    gw = int(ghost.width * gh / ghost.height)
    ghost = ghost.resize((gw, gh), Image.LANCZOS)
    ghost = ghost.rotate(-3, resample=Image.BICUBIC, expand=True)
    # Soft contact shadow on the seat.
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shd = ImageDraw.Draw(shadow)
    shd.ellipse([632, 748, 892, 776], fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(6))
    img = Image.alpha_composite(img.convert("RGBA"), shadow)
    img.alpha_composite(ghost, (650, 518))
    d = ImageDraw.Draw(img)

    # --- Pile of gold coins next to the ghost --------------------------------
    def coin(cx, cy, r=20):
        # Face-on coin: full gold disc with a $ in the middle.
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD,
                  outline=GOLD_DARK, width=3)
        d.text((cx, cy), "$", font=font(22), fill=GOLD_DARK, anchor="mm")

    coin(912, 752)
    coin(938, 752)
    coin(925, 728)

    # --- Bottom punchline band ------------------------------------------------
    d.rectangle([0, 800, W, H], fill=BAND)
    d.rectangle([0, 800, W, 806], fill=MAGENTA)
    f_bot1 = fit_font("MY AI AGENT EARNED REAL MONEY", 940, 58)
    outlined_text(d, (W // 2, 866), "MY AI AGENT EARNED REAL MONEY",
                  f_bot1, WHITE, 6)
    # Second line with MAKE.FUN in magenta.
    f_bot2 = font(58)
    while f_bot2.getlength("ON MAKE.FUN WHILE I WAITED") > 940 and f_bot2.size > 24:
        f_bot2 = font(f_bot2.size - 2)
    left = "ON "
    mid = "MAKE.FUN"
    right = " WHILE I WAITED"
    total = f_bot2.getlength(left + mid + right)
    x = (W - total) / 2
    y = 946
    for text, fill in [(left, WHITE), (mid, (255, 46, 154)), (right, WHITE)]:
        d.text((x, y), text, font=f_bot2, fill=fill, anchor="lm",
               stroke_width=6, stroke_fill=BLACK)
        x += f_bot2.getlength(text)

    img.convert("RGB").save(OUT, optimize=True)
    print("saved", OUT, img.size)


if __name__ == "__main__":
    main()
