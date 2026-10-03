"""Вариант 2: Васил Левски (1837–1873)."""

import math

from cartoon import (BGMap, H, INK, Scene, W, bg_flag, bob, circle, cloud, confetti,
                     drifting_clouds, ease, ellipse, hills, house, label, mountains, paint,
                     person, poly, pop, rgb, rrect, sky, snow, sparkles, stroke_line, sun,
                     text, title_card, tree)

TITLE = "Васил Левски – Апостола на свободата"
VOICE = "bg-BG-BorislavNeural"

LEVSKI = dict(shirt="#f1faee", pants="#3d405b", hair="#c9a227", skin="#f2c49b",
              mustache=True, hat="kalpak")
NIGHT = ("#1d2a5a", "#43507f")


def levski(ctx, x, y, s, t, **kw):
    args = dict(LEVSKI)
    args.update(kw)
    person(ctx, x, y, s, t, **args)


def lion(ctx, x, y, s=1.0, t=0.0, color="#f4a261"):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    for i in range(14):
        a = i * 2 * math.pi / 14 + math.sin(t * 2) * 0.05
        circle(ctx, math.cos(a) * 52, math.sin(a) * 52, 26, "#c8553d", 3)
    circle(ctx, 0, 0, 52, "#c8553d", 0)
    circle(ctx, 0, 0, 44, color)
    circle(ctx, -16, -8, 5, INK, 0)
    circle(ctx, 16, -8, 5, INK, 0)
    poly(ctx, [(-8, 6), (8, 6), (0, 15)], INK, 0)
    ctx.new_path()
    ctx.arc(-7, 18, 7, 0, math.pi)
    ctx.arc(7, 18, 7, 0, math.pi)
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(3)
    ctx.stroke()
    ctx.restore()


def balkan(ctx, t):
    sky(ctx)
    sun(ctx, 1100, 110, t)
    drifting_clouds(ctx, t, seed=4)
    mountains(ctx, [(200, 260, 260), (520, 330, 300), (880, 280, 280), (1180, 240, 240)],
              470, "#7d9cc0")
    hills(ctx, 470, "#86c77a", 18)


def s_birth(ctx, t, d):
    balkan(ctx, t)
    label(ctx, "Карлово", 640, 80, 44, "#ffd166", scale=pop(t, 0.3))
    for i, (x, sc) in enumerate(((180, 0.9), (330, 1.1), (950, 1.0), (1110, 0.85))):
        house(ctx, x, 520, sc, roof=["#c8553d", "#b5332e", "#d1603d", "#a8442b"][i])
    tree(ctx, 470, 540, 0.9, t)
    tree(ctx, 820, 540, 0.8, t)
    # a baby in a cradle, rocking
    ctx.save()
    ctx.translate(640, 470)
    ctx.rotate(math.sin(t * 2.5) * 0.12)
    ctx.new_path()
    ctx.arc(0, 0, 80, 0, math.pi)
    ctx.close_path()
    paint(ctx, "#a0522d")
    ellipse(ctx, 0, -5, 55, 22, "#f1faee")
    circle(ctx, -38, -18, 22, "#f2c49b")
    circle(ctx, -44, -20, 3, INK, 0)
    circle(ctx, -32, -20, 3, INK, 0)
    ctx.restore()
    sc = pop(t, 1.0)
    if sc:
        ctx.save()
        ctx.translate(640, 270)
        ctx.scale(sc, sc)
        circle(ctx, 0, 0, 80, "#ffd166")
        text(ctx, "1837", 0, 14, 44, INK)
        ctx.restore()


def monastery(ctx, x, y, s=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -150, -170, 300, 170, 6, "#f1e3c8")
    for i in range(4):
        ctx.new_path()
        ctx.arc(-105 + i * 70, -60, 22, math.pi, 2 * math.pi)
        ctx.line_to(-83 + i * 70, 0)
        ctx.line_to(-127 + i * 70, 0)
        ctx.close_path()
        paint(ctx, "#8a5a33", 3)
    poly(ctx, [(-170, -170), (0, -240), (170, -170)], "#b5332e")
    rrect(ctx, -30, -330, 60, 100, 4, "#f1e3c8")
    ctx.new_path()
    ctx.arc(0, -330, 30, math.pi, 2 * math.pi)
    paint(ctx, "#5c7c99")
    stroke_line(ctx, [(0, -360), (0, -400)], 5)
    stroke_line(ctx, [(-14, -386), (14, -386)], 5)
    ctx.restore()


def s_monk(ctx, t, d):
    balkan(ctx, t)
    monastery(ctx, 920, 520, 1.0)
    # the uncle leads the boy to the monastery
    walk = ease(t / 3.0)
    x = 250 + walk * 300
    person(ctx, x, 560, 1.15, t, shirt="#6d597a", hair="#555555", mustache=True,
           walk=walk < 1, talk=t > 3.0, blink_seed=2)
    if t < 3.5:
        person(ctx, x + 80, 560, 0.8, t, shirt="#e9c46a", hair="#c9a227", walk=walk < 1,
               mood="sad", blink_seed=1)
    else:
        person(ctx, x + 90, 560, 0.85, t, robe="#1d1d24", hat="monk", hair="#c9a227",
               blink_seed=1)
        label(ctx, "Игнатий", x + 120, 250, 30, scale=pop(t, 3.5))
    label(ctx, "вуйчо", x - 40, 320, 26, scale=pop(t, 0.6))


def s_choice(ctx, t, d):
    balkan(ctx, t)
    # the black robe drops; the young man stands with the flag
    off = ease((t - 1.2) / 1.0)
    x = 600
    if off < 1:
        ctx.push_group()
        person(ctx, x, 560, 1.3, t, robe="#1d1d24", hat="monk", hair="#c9a227")
        ctx.pop_group_to_source()
        ctx.paint_with_alpha(1 - off)
    if off > 0:
        ctx.push_group()
        levski(ctx, x, 560, 1.3, t, hat=None, wave=0.6)
        ctx.pop_group_to_source()
        ctx.paint_with_alpha(off)
        poly(ctx, [(x - 220, 560), (x - 120, 540), (x - 60, 560)], "#1d1d24", 3)  # robe on the ground
    if off > 0.6:
        bg_flag(ctx, x + 140, 210, 1.2, t)
        heart_s = 1 + 0.1 * math.sin(t * 8)
        ctx.save()
        ctx.translate(x - 160, 230)
        ctx.scale(heart_s, heart_s)
        ctx.new_path()
        ctx.move_to(0, 30)
        ctx.curve_to(-60, -10, -30, -60, 0, -28)
        ctx.curve_to(30, -60, 60, -10, 0, 30)
        paint(ctx, "#e63946")
        ctx.restore()
        label(ctx, "Отечеството", x - 160, 330, 26)


def s_serbia(ctx, t, d):
    balkan(ctx, t)
    # a road going right, signpost to Serbia
    poly(ctx, [(0, 600), (W, 500), (W, 560), (0, 700)], "#d4a373", 0)
    stroke_line(ctx, [(1050, 520), (1050, 330)], 8, "#8a5a33")
    rrect(ctx, 960, 330, 200, 54, 8, "#ffd166")
    text(ctx, "Сърбия →", 1060, 368, 28, INK)
    label(ctx, "1862", 160, 80, 40, "#ffd166", scale=pop(t, 0.3))
    walk = ease(t / (d * 0.55))
    x = 150 + walk * 600
    levski(ctx, x, 620 - walk * 80, 1.0, t, hat=None, walk=walk < 1)
    if walk >= 1:
        # the lion appears: Левски comes from „лъв"
        lion(ctx, x + 10, 230 + bob(t, 1, 6), max(pop(t, d * 0.55, 0.6), 1e-3) * 1.1, t)
        label(ctx, "Левски = лъв", x + 10, 120, 32, "#ffd166", scale=pop(t, d * 0.55 + 0.4))


def lion_flag(ctx, x, y, s, t):
    """A green standard with a golden lion; (x, y) is the top of the pole."""
    stroke_line(ctx, [(x, y), (x, y + 260 * s)], 7 * s, "#8a5a33")
    ctx.new_path()
    ctx.move_to(x, y)
    for k in range(11):
        ctx.line_to(x + 150 * s * k / 10, y + math.sin(k / 3 + t * 5) * 6 * s * k / 10)
    for k in range(10, -1, -1):
        ctx.line_to(x + 150 * s * k / 10, y + 100 * s + math.sin(k / 3 + t * 5) * 6 * s * k / 10)
    ctx.close_path()
    paint(ctx, "#2d6a4f")
    lion(ctx, x + 75 * s, y + 50 * s, 0.45 * s, t, "#ffd166")


def s_flag(ctx, t, d):
    sky(ctx, "#9bd0ee", "#e8f6ff")
    mountains(ctx, [(300, 260, 300), (900, 300, 320)], 470, "#7d9cc0")
    hills(ctx, 470, "#4f9d69", 20)
    for i, x in enumerate((90, 200, 1080, 1190)):
        tree(ctx, x, 560, 1.1, t, "#2d6a4f", kind="pine")
    label(ctx, "1867", 640, 70, 40, "#ffd166", scale=pop(t, 0.3))
    # the cheta marches; Levski in front carries the standard
    march = t * 30
    for i in range(4):
        person(ctx, 460 + i * 110 + march * 0.2, 580, 0.85, t + i * 0.3,
               shirt=["#bc6c25", "#606c38", "#8d6e63", "#6d597a"][i], hat="kalpak",
               mustache=i % 2 == 0, hair="#3b2a1a", walk=True, blink_seed=i)

    def hold(c, hx, hy):
        lion_flag(c, hx - 4, hy - 220, 0.9, t)
    levski(ctx, 330 + march * 0.2, 580, 1.05, t, walk=True, wave=0.55, hold=hold)
    label(ctx, "знаменосец", 330 + march * 0.2, 150, 26, scale=pop(t, 1.0))


def s_uprising(ctx, t, d):
    balkan(ctx, t)
    # a crowd that raises its hands together
    n = 9
    for i in range(n):
        up = ease((t - 0.8 - i * 0.12) / 0.6)
        person(ctx, 120 + i * 130, 590 - (i % 2) * 20, 0.8, t + i,
               shirt=["#bc6c25", "#2a9d8f", "#e76f51", "#457b9d", "#e9c46a"][i % 5],
               hair=["#3b2a1a", "#111", "#c9a227", "#8b4513"][i % 4],
               hair_style="long" if i % 3 == 1 else "short", wave=up, blink_seed=i)
    # thought bubble
    sc = pop(t, 1.8)
    if sc:
        ctx.save()
        ctx.translate(640, 170)
        ctx.scale(sc, sc)
        ellipse(ctx, 0, 0, 300, 90, "#ffffff")
        text(ctx, "Свобода!", 0, 18, 56, "#d62612")
        ctx.restore()


TOWNS = ["Плевен", "Ловеч", "Търново", "Пловдив"]


def s_journey(ctx, t, d):
    sky(ctx, "#f7ede2", "#f5cac3")
    m = BGMap(150, 60, 900)
    m.draw(ctx, "#cce3a6")
    label(ctx, "1869 – 1871", 1130, 520, 30, "#ffd166", scale=pop(t, 0.3))
    pts = [m.city(c) for c in TOWNS]
    prog = ease((t - 0.5) / (d * 0.7)) * (len(pts) - 1)
    k = int(prog)
    path = pts[:k + 1]
    if k < len(pts) - 1:
        f = prog - k
        a, b = pts[k], pts[k + 1]
        path = path + [(a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)]
    if len(path) > 1:
        stroke_line(ctx, path, 6, "#d62612", dash=[14, 10])
    for i, c in enumerate(TOWNS):
        m.dot(ctx, c, pop(t, 0.5 + i * (d * 0.7) / (len(pts) - 1), 0.4), size=24,
              above=c not in ("Пловдив",))
    # Levski's head travels along the path
    hx, hy = path[-1]
    circle(ctx, hx, hy - 30 + bob(t, 3, 4), 26, "#f2c49b")
    rrect(ctx, hx - 22, hy - 76 + bob(t, 3, 4), 44, 30, 8, "#2b2522")


def s_network(ctx, t, d):
    sky(ctx, *NIGHT)
    for i in range(40):
        circle(ctx, (i * 197) % W, (i * 89) % 400, 2 + (i % 3), "#fff4c2", 0)
    m = BGMap(150, 60, 900)
    m.draw(ctx, "#52796f")
    extra = [(23.6, 43.3), (24.2, 42.5), (25.2, 42.6), (25.9, 43.5), (26.6, 42.7),
             (23.9, 43.0), (25.1, 43.3), (26.2, 43.1), (24.5, 43.6), (27.2, 43.0)]
    nodes = [m.city(c) for c in TOWNS] + [m.pt(*p) for p in extra]
    grow = ease((t - 0.3) / (d * 0.6))
    for i, a in enumerate(nodes):
        for j, b in enumerate(nodes):
            if i < j and math.dist(a, b) < 230:
                f = grow
                stroke_line(ctx, [a, (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)],
                            3, "#ffd166")
    for i, (x, y) in enumerate(nodes):
        glow = 9 + 3 * math.sin(t * 5 + i)
        circle(ctx, x, y, glow * pop(t, 0.2 + i * 0.08), "#ffd166", 3)
    label(ctx, "тайни комитети", 640, 640, 30, "#ffd166", scale=pop(t, 1.0))


def s_republic(ctx, t, d):
    balkan(ctx, t)
    confetti(ctx, t, 25)
    looks = [("#f2c49b", "#3b2a1a", "#e76f51", None), ("#8d5524", "#111", "#2a9d8f", None),
             ("#f2c49b", "#c9a227", "#457b9d", "fez"), ("#c68642", "#222", "#e9c46a", None),
             ("#f2c49b", "#8b4513", "#9b5de5", "kalpak"), ("#e0ac69", "#111", "#06d6a0", None)]
    n = len(looks)
    for i, (skin, hair, shirt, hat) in enumerate(looks):
        x = 190 + i * 180
        person(ctx, x, 560, 0.95, t + i, skin=skin, hair=hair, shirt=shirt, hat=hat,
               hair_style="long" if i % 2 else "short", blink_seed=i,
               wave=0.15 + 0.1 * math.sin(t * 3 + i))
        if i < n - 1:
            stroke_line(ctx, [(x + 40, 450), (x + 140, 450)], 10, "#f2c49b")
    sc = pop(t, 1.2)
    if sc:
        ctx.save()
        ctx.translate(640, 150)
        ctx.scale(sc, sc)
        rrect(ctx, -330, -55, 660, 110, 24, "#fffbe8")
        text(ctx, "Чиста и свята република", 0, -5, 38, INK)
        text(ctx, "всички хора са равни", 0, 36, 28, "#2a9d8f")
        ctx.restore()


def s_apostle(ctx, t, d):
    sky(ctx, "#ffd166", "#fff3c4")
    for i in range(16):
        a = i * math.pi / 8 + t * 0.2
        ctx.new_path()
        ctx.move_to(640, 330)
        ctx.arc(640, 330, 1000, a, a + math.pi / 16)
        ctx.close_path()
        ctx.set_source_rgba(1, 1, 1, 0.25)
        ctx.fill()
    circle(ctx, 640, 330, 210, "#fff8e1")
    levski(ctx, 640, 600, 1.9, t, wave=0.0)
    sc = pop(t, 0.8)
    if sc:
        ctx.save()
        ctx.translate(640, 80)
        ctx.scale(sc, sc)
        rrect(ctx, -330, -45, 660, 90, 24, "#d62612")
        text(ctx, "Апостол на свободата", 0, 14, 40, "#ffffff")
        ctx.restore()
    sparkles(ctx, 640, 260, t, 260, 10)


def soldier(ctx, x, y, t, walk=True):
    person(ctx, x, y, 0.9, t, shirt="#264653", pants="#1b263b", hair="#111",
           hat="fez", mustache=True, walk=walk, facing=1)


def s_capture(ctx, t, d):
    sky(ctx, *NIGHT)
    moon(ctx, 1100, 110, 46)
    rrect(ctx, 0, 470, W, 260, 0, "#e9f1f7", 0)  # snow
    for i, x in enumerate((140, 980, 1180)):
        tree(ctx, x, 520, 1.0, t, "#2d6a4f", kind="pine")
    snow(ctx, t)
    # footprints lead to the right; the soldiers follow them
    for i in range(10):
        if t > i * 0.25:
            ellipse(ctx, 260 + i * 60, 600 + (i % 2) * 18, 12, 7, "#9fb3c8", 0)
    p = ease(t / (d * 0.7))
    for i in range(3):
        soldier(ctx, 120 + i * 100 + p * 300, 600, t + i * 0.2, walk=p < 1)
        lantern = 120 + i * 100 + p * 300 + 40
        if i == 0:
            circle(ctx, lantern, 470, 16, "#ffd166", 3)
    label(ctx, "1872 · край Ловеч", 640, 90, 34, "#ffd166", scale=pop(t, 0.4))
    label(ctx, "„влизам в дирите“ = следя някого", 640, 170, 24, scale=pop(t, 1.6))


def moon(ctx, x, y, r):
    circle(ctx, x, y, r, "#fff4c2")
    circle(ctx, x + r * 0.45, y - r * 0.2, r * 0.85, rgb(NIGHT[0]), 0)


def s_death(ctx, t, d):
    sky(ctx, "#5c677d", "#979dac")
    snow(ctx, t, 90, 9)
    rrect(ctx, 0, 500, W, 260, 0, "#e9f1f7", 0)
    # a calendar page and a candle: the date, told gently
    sc = pop(t, 0.3)
    if sc:
        ctx.save()
        ctx.translate(420, 300)
        ctx.scale(sc, sc)
        rrect(ctx, -150, -170, 300, 330, 18, "#ffffff")
        rrect(ctx, -150, -170, 300, 80, 18, "#d62612")
        text(ctx, "февруари", 0, -118, 36, "#ffffff")
        text(ctx, "18", 0, 60, 130, INK)
        text(ctx, "1873", 0, 130, 40, "#6c757d")
        ctx.restore()
    # candle with a flickering flame
    rrect(ctx, 830, 330, 60, 170, 8, "#fff3c4")
    fl = 1 + 0.12 * math.sin(t * 17) + 0.08 * math.sin(t * 7)
    ctx.save()
    ctx.translate(860, 320)
    ctx.scale(fl, fl)
    ctx.new_path()
    ctx.move_to(0, -60)
    ctx.curve_to(26, -20, 22, 8, 0, 10)
    ctx.curve_to(-22, 8, -26, -20, 0, -60)
    paint(ctx, "#ffb703", 3)
    ellipse(ctx, 0, -8, 8, 14, "#fff3c4", 0)
    ctx.restore()
    label(ctx, "край София", 860, 120, 30, scale=pop(t, 1.0))


def s_legacy(ctx, t, d):
    rise = ease(t / 2.5)
    sky(ctx, "#ffafcc", "#ffe5b4")
    sun(ctx, 640, 520 - rise * 300, t, 70)
    mountains(ctx, [(200, 260, 260), (640, 300, 320), (1080, 260, 260)], 500, "#9d8189")
    hills(ctx, 500, "#86c77a", 15)
    for i, x in enumerate((180, 400, 880, 1100)):
        bg_flag(ctx, x, 470 - ease((t - 0.8 - i * 0.3) / 1.0) * 250, 0.9, t)
    label(ctx, "Комитетите → въстанието", 640, 70, 34, "#fffbe8", scale=pop(t, 1.5))


def s_end(ctx, t, d):
    balkan(ctx, t)
    label(ctx, "Край", 640, 220, 64, "#ffd166", scale=pop(t, 0.2))
    label(ctx, "Сега решете задачи 1–5 от Вариант 2", 640, 360, 30, scale=pop(t, 0.8))


SCENES = [
    # Captions are the exam's reading text, sentence by sentence.
    Scene("Вариант 2. Васил Левски – Апостола на свободата.",
          title_card(TITLE, "Образец на тест – Вариант 2", ("#00966e", "#d62612"))),
    Scene("Васил Левски е национален герой. Роден е в град Карлово.", s_birth),
    Scene("Останал рано сирак и по настояване на вуйчо си се замонашва под името Игнатий.",
          s_monk),
    Scene("Ала черното расо не подхождало на будния младеж и той решил да посвети живота си "
          "на Отечеството.", s_choice),
    Scene("През 1862 г. заминал за Сърбия, където се включил в Първата българска легия "
          "на Георги Раковски. Там получил името Левски.", s_serbia),
    Scene("През 1867 г. станал знаменосец в четата на Панайот Хитов.", s_flag),
    Scene("Личният му опит го убедил, че свободата може да се извоюва само чрез "
          "всеобщо въстание.", s_uprising),
    Scene("От 1869 г. до 1871 г. обиколил Плевен, Ловеч, Търново, Пловдив и много други "
          "градове и села,", s_journey),
    Scene("където създал мрежа от революционни комитети, обединени в единна Вътрешна "
          "революционна организация.", s_network),
    Scene("Неговата мечта била за чиста и свята република, в която всички да имат равни "
          "права, независимо от етническата и религиозната си принадлежност.", s_republic),
    Scene("Народът нарекъл Левски Апостол на свободата, защото проповядвал истинска народна "
          "свобода – политическа и социална, свобода на личността, словото и печата, "
          "равноправие между хората.", s_apostle),
    Scene("През 1872 г. османската власт влязла в дирите на Апостола и го заловила "
          "край Ловеч.", s_capture),
    Scene("Левски бил осъден на смърт и обесен на 18 февруари 1873 г. край София.", s_death),
    # The printed text has the typo „бъдещето въстание"; the caption fixes it.
    Scene("България загубила най-достойния си син, но неговите усилия не останали напразни – "
          "комитетската мрежа станала основа на бъдещото въстание.", s_legacy),
    Scene("Край. Сега решете задачи 1–5 от Вариант 2.", s_end,
          narration="Край. Сега решете задачи от едно до пет от Вариант 2."),
]
