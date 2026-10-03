"""Вариант 3: Тетевен – привлекателна туристическа дестинация."""

import math

from cartoon import (BGMap, H, INK, Scene, W, bob, circle, cloud, confetti, drifting_clouds,
                     ease, ellipse, hills, house, label, mountains, paint, person, poly, pop,
                     rgb, rrect, sky, snow, sparkles, stroke_line, sun, text, title_card, tree)

TITLE = "Тетевен – най-зеленият град"
VOICE = "bg-BG-KalinaNeural"

PEAKS = [(130, 300, 230), (430, 380, 280), (800, 340, 280), (1130, 300, 250)]


def valley(ctx, t, river=True, green="#74c69d"):
    sky(ctx)
    sun(ctx, 1110, 100, t)
    drifting_clouds(ctx, t, seed=7)
    mountains(ctx, PEAKS, 480, "#52b788", snow=False)
    for i in range(12):
        tree(ctx, 40 + i * 110, 470 + (i % 2) * 10, 0.55, t, "#2d6a4f", kind="pine")
    hills(ctx, 480, green, 10)
    if river:
        river_path(ctx, t)


def river_path(ctx, t):
    ctx.new_path()
    ctx.move_to(-10, 540)
    ctx.curve_to(300, 500, 500, 600, 800, 540)
    ctx.curve_to(1000, 500, 1150, 560, W + 10, 530)
    ctx.line_to(W + 10, 580)
    ctx.curve_to(1150, 610, 1000, 560, 800, 600)
    ctx.curve_to(500, 660, 300, 560, -10, 600)
    ctx.close_path()
    paint(ctx, "#48cae4")
    for i in range(10):
        x = (i * 140 + t * 60) % (W + 40) - 20
        y = 560 + math.sin(x / 200) * 20
        stroke_line(ctx, [(x, y), (x + 30, y)], 4, "#ffffff")


def town(ctx, base, t, s=0.8):
    for i, x in enumerate((420, 520, 620, 720, 820)):
        house(ctx, x, base + (i % 2) * 8, s, wall=["#f4d7a8", "#fff1e6", "#ffe5b4"][i % 3],
              roof=["#c8553d", "#b5332e", "#d1603d"][i % 3])


def car(ctx, x, y, s=1.0, color="#ffb703"):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -110, -60, 220, 48, 16, color)
    poly(ctx, [(-60, -60), (-34, -100), (44, -100), (70, -60)], color)
    poly(ctx, [(-48, -64), (-28, -94), (2, -94), (2, -64)], "#bde0fe", 3)
    poly(ctx, [(12, -64), (12, -94), (40, -94), (58, -64)], "#bde0fe", 3)
    for wx in (-62, 62):
        circle(ctx, wx, -12, 22, "#333333")
        circle(ctx, wx, -12, 8, "#bbbbbb", 3)
    ctx.restore()


def s_arrive(ctx, t, d):
    sky(ctx)
    sun(ctx, 1110, 100, t)
    drifting_clouds(ctx, t, seed=7)
    m = BGMap(30, 50, 600)
    m.draw(ctx, "#b7e4c7")
    m.dot(ctx, "София", 1, size=22, above=False)
    m.dot(ctx, "Тетевен", pop(t, 0.5), "#2d6a4f", size=22)
    a, b = m.city("София"), m.city("Тетевен")
    f = ease((t - 0.8) / 1.5)
    stroke_line(ctx, [a, (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)], 5,
                "#d62612", dash=[10, 8])
    if f > 0.5:
        label(ctx, "120 км", (a[0] + b[0]) / 2 + 40, (a[1] + b[1]) / 2 - 45, 24, "#ffd166")
    # on the right: the car drives up to the mountain town
    mountains(ctx, [(760, 260, 200), (1000, 320, 240), (1220, 260, 200)], 520, "#52b788",
              snow=False)
    hills(ctx, 520, "#74c69d", 8)
    for i, x in enumerate((900, 1000, 1100)):
        house(ctx, x, 530, 0.6, roof=["#c8553d", "#b5332e", "#d1603d"][i])
    x = 600 + ease(t / (d * 0.8)) * 260
    car(ctx, x, 575, 0.75)
    label(ctx, "Стара планина", 1000, 160, 26, scale=pop(t, 1.5))


def s_height(ctx, t, d):
    valley(ctx, t, river=False)
    town(ctx, 540, t)
    # altitude marker
    stroke_line(ctx, [(170, 540), (170, 300)], 6)
    poly(ctx, [(170, 290), (155, 318), (185, 318)], INK, 0)
    sc = pop(t, 0.6)
    label(ctx, "418 м", 260, 330, 34, "#ffd166", scale=sc)
    label(ctx, "надморска височина", 260, 390, 22, scale=sc)
    # flags on the peaks
    for i, (x, h, _) in enumerate(PEAKS):
        if t > 1.2 + i * 0.3:
            stroke_line(ctx, [(x, 480 - h), (x, 480 - h - 50)], 4)
            poly(ctx, [(x, 480 - h - 50), (x + 32, 480 - h - 40), (x, 480 - h - 30)],
                 "#ef476f", 3)


def basket(ctx, hx, hy):
    rrect(ctx, hx - 24, hy, 48, 30, 8, "#c08552", 3)
    for i, c in enumerate(("#e63946", "#9d4edd", "#ffb703")):
        circle(ctx, hx - 12 + i * 12, hy + 2, 7, c, 2)


def mushroom(ctx, x, y, s=1.0):
    rrect(ctx, x - 8 * s, y - 26 * s, 16 * s, 26 * s, 4, "#fff1e6", 3)
    ctx.new_path()
    ctx.arc(x, y - 24 * s, 24 * s, math.pi, 2 * math.pi)
    ctx.close_path()
    paint(ctx, "#bc4749", 3)
    circle(ctx, x - 8 * s, y - 34 * s, 4 * s, "#ffffff", 0)
    circle(ctx, x + 9 * s, y - 30 * s, 3 * s, "#ffffff", 0)


def s_activities(ctx, t, d):
    valley(ctx, t, river=False)
    # hiker with a stick
    def stick(c, hx, hy):
        stroke_line(c, [(hx, hy - 40), (hx + 10, hy + 60)], 6, "#8a5a33")
    x = 120 + ease(t / d) * 140
    person(ctx, x, 570, 0.9, t, shirt="#e76f51", hat="cap", walk=True, hold=stick)
    label(ctx, "разходка", 190, 300, 22, scale=pop(t, 0.2))
    # picker with a basket among mushrooms and herbs
    person(ctx, 470, 570, 0.9, t, shirt="#9d4edd", hair="#8b4513", hair_style="long",
           hold=basket, blink_seed=2)
    for i, mx in enumerate((540, 590, 380)):
        mushroom(ctx, mx, 575 - (i % 2) * 10, 1.0 * pop(t, 0.6 + i * 0.3))
    label(ctx, "билки, гъби, плодове", 480, 300, 22, scale=pop(t, 0.8))
    # climber on a rock
    poly(ctx, [(780, 640), (840, 330), (960, 300), (1010, 640)], "#adb5bd")
    climb = ease(t / (d * 0.8))
    stroke_line(ctx, [(900, 300), (900, 560 - climb * 180)], 3, "#e63946")
    person(ctx, 880, 600 - climb * 180, 0.7, t, shirt="#118ab2", hat="cap", wave=0.8,
           blink_seed=4)
    label(ctx, "алпинизъм", 900, 260, 22, scale=pop(t, 1.4))
    # a deer for the hunters
    ctx.save()
    ctx.translate(1150, 560)
    ellipse(ctx, 0, -60, 55, 28, "#bc6c25")
    for lx in (-35, -15, 20, 40):
        stroke_line(ctx, [(lx, -40), (lx, 0)], 7, "#bc6c25")
    circle(ctx, 55, -100, 20, "#bc6c25")
    stroke_line(ctx, [(50, -118), (40, -150), (28, -160)], 4, "#8a5a33")
    stroke_line(ctx, [(62, -118), (72, -150), (86, -160)], 4, "#8a5a33")
    circle(ctx, 62, -104, 3, INK, 0)
    ctx.restore()
    label(ctx, "лов", 1150, 380, 22, scale=pop(t, 2.0))


def fish(ctx, x, y, s=1.0, color="#ffb703", flip=1):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s * flip, s)
    poly(ctx, [(-40, 0), (-62, -18), (-62, 18)], color, 3)
    ellipse(ctx, 0, 0, 42, 22, color, 3)
    circle(ctx, 22, -5, 4, INK, 0)
    ctx.restore()


def s_river(ctx, t, d):
    valley(ctx, t)
    label(ctx, "река Вит", 160, 460, 30, "#bde0fe", scale=pop(t, 0.3))
    # fish jumping
    for i in range(3):
        ph = (t * 0.8 + i * 0.33) % 1
        x = 280 + i * 280 + ph * 120
        y = 570 - math.sin(ph * math.pi) * 120
        if ph < 0.95:
            fish(ctx, x, y, 0.7, ["#ffb703", "#f78c6b", "#90be6d"][i])
    # the fisherman on the bank
    def rod(c, hx, hy):
        stroke_line(c, [(hx, hy), (hx + 200, hy - 140)], 5, "#8a5a33")
        bobber = 30 * math.sin(t * 2)
        stroke_line(c, [(hx + 200, hy - 140), (hx + 220, 560 + bobber * 0.2)], 2)
        circle(c, hx + 220, 560 + bobber * 0.2, 8, "#e63946", 2)
    person(ctx, 900, 520, 0.9, t, shirt="#2a9d8f", hat="cap", hold=rod, wave=0.25,
           mustache=True, hair="#555555", facing=1)
    if t > d * 0.6:
        fish(ctx, 1120, 440 + bob(t, 3, 8), 0.8, "#ffb703")
        sparkles(ctx, 1120, 440, t, 60, 6)


def lungs(ctx, x, y, s, t):
    br = 1 + 0.08 * math.sin(t * 3)
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s * br, s * br)
    stroke_line(ctx, [(0, -70), (0, -20), (-20, 0)], 8, "#e5989b")
    stroke_line(ctx, [(0, -20), (20, 0)], 8, "#e5989b")
    for k in (-1, 1):
        ctx.new_path()
        ctx.move_to(k * 12, -40)
        ctx.curve_to(k * 70, -70, k * 80, 40, k * 30, 60)
        ctx.curve_to(k * 10, 40, k * 12, 0, k * 12, -40)
        paint(ctx, "#ffadad")
    ctx.restore()


def s_climate(ctx, t, d):
    # left half winter, right half summer
    ctx.save()
    ctx.rectangle(0, 0, W / 2, H)
    ctx.clip()
    sky(ctx, "#bde0fe", "#edf6f9")
    mountains(ctx, PEAKS, 480, "#8ecae6")
    hills(ctx, 480, "#f8f9fa", 10)
    snow(ctx, t, 40)
    person(ctx, 330, 600, 1.0, t, shirt="#e63946", hat="cap", blink_seed=1, wave=0.5)
    label(ctx, "Зимата е мека", 320, 90, 30, scale=pop(t, 0.3))
    ctx.restore()
    ctx.save()
    ctx.rectangle(W / 2, 0, W / 2, H)
    ctx.clip()
    sky(ctx)
    sun(ctx, 1150, 120, t, 40)
    mountains(ctx, PEAKS, 480, "#52b788", snow=False)
    hills(ctx, 480, "#74c69d", 10)
    tree(ctx, 1150, 600, 1.2, t)
    person(ctx, 960, 600, 1.0, t, shirt="#ffd166", hair_style="long", hair="#8b4513",
           blink_seed=2)
    label(ctx, "лятото – прохладно", 960, 90, 30, scale=pop(t, 1.0))
    ctx.restore()
    stroke_line(ctx, [(W / 2, 0), (W / 2, H)], 6)
    sc = pop(t, 2.0)
    if sc:
        circle(ctx, 640, 300, 90 * sc, "#ffffff")
        lungs(ctx, 640, 305, 0.9 * sc, t)


def flowers(ctx, x, y, n, t, seed=0):
    cols = ["#ef476f", "#ffd166", "#ffffff", "#9d4edd", "#f78c6b"]
    for i in range(n):
        fx = x + (i * 37 + seed * 13) % 120 - 60
        fy = y + (i * 23) % 20
        stroke_line(ctx, [(fx, fy + 18), (fx, fy)], 3, "#2d6a4f")
        circle(ctx, fx, fy, 7 + math.sin(t * 3 + i) * 1, cols[(i + seed) % len(cols)], 2)


def s_ribaritsa(ctx, t, d):
    valley(ctx, t, river=False)
    # compass rose: south-east
    cx, cy = 150, 170
    circle(ctx, cx, cy, 80, "#ffffff")
    for a, lab in ((0, "С"), (90, "И"), (180, "Ю"), (270, "З")):
        r = math.radians(a)
        text(ctx, lab, cx + math.sin(r) * 58, cy - math.cos(r) * 58 + 9, 24, INK)
    ang = math.radians(135) * ease((t - 0.3) / 1.0)
    stroke_line(ctx, [(cx, cy), (cx + math.sin(ang) * 48, cy - math.cos(ang) * 48)], 7, "#d62612")
    circle(ctx, cx, cy, 8, INK, 0)
    label(ctx, "12 км ЮИ", cx, 290, 24, "#ffd166", scale=pop(t, 1.3))
    label(ctx, "Рибарица", 760, 90, 44, "#ffd166", scale=pop(t, 0.5))
    # hotel + little villas among flowers
    rrect(ctx, 380, 300, 220, 230, 10, "#fff1e6")
    poly(ctx, [(360, 300), (490, 230), (620, 300)], "#8a5a33")
    text(ctx, "ХОТЕЛ", 490, 345, 30, "#bc4749")
    for r in range(2):
        for c in range(3):
            rrect(ctx, 405 + c * 65, 370 + r * 65, 45, 45, 5, "#bde0fe", 3)
    for i, x in enumerate((730, 880, 1030, 1170)):
        house(ctx, x, 540 + (i % 2) * 6, 0.65, wall=["#fff1e6", "#ffe5b4"][i % 2],
              roof=["#8a5a33", "#b5332e"][i % 2])
    for i in range(6):
        flowers(ctx, 330 + i * 160, 600, 6, t, i)
    label(ctx, "тишина и спокойствие", 1000, 210, 24, scale=pop(t, 2.0))


def s_cheese(ctx, t, d):
    sky(ctx, "#ffe8d6", "#fff1e6")
    rrect(ctx, 0, 520, W, 220, 0, "#ddb892", 0)
    # barrel of brine with white cheese
    rrect(ctx, 140, 280, 280, 250, 30, "#a0522d")
    for y in (330, 470):
        stroke_line(ctx, [(140, y), (420, y)], 6, "#5c3d2e")
    ellipse(ctx, 280, 282, 140, 34, "#d0f4ff")
    for i in range(3):
        rrect(ctx, 200 + i * 60, 262 - (i % 2) * 6 + bob(t, 1, 3, i), 50, 36, 6, "#ffffff", 3)
    label(ctx, "саламурено сирене", 280, 200, 26, scale=pop(t, 0.3))
    # copper still for plum rakia, with fire and drops
    rrect(ctx, 740, 470, 200, 50, 10, "#5c3d2e")
    for i in range(5):
        fh = 30 + 12 * math.sin(t * 10 + i * 2)
        poly(ctx, [(760 + i * 38, 470), (775 + i * 38, 470 - fh), (790 + i * 38, 470)],
             "#ff7b00", 2)
    ellipse(ctx, 840, 380, 120, 90, "#d68c45")
    rrect(ctx, 815, 260, 50, 60, 10, "#d68c45")
    stroke_line(ctx, [(840, 262), (1040, 262), (1100, 380)], 10, "#b87333")
    rrect(ctx, 1060, 420, 90, 100, 12, "#e9f5db")
    drop_y = 390 + (t * 80) % 40
    ellipse(ctx, 1100, drop_y, 6, 9, "#bde0fe", 2)
    for i, x in enumerate((640, 680, 600)):
        circle(ctx, x, 500 - (i % 2) * 14, 18, "#6a4c93")
    label(ctx, "сливова ракия", 920, 130, 26, scale=pop(t, 1.2))
    for i in range(3):
        y = 245 - ((t * 30 + i * 30) % 60)
        cloud(ctx, 860 + i * 25, y, 0.3, "#ffffff")


def s_crafts(ctx, t, d):
    sky(ctx, "#f1faee", "#ffe5d9")
    rrect(ctx, 0, 520, W, 220, 0, "#ddb892", 0)
    # a loom: the colourful rug grows row by row
    rrect(ctx, 120, 160, 30, 380, 6, "#8a5a33")
    rrect(ctx, 520, 160, 30, 380, 6, "#8a5a33")
    rrect(ctx, 110, 150, 450, 30, 6, "#8a5a33")
    rows = int(ease(t / (d * 0.8)) * 14)
    cols = ["#d62612", "#00966e", "#ffd166", "#1d3557", "#ffffff", "#e76f51"]
    for r in range(14):
        y = 500 - r * 22
        if r < rows:
            rrect(ctx, 170, y - 22, 330, 22, 0, cols[r % len(cols)], 2)
            for k in range(5):
                poly(ctx, [(200 + k * 64, y - 22), (222 + k * 64, y - 11), (200 + k * 64, y)],
                     cols[(r + 2) % len(cols)], 0)
        else:
            for k in range(12):
                stroke_line(ctx, [(178 + k * 28, y - 22), (178 + k * 28, y)], 2, "#adb5bd")
    label(ctx, "пъстри черги", 335, 110, 26, scale=pop(t, 0.3))
    # jars of forest-fruit jam
    for i, (col, lab) in enumerate((("#9d0208", "малини"), ("#3a0ca3", "боровинки"),
                                    ("#d00000", "ягоди"))):
        x = 760 + i * 170
        sc = pop(t, 0.8 + i * 0.5)
        if sc:
            ctx.save()
            ctx.translate(x, 520)
            ctx.scale(sc, sc)
            rrect(ctx, -60, -170, 120, 170, 22, col)
            rrect(ctx, -66, -196, 132, 34, 8, "#f4f1de")
            stroke_line(ctx, [(-66, -196), (66, -162)], 3, "#e63946")
            rrect(ctx, -52, -110, 104, 50, 8, "#fffbe8", 3)
            text(ctx, lab, 0, -79, 15, INK)
            circle(ctx, -30, -140, 8, "#ffffff", 0)
            ctx.restore()
    label(ctx, "сладко от горски плодове", 930, 200, 26, scale=pop(t, 1.8))


def s_why(ctx, t, d):
    valley(ctx, t)
    town(ctx, 530, t, 0.7)
    for i, (icon, lab) in enumerate((("🌲", "природа"), ("☀", "климат"), ("🏛", "история"))):
        sc = pop(t, 0.4 + i * 0.6)
        if not sc:
            continue
        x = 320 + i * 320
        ctx.save()
        ctx.translate(x, 210)
        ctx.scale(sc, sc)
        circle(ctx, 0, 0, 80, ["#b7e4c7", "#ffe066", "#e9c46a"][i])
        if i == 0:
            tree(ctx, 0, 50, 0.7, t, "#2d6a4f", kind="pine")
        elif i == 1:
            sun(ctx, 0, 0, t, 32, face=False)
        else:
            poly(ctx, [(-50, -15), (0, -50), (50, -15)], "#c8553d", 3)
            for k in range(4):
                rrect(ctx, -42 + k * 26, -12, 14, 50, 3, "#fff1e6", 3)
            rrect(ctx, -55, 38, 110, 12, 3, "#fff1e6", 3)
        ctx.restore()
        label(ctx, lab, x, 330, 26, scale=sc)
    # tourists with a camera
    def camera(c, hx, hy):
        rrect(c, hx - 22, hy - 16, 44, 30, 6, "#343a40", 3)
        circle(c, hx, hy - 1, 9, "#bde0fe", 3)
    flash = int(t * 2) % 3 == 0
    person(ctx, 1110, 640, 0.8, t, shirt="#ef476f", hold=camera, wave=0.5, hat="cap",
           blink_seed=3)
    if flash:
        sparkles(ctx, 1080, 470, t, 30, 6, "#ffffff")


def s_greenest(ctx, t, d):
    valley(ctx, t, river=False, green="#52b788")
    confetti(ctx, t, 30)
    town(ctx, 560, t, 0.75)
    for i in range(8):
        g = ease((t - 0.3 - i * 0.15) / 0.8)
        if g > 0:
            tree(ctx, 80 + i * 160, 600, 0.9 * g, t, ["#2d6a4f", "#40916c"][i % 2],
                 kind="round" if i % 2 else "pine")
    sc = pop(t, 1.0)
    if sc:
        ctx.save()
        ctx.translate(640, 150)
        ctx.scale(sc, sc)
        rrect(ctx, -380, -55, 760, 110, 26, "#2d6a4f")
        text(ctx, "Най-зеленият град", 0, -3, 44, "#ffffff")
        text(ctx, "на България", 0, 38, 30, "#b7e4c7")
        ctx.restore()


def s_end(ctx, t, d):
    valley(ctx, t)
    label(ctx, "Край", 640, 220, 64, "#ffd166", scale=pop(t, 0.2))
    label(ctx, "Сега решете задачи 1–5 от Вариант 3", 640, 360, 30, scale=pop(t, 0.8))


def s_horo(ctx, t, d):
    """Locals in red and white dance a horo on the village square."""
    valley(ctx, t, river=False)
    town(ctx, 470, t, 0.6)
    n = 7
    for i in range(n):
        step = math.sin(t * 6 + i * 0.6)
        x = 200 + i * 145 + math.sin(t * 1.5) * 30
        person(ctx, x, 575 - abs(step) * 10, 0.85, t + i * 0.2,
               shirt="#ffffff" if i % 2 else "#d62612", pants="#1d1d24",
               hair=["#3b2a1a", "#111", "#8b4513"][i % 3],
               hair_style="long" if i % 2 else "short", walk=True, blink_seed=i)
        if i < n - 1:
            stroke_line(ctx, [(x + 40, 470 - abs(step) * 10), (x + 105, 470)], 9, "#f2c49b")
    label(ctx, "бит и традиции", 640, 230, 32, "#ffd166", scale=pop(t, 0.5))


SCENES = [
    # Captions are the exam's reading text, sentence by sentence.
    Scene("Вариант 3. Тетевен – най-зеленият град.",
          title_card(TITLE, "Образец на тест – Вариант 3", ("#95d5b2", "#48cae4"))),
    Scene("Тетевен е малък живописен град в България, разположен само на 120 км от София "
          "в полите на Централна Стара планина", s_arrive),
    Scene("на 418 м надморска височина. Заобиколен отвсякъде с красиви върхове, той е "
          "приятна среда за туризъм и отдих –", s_height),
    Scene("пешеходна разходка, ловуване, бране на диви плодове, билки, гъби, алпинизъм.",
          s_activities),
    Scene("През града минава река Вит, което го прави привлекателен център за риболов.",
          s_river),
    Scene("Зимата тук е мека, а лятото – прохладно. Климатът е особено подходящ за хора "
          "с белодробни заболявания.", s_climate),
    Scene("На 12 км югоизточно от Тетевен се намира живописният планински курорт Рибарица.",
          s_ribaritsa),
    Scene("Множество хотели, малки вилички и къщи, потънали в зеленина и цветя, предлагат "
          "на гостите на този край не само тишина и спокойствие,", s_ribaritsa),
    Scene("но и възможност да се потопят в автентичната и неповторима атмосфера, бит и "
          "традиции на българите.", s_horo),
    Scene("Тук можете да видите как се приготвя прочутото балканско саламурено сирене, "
          "как се вари сливова ракия", s_cheese),
    Scene("или как се тъкат пъстри черги и се правят най-вкусните сладка от горски плодове.",
          s_crafts),
    Scene("Заради уникалното съчетание на прекрасна природна среда, благоприятни климатични "
          "условия и богато културно-историческо наследство Тетевен е привлекателна "
          "туристическа дестинация,", s_why),
    Scene("а от няколко години е обявен за най-зеления град на България.", s_greenest),
    Scene("Край. Сега решете задачи 1–5 от Вариант 3.", s_end,
          narration="Край. Сега решете задачи от едно до пет от Вариант 3."),
]
