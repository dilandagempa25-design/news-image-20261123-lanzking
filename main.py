#!/usr/bin/env python3
"""news-image-20261123 entry for @lanzking.

Draws one 1024x1024 PNG poster summing up the world news of
Monday 23 November 2026: a dated banner over a grid of eight
story tiles, each with a small drawn icon, a bold headline and
a one-line summary. Run:  python3 main.py   ->  entry.png
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "entry.png"

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (10, 22, 48)
WHITE = (255, 255, 255)
SOFT = (214, 224, 240)
AMBER = (255, 190, 60)
RED = (235, 70, 60)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- icons
# Every icon is drawn inside the box (x, y, s) with PIL primitives only.

def icon_globe_crack(d, x, y, s, ink):
    d.ellipse([x, y, x + s, y + s], outline=ink, width=5)
    d.ellipse([x + s * 0.32, y, x + s * 0.68, y + s], outline=ink, width=3)
    d.line([x + 4, y + s * 0.5, x + s - 4, y + s * 0.5], fill=ink, width=3)
    crack = [(x + s * 0.55, y + 2), (x + s * 0.44, y + s * 0.3),
             (x + s * 0.6, y + s * 0.52), (x + s * 0.47, y + s * 0.78),
             (x + s * 0.56, y + s - 2)]
    d.line(crack, fill=RED, width=6)


def icon_drone_ship(d, x, y, s, ink):
    # quadcopter: top bar, two rotor discs, hanging camera body
    cy = y + s * 0.16
    d.line([x + s * 0.14, cy, x + s * 0.86, cy], fill=ink, width=4)
    for rx in (0.14, 0.86):
        d.ellipse([x + (rx - 0.13) * s, cy - s * 0.07, x + (rx + 0.13) * s, cy + s * 0.07],
                  outline=ink, width=3)
    d.line([x + s * 0.5, cy, x + s * 0.5, cy + s * 0.1], fill=ink, width=4)
    d.rounded_rectangle([x + s * 0.4, cy + s * 0.1, x + s * 0.6, cy + s * 0.26],
                        radius=5, fill=ink)
    d.ellipse([x + s * 0.46, cy + s * 0.24, x + s * 0.54, cy + s * 0.32], fill=ink)
    # dashed drop line toward the ship
    for i in range(3):
        ly = cy + s * (0.38 + i * 0.09)
        d.line([x + s * 0.5, ly, x + s * 0.5, ly + s * 0.045], fill=RED, width=3)
    # ship hull + bridge
    hy = y + s * 0.66
    d.polygon([(x + s * 0.08, hy), (x + s * 0.92, hy), (x + s * 0.8, hy + s * 0.15),
               (x + s * 0.2, hy + s * 0.15)], outline=ink, width=4)
    d.rectangle([x + s * 0.4, hy - s * 0.13, x + s * 0.62, hy], outline=ink, width=4)
    # waves across the full width under the hull
    for i in range(4):
        wx = x + s * (0.02 + i * 0.24)
        d.arc([wx, hy + s * 0.17, wx + s * 0.2, hy + s * 0.29], 0, 180, fill=ink, width=3)


def icon_house_crack(d, x, y, s, ink):
    d.line([x + s * 0.08, y + s * 0.45, x + s * 0.5, y + s * 0.1], fill=ink, width=5)
    d.line([x + s * 0.5, y + s * 0.1, x + s * 0.92, y + s * 0.45], fill=ink, width=5)
    d.rectangle([x + s * 0.2, y + s * 0.45, x + s * 0.8, y + s * 0.92],
                outline=ink, width=5)
    crack = [(x + s * 0.52, y + s * 0.45), (x + s * 0.42, y + s * 0.62),
             (x + s * 0.55, y + s * 0.75), (x + s * 0.47, y + s * 0.92)]
    d.line(crack, fill=RED, width=5)
    # small heart of hope beside the door
    hx, hy = x + s * 0.68, y + s * 0.58
    d.ellipse([hx - 9, hy - 6, hx + 1, hy + 6], fill=AMBER)
    d.ellipse([hx - 1, hy - 6, hx + 9, hy + 6], fill=AMBER)
    d.polygon([(hx - 9, hy + 2), (hx + 9, hy + 2), (hx, hy + 14)], fill=AMBER)


def icon_chart(d, x, y, s, ink):
    d.line([x + s * 0.12, y + s * 0.08, x + s * 0.12, y + s * 0.88], fill=ink, width=4)
    d.line([x + s * 0.12, y + s * 0.88, x + s * 0.92, y + s * 0.88], fill=ink, width=4)
    pts = [(x + s * 0.16, y + s * 0.74), (x + s * 0.42, y + s * 0.6),
           (x + s * 0.58, y + s * 0.66), (x + s * 0.86, y + s * 0.2)]
    d.line(pts, fill=(90, 230, 120), width=7)
    ax, ay = pts[-1]
    d.polygon([(ax, ay), (ax - s * 0.16, ay + s * 0.02), (ax - s * 0.03, ay + s * 0.16)],
              fill=(90, 230, 120))


def icon_plane_x(d, x, y, s, ink):
    cy = y + s * 0.44
    # long slim fuselage with a pointed, slightly raised nose
    d.rounded_rectangle([x + s * 0.03, cy - s * 0.06, x + s * 0.86, cy + s * 0.06],
                        radius=11, fill=ink)
    d.polygon([(x + s * 0.8, cy - s * 0.06), (x + s * 0.98, cy + s * 0.01),
               (x + s * 0.84, cy + s * 0.06)], fill=ink)
    # main wing: clear triangle sweeping down and back from mid-body
    d.polygon([(x + s * 0.4, cy + s * 0.03), (x + s * 0.58, cy + s * 0.03),
               (x + s * 0.8, cy + s * 0.38), (x + s * 0.62, cy + s * 0.38)], fill=ink)
    # tail fin and rear stabiliser
    d.polygon([(x + s * 0.05, cy - s * 0.04), (x + s * 0.14, cy - s * 0.04),
               (x + s * 0.2, cy - s * 0.3), (x + s * 0.11, cy - s * 0.3)], fill=ink)
    d.polygon([(x + s * 0.05, cy + s * 0.04), (x + s * 0.16, cy + s * 0.04),
               (x + s * 0.22, cy + s * 0.18), (x + s * 0.12, cy + s * 0.18)], fill=ink)
    # cabin windows
    for i in range(4):
        wx = x + s * (0.58 + i * 0.065)
        d.ellipse([wx, cy - s * 0.028, wx + s * 0.032, cy + s * 0.004], fill=NAVY)
    # red X badge
    bx, by, br = x + s * 0.82, y + s * 0.8, s * 0.16
    d.ellipse([bx - br, by - br, bx + br, by + br], fill=RED)
    d.line([bx - br * 0.5, by - br * 0.5, bx + br * 0.5, by + br * 0.5], fill=WHITE, width=5)
    d.line([bx - br * 0.5, by + br * 0.5, bx + br * 0.5, by - br * 0.5], fill=WHITE, width=5)


def icon_controller(d, x, y, s, ink):
    d.rounded_rectangle([x + s * 0.05, y + s * 0.28, x + s * 0.95, y + s * 0.74],
                        radius=26, outline=ink, width=5)
    cx, cy = x + s * 0.28, y + s * 0.51
    d.rectangle([cx - 5, cy - 16, cx + 5, cy + 16], fill=ink)
    d.rectangle([cx - 16, cy - 5, cx + 16, cy + 5], fill=ink)
    for dx, dy in [(0.68, 0.42), (0.8, 0.55)]:
        d.ellipse([x + dx * s - 8, y + dy * s - 8, x + dx * s + 8, y + dy * s + 8],
                  fill=ink)


def icon_cross(d, x, y, s, ink):
    d.ellipse([x + s * 0.06, y + s * 0.06, x + s * 0.94, y + s * 0.94],
              outline=ink, width=5)
    cx, cy = x + s * 0.5, y + s * 0.5
    d.rectangle([cx - s * 0.09, cy - s * 0.26, cx + s * 0.09, cy + s * 0.26], fill=RED)
    d.rectangle([cx - s * 0.26, cy - s * 0.09, cx + s * 0.26, cy + s * 0.09], fill=RED)


def icon_trophy(d, x, y, s, ink):
    d.polygon([(x + s * 0.28, y + s * 0.12), (x + s * 0.72, y + s * 0.12),
               (x + s * 0.68, y + s * 0.5), (x + s * 0.32, y + s * 0.5)], fill=AMBER)
    d.arc([x + s * 0.17, y + s * 0.13, x + s * 0.37, y + s * 0.45], 90, 270,
          fill=AMBER, width=6)
    d.arc([x + s * 0.63, y + s * 0.13, x + s * 0.83, y + s * 0.45], 270, 90,
          fill=AMBER, width=6)
    d.rectangle([x + s * 0.45, y + s * 0.5, x + s * 0.55, y + s * 0.68], fill=AMBER)
    d.rectangle([x + s * 0.32, y + s * 0.68, x + s * 0.68, y + s * 0.8], fill=AMBER)


ICONS = {
    "globe": icon_globe_crack,
    "drone": icon_drone_ship,
    "house": icon_house_crack,
    "chart": icon_chart,
    "plane": icon_plane_x,
    "pad": icon_controller,
    "cross": icon_cross,
    "trophy": icon_trophy,
}

# ------------------------------------------------------------- content
# (region tag, headline, one-line summary, tile colour, icon)
STORIES = [
    ("CLIMATE - ANTALYA", "COP31 TALKS COLLAPSE",
     "Summit ends with no deal; 130+ nations reject draft on fossil fuels",
     (18, 82, 74), "globe"),
    ("LIBYA - BENGHAZI", "WARSHIP SUNK BY SEA DRONES",
     "Ukraine drones sink Russia's Merkury; UN calls for a probe",
     (36, 72, 110), "drone"),
    ("UKRAINE - KYIV REGION", "STRIKES KILL 12",
     "Russian strikes hit Kyiv region; boy of 7 pulled alive from rubble",
     (104, 72, 44), "house"),
    ("TECH - NVIDIA", "NVIDIA SHARES SOAR 30%",
     "Jensen Huang back as CEO; US blacklists Megaspeed over AI chips",
     (40, 102, 52), "chart"),
    ("TRAVEL - ATLANTA", "DELTA GROUND STOP",
     "Load-system crash; 1,300 flights delayed on Thanksgiving eve",
     (118, 46, 54), "plane"),
    ("GAMES - GTA VI", "GTA VI SMASHES RECORDS",
     "$3.79B day-one haul, the biggest in entertainment history",
     (88, 56, 118), "pad"),
    ("AFRICA - DR CONGO", "EBOLA TEAMS TRAPPED",
     "Fighting in Ituri strands responders near a hospital - WHO",
     (94, 104, 44), "cross"),
    ("SPORT", "UK TO HOST 2035 WORLD CUP",
     "FIFA confirms women's cup; Alcaraz wins first ATP Finals title",
     (140, 100, 20), "trophy"),
]


def main():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # ---- banner (date auto-fitted to the canvas width)
    d.rectangle([0, 0, W, 10], fill=RED)
    d.text((48, 30), "MONDAY - THE DAY IN NEWS", font=font(BOLD, 32), fill=AMBER)
    right = "8 STORIES - ONE DAY"
    d.text((W - 48 - d.textlength(right, font=font(BOLD, 32)), 30), right,
           font=font(BOLD, 32), fill=SOFT)
    size = 116
    while size > 40 and d.textlength("23 NOVEMBER 2026", font=font(BOLD, size)) > W - 96:
        size -= 2
    d.text((46, 68), "23 NOVEMBER 2026", font=font(BOLD, size), fill=WHITE)
    d.line([48, 204, W - 48, 204], fill=AMBER, width=4)

    # ---- tile grid: 2 columns x 4 rows
    gx, gy, gap = 24, 224, 12
    tw = (W - gx * 2 - gap) // 2
    th = (H - gy - 20 - 3 * gap) // 4
    f_tag = font(BOLD, 20)
    f_head = font(BOLD, 31)
    f_sum = font(REG, 22)

    for i, (tag, head, summ, colour, icon) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = gx + col * (tw + gap)
        y = gy + row * (th + gap)
        edge = tuple(min(255, c + 38) for c in colour)
        d.rounded_rectangle([x, y, x + tw, y + th], radius=18, fill=colour, outline=edge, width=2)
        ICONS[icon](d, x + 20, y + (th - 100) // 2, 100, WHITE)
        tx = x + 138
        max_w = x + tw - tx - 12
        head_lines = wrap(d, head, f_head, max_w)
        sum_lines = wrap(d, summ, f_sum, max_w)[:3]
        # vertically centre the whole text block inside the tile
        block_h = 24 + len(head_lines) * 35 + 4 + len(sum_lines) * 26
        ty = y + (th - block_h) // 2
        d.text((tx, ty), tag, font=f_tag, fill=AMBER)
        hy = ty + 28
        for line in head_lines:
            d.text((tx, hy), line, font=f_head, fill=WHITE)
            hy += 35
        sy = hy + 4
        for line in sum_lines:
            d.text((tx, sy), line, font=f_sum, fill=SOFT)
            sy += 26

    img.save(OUT, optimize=True)
    print("saved", OUT)


if __name__ == "__main__":
    main()
