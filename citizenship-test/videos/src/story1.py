"""Вариант 1: Бургас, „най-добрият град за живеене в България" 2012."""

import math

from cartoon import (BGMap, H, INK, Scene, W, bob, building, circle, cloud, confetti,
                     drifting_clouds, ease, ellipse, hills, label, moon, person, poly,
                     pop, rrect, sea, sky, sparkles, stroke_line, sun, text, title_card,
                     tree, trophy, rgb)

TITLE = "Бургас – най-добрият град за живеене"
VOICE = "bg-BG-KalinaNeural"


def skyline(ctx, base, t, lit=False):
    cols = ["#f2a65a", "#f7d08a", "#e07a5f", "#81b29a", "#f2cc8f", "#a5a5d6"]
    xs = [60, 170, 260, 390, 500, 640, 760, 880, 990, 1100]
    hs = [190, 260, 160, 300, 210, 250, 180, 280, 200, 230]
    for i, (x, h) in enumerate(zip(xs, hs)):
        building(ctx, x, base, 100, h, cols[i % len(cols)], lit)


def seaside(ctx, t):
    sky(ctx)
    sun(ctx, 1110, 110, t)
    drifting_clouds(ctx, t)
    skyline(ctx, 420, t)
    sea(ctx, 410, t)
    # a seagull
    gx = (t * 70) % (W + 200) - 100
    gy = 200 + math.sin(t * 2) * 15
    flap = math.sin(t * 10) * 10
    stroke_line(ctx, [(gx - 26, gy - flap), (gx, gy), (gx + 26, gy - flap)], 5)


def s_city(ctx, t, d):
    seaside(ctx, t)
    # a little boat
    bx = 200 + t * 25
    poly(ctx, [(bx - 60, 470), (bx + 60, 470), (bx + 40, 500), (bx - 40, 500)], "#e63946")
    stroke_line(ctx, [(bx, 470), (bx, 395)], 5)
    poly(ctx, [(bx + 3, 400), (bx + 45, 462), (bx + 3, 462)], "#ffffff")
    label(ctx, "Бургас", 640, 80, 46, "#ffd166", scale=pop(t, 0.3))
    label(ctx, "Черно море", 900, 540, 26, "#bde0fe", scale=pop(t, 0.9))


def s_winner(ctx, t, d):
    seaside(ctx, t)
    confetti(ctx, t)
    # banner between two poles
    sc = pop(t, 0.3, 0.7)
    stroke_line(ctx, [(240, 470), (240, 140)], 8, "#8a5a33")
    stroke_line(ctx, [(1040, 470), (1040, 140)], 8, "#8a5a33")
    if sc > 0:
        ctx.save()
        ctx.translate(640, 200)
        ctx.scale(sc, sc)
        rrect(ctx, -390, -60, 780, 120, 20, "#ef476f")
        text(ctx, "Най-добрият град", 0, -8, 44, "#ffffff")
        text(ctx, "за живеене – 2012", 0, 40, 38, "#ffe066")
        ctx.restore()
    for i, x in enumerate((420, 560, 720, 860)):
        person(ctx, x, 560, 0.85, t + i, shirt=["#06d6a0", "#118ab2", "#ffd166", "#f78c6b"][i],
               wave=1.0 if (t + i * 0.3) % 2 < 1.3 else 0.3, hair=["#5a3825", "#e0a050", "#222", "#8b4513"][i],
               hair_style="long" if i % 2 else "short", blink_seed=i)


def s_award(ctx, t, d):
    # a stage with curtains
    ctx.set_source_rgb(*rgb("#3a2e5c"))
    ctx.paint()
    for side in (-1, 1):
        x0 = 0 if side < 0 else W
        poly(ctx, [(x0, 0), (x0 - side * 220, 0), (x0 - side * 150, H), (x0, H)], "#b5332e")
    rrect(ctx, 120, 470, 1040, 140, 10, "#8a5a33")
    # spotlight
    ctx.new_path()
    ctx.move_to(560, 0)
    ctx.line_to(720, 0)
    ctx.line_to(980, 480)
    ctx.line_to(300, 480)
    ctx.close_path()
    ctx.set_source_rgba(1, 1, 0.8, 0.18)
    ctx.fill()
    walk_in = ease(t / 1.6)
    # the president gives, the mayor receives
    pres_x = 440
    mayor_x = 1000 - walk_in * 160
    person(ctx, pres_x, 500, 1.15, t, shirt="#2b3a67", hair="#888888", talk=1.5 < t < 3.5,
           blink_seed=1)
    give = ease((t - 1.8) / 1.0)
    person(ctx, mayor_x, 500, 1.15, t, shirt="#264653", hair="#3b2a1a", walk=walk_in < 1,
           facing=-1, wave=0.4 * give, blink_seed=2)
    tx = pres_x + 70 + give * (mayor_x - pres_x - 140) / 2
    trophy(ctx, tx + 40, 380 - give * 20, 0.55)
    label(ctx, "президентът", pres_x, 120, 26, scale=pop(t, 0.5))
    label(ctx, "кметът на Бургас", mayor_x, 120, 26, scale=pop(t, 1.0))
    if give > 0.95:
        sparkles(ctx, tx + 40, 320, t)


def radio(ctx, x, y, t):
    rrect(ctx, x - 130, y - 90, 260, 170, 24, "#e76f51")
    circle(ctx, x - 60, y, 50 + math.sin(t * 12) * 3, "#264653")
    circle(ctx, x - 60, y, 18, "#2a9d8f")
    rrect(ctx, x + 10, y - 50, 100, 40, 8, "#f4f1de")
    text(ctx, "ДАРИК", x + 60, y - 21, 22, "#e63946")
    for i in range(3):
        circle(ctx, x + 30 + i * 30, y + 40, 10, "#f4a261")
    stroke_line(ctx, [(x + 90, y - 90), (x + 140, y - 170)], 6)
    for i in range(3):
        r = 30 + i * 22 + (t * 40) % 22
        ctx.new_path()
        ctx.arc(x + 140, y - 170, r, -1.0, -0.2)
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(4)
        ctx.stroke()


def newspaper(ctx, x, y, t):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(math.sin(t * 1.5) * 0.05)
    rrect(ctx, -140, -120, 280, 240, 6, "#fbfbf2")
    text(ctx, "24 часа", 0, -70, 44, "#d62828")
    stroke_line(ctx, [(-120, -50), (120, -50)], 4)
    rrect(ctx, -120, -35, 110, 80, 4, "#a8dadc", 3)
    for i in range(6):
        stroke_line(ctx, [(10, -30 + i * 16), (120, -30 + i * 16)], 4, "#9a9a9a")
    for i in range(3):
        stroke_line(ctx, [(-120, 65 + i * 16), (120, 65 + i * 16)], 4, "#9a9a9a")
    ctx.restore()


def s_media(ctx, t, d):
    sky(ctx, "#ffe8d6", "#ffd7ba")
    rrect(ctx, 0, 470, W, 260, 0, "#cb997e", 0)
    radio(ctx, 330, 330, t)
    newspaper(ctx, 900, 320 + bob(t, 1, 6), t)
    text(ctx, "+", 615, 350, 90, "#ef476f")
    sc = pop(t, 1.5)
    if sc:
        ctx.save()
        ctx.translate(640, 105)
        ctx.scale(sc, sc)
        circle(ctx, 0, 0, 70, "#ffd166")
        text(ctx, "6", 0, 10, 62, INK)
        text(ctx, "години", 0, 48, 20, INK)
        ctx.restore()


def s_contest(ctx, t, d):
    sky(ctx, "#cdeffd", "#eaf7ff")
    m = BGMap(90, 90, 760)
    m.draw(ctx)
    # 27 dots popping up one by one (the regional cities)
    pts = [(22.9, 43.9), (23.2, 43.4), (23.55, 43.2), (23.32, 42.70), (23.1, 42.4),
           (23.10, 42.02), (24.0, 42.2), (24.75, 42.15), (24.3, 43.4), (24.72, 43.14),
           (24.62, 43.42), (25.3, 43.6), (25.63, 43.08), (25.32, 42.88), (25.63, 42.43),
           (25.9, 43.85), (26.5, 43.55), (26.95, 43.27), (26.5, 43.2), (27.47, 42.50),
           (27.91, 43.21), (27.6, 43.55), (26.3, 42.67), (26.5, 42.48), (25.4, 41.66),
           (24.7, 41.58), (25.8, 42.05)]
    shown = 0
    for i, (lo, la) in enumerate(pts):
        sc = pop(t, 0.4 + i * 0.12, 0.4)
        if sc > 0:
            shown += 1
            x, y = m.pt(lo, la)
            circle(ctx, x, y, 11 * sc, "#ef476f", 3)
    label(ctx, "%d града" % shown, 470, 70, 32, "#ffd166")
    # clipboard with 29 criteria
    cx, cy = 1050, 300
    rrect(ctx, cx - 130, cy - 170, 260, 340, 16, "#c08552")
    rrect(ctx, cx - 110, cy - 145, 220, 300, 8, "#ffffff", 3)
    rrect(ctx, cx - 40, cy - 185, 80, 36, 8, "#adb5bd", 3)
    text(ctx, "29 критерия", cx, cy - 105, 28, INK)
    for i in range(5):
        y = cy - 60 + i * 42
        rrect(ctx, cx - 90, y - 16, 28, 28, 5, "#ffffff", 3)
        if t > 1.2 + i * 0.5:
            stroke_line(ctx, [(cx - 84, y - 2), (cx - 76, y + 7), (cx - 58, y - 20)], 5, "#2a9d8f")
        stroke_line(ctx, [(cx - 45, y), (cx + 90, y)], 5, "#ced4da")


def s_second(ctx, t, d):
    seaside(ctx, t)
    trophy(ctx, 500, 470, 1.0, "2012", "#ffc93c")
    trophy(ctx, 330, 470, 0.7, None, "#e9c46a")
    sc = pop(t, 0.8)
    if sc:
        ctx.save()
        ctx.translate(820, 270)
        ctx.scale(sc, sc)
        circle(ctx, 0, 0, 95, "#ef476f")
        text(ctx, "2", 0, 20, 100, "#ffffff")
        text(ctx, "път", 0, 60, 26, "#ffffff")
        ctx.restore()
    sparkles(ctx, 500, 360, t)


def coin(ctx, x, y, r=26):
    circle(ctx, x, y, r, "#ffd166")
    text(ctx, "€", x, y + r * 0.38, r * 1.1, "#b08900")


def dog(ctx, x, y, s, t, color="#d4a373"):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    wag = math.sin(t * 14) * 0.5
    stroke_line(ctx, [(-60, -50), (-60 - 30 * math.cos(wag), -80 - 20 * math.sin(wag))], 9, color)
    for lx in (-45, -20, 25, 50):
        stroke_line(ctx, [(lx, -30), (lx, 0)], 11, color)
    ellipse(ctx, 0, -45, 65, 30, color)
    circle(ctx, 65, -80, 30, color)
    ellipse(ctx, 50, -100, 10, 22, "#8d5524")
    circle(ctx, 75, -86, 4, INK, 0)
    circle(ctx, 93, -74, 6, INK, 0)
    rrect(ctx, 30, -62, 22, 10, 4, "#e63946", 3)
    ctx.restore()


def s_points1(ctx, t, d):
    sky(ctx)
    drifting_clouds(ctx, t)
    hills(ctx, 470, "#95d5b2")
    # 1) investments: coins falling into a building
    building(ctx, 110, 480, 220, 260, "#a5a5d6")
    for i in range(5):
        y = 120 + ((t * 120 + i * 70) % 260)
        coin(ctx, 150 + i * 36, y)
    label(ctx, "инвестиции", 220, 160, 24, scale=pop(t, 0.3))
    # 2) jobs: a happy worker with a briefcase
    def briefcase(c, hx, hy):
        rrect(c, hx - 22, hy, 44, 32, 6, "#8a5a33", 3)
    sc = pop(t, 1.2)
    if sc:
        person(ctx, 630, 520, 1.1 * sc, t, shirt="#2a9d8f", hold=briefcase, blink_seed=3)
        label(ctx, "работа", 630, 160, 24, scale=sc)
    # 3) few stray dogs: a dog with a collar and an owner
    sc = pop(t, 2.4)
    if sc:
        dog(ctx, 1030, 520, 0.9 * sc, t)
        label(ctx, "кучета със стопани", 1010, 160, 24, scale=sc)
    for i, x in enumerate((220, 630, 1020)):
        if t > 0.8 + i * 1.2:
            text(ctx, "+", x + 120, 230, 60, "#2a9d8f", outline="#ffffff")


def wifi(ctx, x, y, t):
    on = int(t * 3) % 4
    for i in range(3):
        ctx.new_path()
        ctx.arc(x, y, 30 + i * 28, -math.pi * 0.75, -math.pi * 0.25)
        ctx.set_source_rgb(*(rgb("#118ab2") if i < on else rgb("#cfd8dc")))
        ctx.set_line_width(12)
        ctx.set_line_cap(1)
        ctx.stroke()
    circle(ctx, x, y, 10, "#118ab2", 3)


def s_points2(ctx, t, d):
    sky(ctx, "#ffd6a5", "#fdffb6")
    rrect(ctx, 0, 470, W, 260, 0, "#e9c46a", 0)  # pedestrian street
    for i in range(10):
        rrect(ctx, i * 140 - (t * 40) % 140, 500, 70, 20, 4, "#f4a261", 0)
    # free wifi
    wifi(ctx, 170, 300, t)
    label(ctx, "безплатен интернет", 170, 370, 22, scale=pop(t, 0.2))
    # 24h pharmacy at night
    rrect(ctx, 330, 170, 230, 300, 10, "#1d2a5a")
    moon(ctx, 400, 230, 26)
    rrect(ctx, 370, 300, 150, 150, 8, "#e0fbfc")
    rrect(ctx, 432, 320, 26, 80, 4, "#2a9d8f", 0)
    rrect(ctx, 405, 347, 80, 26, 4, "#2a9d8f", 0)
    text(ctx, "24/7", 445, 435, 26, INK)
    label(ctx, "денонощна аптека", 445, 135, 22, scale=pop(t, 0.8))
    # shop with long opening hours
    rrect(ctx, 640, 230, 230, 240, 10, "#ffb4a2")
    for i in range(6):
        poly(ctx, [(640 + i * 38, 230), (678 + i * 38, 230), (678 + i * 38, 270),
                   (640 + i * 38, 270)], "#e63946" if i % 2 else "#ffffff", 2)
    circle(ctx, 755, 350, 50, "#ffffff")
    a = t * 2
    stroke_line(ctx, [(755, 350), (755 + math.sin(a) * 35, 350 - math.cos(a) * 35)], 5)
    stroke_line(ctx, [(755, 350), (755 + math.sin(a / 12) * 22, 350 - math.cos(a / 12) * 22)], 6)
    label(ctx, "магазини", 755, 110, 22, scale=pop(t, 1.4))
    # resort: beach umbrella
    stroke_line(ctx, [(1080, 470), (1080, 250)], 7, "#8a5a33")
    ctx.new_path()
    ctx.arc(1080, 260, 110, math.pi, 2 * math.pi)
    ctx.close_path()
    from cartoon import paint
    paint(ctx, "#ef476f")
    for k in (-1, 1):
        poly(ctx, [(1080, 150), (1080 + k * 55, 260), (1080 + k * 30, 260)], "#ffffff", 0)
    label(ctx, "курорти наблизо", 1080, 110, 22, scale=pop(t, 2.0))
    # people strolling on the street
    for i in range(3):
        x = (i * 430 + t * 60) % (W + 200) - 100
        person(ctx, x, 560, 0.6, t + i, shirt=["#ffd166", "#06d6a0", "#118ab2"][i], walk=True,
               hair_style="long" if i == 1 else "short", blink_seed=i)


def smog(ctx, x, y, t, s=1.0):
    for i in range(4):
        cloud(ctx, x + i * 60 * s + math.sin(t + i) * 10, y - (t * 15 + i * 30) % 120 * s,
              0.6 * s, "#9e9e9e")


def car(ctx, x, y, s=1.0, color="#3a86ff", t=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -120, -70, 240, 55, 18, color)
    poly(ctx, [(-70, -70), (-40, -120), (50, -120), (80, -70)], color)
    poly(ctx, [(-55, -75), (-32, -110), (2, -110), (2, -75)], "#bde0fe", 3)
    poly(ctx, [(12, -75), (12, -110), (44, -110), (66, -75)], "#bde0fe", 3)
    for wx in (-70, 70):
        circle(ctx, wx, -15, 26, "#333333")
        circle(ctx, wx, -15, 10, "#bbbbbb", 3)
    ctx.restore()


def s_problems(ctx, t, d):
    sky(ctx, "#b0b8c1", "#dfe3e6")
    skyline(ctx, 470, t, lit=True)
    rrect(ctx, 0, 470, W, 260, 0, "#6c757d", 0)
    # factory with smoke
    rrect(ctx, 80, 320, 160, 150, 6, "#8d99ae")
    rrect(ctx, 180, 210, 36, 110, 4, "#6c757d")
    smog(ctx, 160, 200, t)
    label(ctx, "екология", 180, 90, 28, "#e9ecef", scale=pop(t, 0.3))
    # the thief tiptoes toward a car
    car(ctx, 900, 560, 1.0, "#ef476f")
    tx = 520 + ease((t - 1.0) / 2.5) * 200
    person(ctx, tx, 565, 0.95, t, shirt="#222222", pants="#222222", hair="#111111",
           hat="cap", mood="sneaky", walk=1.0 < t < 3.5, blink_seed=5)
    ctx.save()  # mask over the eyes
    rrect(ctx, tx - 0.95 * 30, 565 - 0.95 * 180, 0.95 * 60, 0.95 * 14, 6, "#111111", 0)
    ctx.restore()
    label(ctx, "кражби на коли", 820, 90, 28, "#e9ecef", scale=pop(t, 1.2))
    if t > 3.3 and int(t * 4) % 2:
        text(ctx, "!", 960, 400, 90, "#e63946", outline="#ffffff")


def medal(ctx, x, y, city, prize, s, color):
    if s <= 0:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    poly(ctx, [(-30, -150), (-5, -60), (5, -60), (30, -150)], "#ef476f", 3)
    circle(ctx, 0, -20, 48, color)
    text(ctx, "★", 0, -4, 46, "#ffffff")
    text(ctx, city, 0, 60, 26, INK, outline="#ffffff")
    text(ctx, prize, 0, 92, 20, "#5a189a", outline="#ffffff")
    ctx.restore()


def s_others(ctx, t, d):
    sky(ctx, "#caffbf", "#fdffb6")
    confetti(ctx, t, 30)
    items = [("София", "устойчиво развитие", "#bde0fe"),
             ("Пловдив", "„Арт град“", "#ffc6ff"),
             ("Ловеч", "„Зелен град“", "#95d5b2"),
             ("Кочериново", "„Малък зелен град“", "#b7e4c7"),
             ("Трявна", "„Красив град“", "#ffd166")]
    for i, (city, prize, col) in enumerate(items):
        x = 140 + i * 250
        medal(ctx, x, 360 + bob(t, 1, 5, i), city, prize, pop(t, 0.3 + i * 0.6), col)


def s_ranking(ctx, t, d):
    sky(ctx, "#e0fbfc", "#ffffff")
    rows = [("Бургас", 66.5), ("София", 64.5), ("Благоевград", 61.5), ("Варна", 60),
            ("Стара Загора", 59.5), ("Велико Търново", 57), ("Пловдив", 57)]
    text(ctx, "Най-добър град за живеене – точки", 640, 60, 32, INK)
    for i, (city, pts) in enumerate(rows):
        y = 100 + i * 66
        grow = ease((t - 0.3 - i * 0.25) / 1.0)
        w = (pts - 50) / 17 * 580 * grow
        text(ctx, "%d." % (i + 1), 40, y + 40, 28, INK, align="left")
        text(ctx, city, 380, y + 40, 28, INK, align="right")
        if w > 4:
            rrect(ctx, 400, y + 10, w, 44, 10, "#ffd166" if i == 0 else "#90e0ef", 3)
        if grow > 0.9:
            text(ctx, ("%.1f" % pts).replace(".0", "").replace(".", ","), 420 + w, y + 42,
                 26, INK, align="left")
    if t > 2.5:
        trophy(ctx, 1150, 260 + bob(t, 1, 6), 0.55)


def s_end(ctx, t, d):
    seaside(ctx, t)
    label(ctx, "Край", 640, 220, 64, "#ffd166", scale=pop(t, 0.2))
    label(ctx, "Сега решете задачи 1–5 от Вариант 1", 640, 360, 30, scale=pop(t, 0.8))


SCENES = [
    # Captions are the exam's reading text, sentence by sentence; the table is
    # read out at the end.
    Scene("Вариант 1. Бургас – най-добрият град за живеене.",
          title_card(TITLE, "Образец на тест – Вариант 1", ("#48cae4", "#ffd166"))),
    Scene("Бургас е „най-добрият град за живеене в България“ за 2012 г.", s_winner),
    Scene("Кметът на морския град получи приза от президента на страната.", s_award),
    Scene("Класацията се провежда за шеста поредна година и е съвместна инициатива "
          "на Дарик радио и в. „24 часа“.", s_media),
    Scene("В проучването участие взеха 27-те областни града, които бяха оценявани "
          "по 29 критерия.", s_contest),
    Scene("Бургас получава приза „Най-добър град за живеене“ за втори път.", s_second),
    Scene("От общо 29 критерия морският град получи максимален брой точки в областите: "
          "чужди инвестиции, процент на безработни граждани, бездомни кучета,", s_points1),
    Scene("безплатен безжичен интернет на обществени места, брой денонощни аптеки, "
          "хубава главна пешеходна улица, работно време на магазините, близост до курорти.",
          s_points2),
    Scene("Проблеми за Бургас обаче остават екологичното състояние на града и броят "
          "на кражби на автомобили.", s_problems),
    Scene("Тази година специални призове взеха и още пет града – София за град с устойчиво "
          "развитие, Пловдив за „Арт град“, Ловеч за „Зелен град“, Кочериново за "
          "„Малък зелен град“ и Трявна за „Красив град“.", s_others),
    Scene("Резултати от анкетата: 1. Бургас – 66,5 т., 2. София – 64,5 т., "
          "3. Благоевград – 61,5 т.", s_ranking,
          narration="Резултати от анкетата: първо място – Бургас, 66,5 точки. Второ – София, "
                    "64,5 точки. Трето – Благоевград, 61,5 точки."),
    Scene("Край. Сега решете задачи 1–5 от Вариант 1.", s_end,
          narration="Край. Сега решете задачи от едно до пет от Вариант 1."),
]
