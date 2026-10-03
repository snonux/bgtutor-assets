"""Small cartoon toolkit: Cairo drawing helpers and the video pipeline.

Each story (story1.py ... story3.py) is a list of scenes. A scene has a
Bulgarian narration line, which is also the on-screen caption, and a draw
function ``draw(ctx, t, d)`` where ``t`` is seconds into the scene and ``d``
the scene length. ``render()`` synthesises the narration with edge-tts,
sizes every scene to its audio, draws the frames and muxes an MP4.
"""

import asyncio
import math
import os
import random
import re
import subprocess
import tempfile

import cairo

W, H = 1280, 720
FPS = 24
INK = (0.17, 0.16, 0.24)
FONT = "DejaVu Sans"
CAPTION_TOP = 590  # scene art should keep important things above this line


# ---------------------------------------------------------------- basics

def rgb(hexstr):
    """'#rrggbb' -> (r, g, b) floats."""
    h = hexstr.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def ease(x):
    """Smoothstep easing clamped to 0..1."""
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def pop(t, start, length=0.5):
    """Bouncy 0..1 scale for things that pop into view at ``start``."""
    x = (t - start) / length
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    return 1 + 0.25 * math.sin(x * math.pi) - 0.25 * (1 - x) - (1 - x) ** 3 * 0.75


def bob(t, speed=2.0, amp=4.0, phase=0.0):
    return math.sin(t * speed * math.pi + phase) * amp


def paint(ctx, fill, line=4.0, ink=INK):
    """Fill the current path with ``fill`` and stroke a cartoon outline."""
    if isinstance(fill, str):
        fill = rgb(fill)
    ctx.set_source_rgb(*fill)
    if line:
        ctx.fill_preserve()
        ctx.set_source_rgb(*ink)
        ctx.set_line_width(line)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()
    else:
        ctx.fill()


def circle(ctx, x, y, r, fill, line=4.0):
    ctx.new_path()
    ctx.arc(x, y, r, 0, 2 * math.pi)
    paint(ctx, fill, line)


def ellipse(ctx, x, y, rx, ry, fill, line=4.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(rx, ry)
    ctx.new_path()
    ctx.arc(0, 0, 1, 0, 2 * math.pi)
    ctx.restore()
    paint(ctx, fill, line)


def rrect(ctx, x, y, w, h, r, fill, line=4.0):
    r = min(r, w / 2, h / 2)
    ctx.new_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    ctx.close_path()
    paint(ctx, fill, line)


def poly(ctx, pts, fill, line=4.0, closed=True):
    ctx.new_path()
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    if closed:
        ctx.close_path()
    paint(ctx, fill, line)


def stroke_line(ctx, pts, width=4.0, color=INK, dash=None):
    ctx.new_path()
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    ctx.set_source_rgb(*(rgb(color) if isinstance(color, str) else color))
    ctx.set_line_width(width)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    if dash:
        ctx.set_dash(dash)
    ctx.stroke()
    ctx.set_dash([])


def text(ctx, s, x, y, size=32, color=INK, bold=True, align="center",
         outline=None):
    """Draw one line of text; ``y`` is the baseline."""
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
    ext = ctx.text_extents(s)
    if align == "center":
        x -= ext.x_advance / 2
    elif align == "right":
        x -= ext.x_advance
    ctx.new_path()
    ctx.move_to(x, y)
    ctx.text_path(s)
    if outline:
        ctx.set_source_rgb(*(rgb(outline) if isinstance(outline, str) else outline))
        ctx.set_line_width(size / 6)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.stroke_preserve()
    ctx.set_source_rgb(*(rgb(color) if isinstance(color, str) else color))
    ctx.fill()


def wrap(ctx, s, size, max_w, bold=True):
    """Greedy word wrap using the real font metrics."""
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if ctx.text_extents(trial).x_advance <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def label(ctx, s, x, y, size=26, fill="#fffbe8", color=INK, scale=1.0):
    """A rounded sign with text, centred on (x, y)."""
    if scale <= 0:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(scale, scale)
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(size)
    w = ctx.text_extents(s).x_advance + size * 1.0
    h = size * 1.6
    rrect(ctx, -w / 2, -h / 2, w, h, h / 3, fill, 3.5)
    text(ctx, s, 0, size * 0.36, size, color)
    ctx.restore()


# ---------------------------------------------------------------- scenery

def sky(ctx, top="#7ec8f2", bottom="#d8f1ff"):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *rgb(top))
    g.add_color_stop_rgb(1, *rgb(bottom))
    ctx.set_source(g)
    ctx.paint()


def sun(ctx, x, y, t, r=48, face=True):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(t * 0.4)
    for i in range(12):
        a = i * math.pi / 6
        stroke_line(ctx, [(math.cos(a) * (r + 10), math.sin(a) * (r + 10)),
                          (math.cos(a) * (r + 28), math.sin(a) * (r + 28))],
                    6, "#ffb703")
    ctx.restore()
    circle(ctx, x, y, r, "#ffd23f")
    if face:
        circle(ctx, x - r * 0.3, y - r * 0.15, r * 0.08, INK, 0)
        circle(ctx, x + r * 0.3, y - r * 0.15, r * 0.08, INK, 0)
        ctx.new_path()
        ctx.arc(x, y + r * 0.05, r * 0.4, 0.2 * math.pi, 0.8 * math.pi)
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(4)
        ctx.stroke()


def moon(ctx, x, y, r=40):
    circle(ctx, x, y, r, "#fff4c2")
    circle(ctx, x + r * 0.45, y - r * 0.2, r * 0.85, rgb("#1d2a5a"), 0)


def cloud(ctx, x, y, s=1.0, fill="#ffffff"):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.new_path()
    for cx, cy, r in ((-50, 10, 32), (-10, -12, 42), (38, 4, 34), (70, 18, 22)):
        ctx.new_sub_path()
        ctx.arc(cx, cy, r, 0, 2 * math.pi)
    ctx.restore()
    paint(ctx, "#2b2b3a", 0)  # cheap outline: dark blob slightly larger
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.new_path()
    for cx, cy, r in ((-50, 10, 29), (-10, -12, 39), (38, 4, 31), (70, 18, 19)):
        ctx.new_sub_path()
        ctx.arc(cx, cy, r, 0, 2 * math.pi)
    ctx.restore()
    paint(ctx, fill, 0)


def drifting_clouds(ctx, t, n=3, y0=90, seed=1):
    rnd = random.Random(seed)
    for i in range(n):
        speed = rnd.uniform(10, 25)
        x = (rnd.uniform(0, W + 300) + t * speed) % (W + 300) - 150
        cloud(ctx, x, y0 + rnd.uniform(-30, 50), rnd.uniform(0.6, 1.0))


def hills(ctx, y, color="#7cc46a", amp=30, phase=0.0, line=4.0):
    ctx.new_path()
    ctx.move_to(-10, H + 10)
    for x in range(-10, W + 20, 20):
        ctx.line_to(x, y + math.sin(x / 180 + phase) * amp)
    ctx.line_to(W + 10, H + 10)
    ctx.close_path()
    paint(ctx, color, line)


def mountains(ctx, peaks, base, color="#6b8fb5", snow=True):
    """peaks: list of (x, height, half_width)."""
    for x, h, hw in peaks:
        top = base - h
        poly(ctx, [(x - hw, base), (x, top), (x + hw, base)], color)
        if snow:
            k = 0.28
            poly(ctx, [(x - hw * k, top + h * k), (x, top), (x + hw * k, top + h * k),
                       (x + hw * k * 0.4, top + h * k * 0.8), (x, top + h * k * 1.05),
                       (x - hw * k * 0.4, top + h * k * 0.8)], "#ffffff", 3)


def sea(ctx, y, t, color="#2f8fd8"):
    ctx.new_path()
    ctx.move_to(-10, H + 10)
    for x in range(-10, W + 20, 10):
        ctx.line_to(x, y + math.sin(x / 40 + t * 3) * 5)
    ctx.line_to(W + 10, H + 10)
    ctx.close_path()
    paint(ctx, color)
    for row in range(3):
        yy = y + 40 + row * 45
        for i in range(8):
            x = (i * 190 + row * 90 + t * (25 + row * 10)) % (W + 100) - 50
            ctx.new_path()
            ctx.arc(x, yy, 14, math.pi * 1.1, math.pi * 1.9)
            ctx.set_source_rgb(1, 1, 1)
            ctx.set_line_width(4)
            ctx.stroke()


def tree(ctx, x, y, s=1.0, t=0.0, color="#3fa34d", kind="round"):
    sway = math.sin(t * 2 + x) * 3 * s
    rrect(ctx, x - 8 * s, y - 50 * s, 16 * s, 50 * s, 4, "#8a5a33")
    if kind == "pine":
        for i in range(3):
            w = (60 - i * 14) * s
            yy = y - (40 + i * 32) * s
            poly(ctx, [(x - w + sway, yy), (x + sway * 1.4, yy - 50 * s), (x + w + sway, yy)], color)
    else:
        circle(ctx, x + sway, y - 85 * s, 45 * s, color)
        circle(ctx, x - 25 * s + sway, y - 70 * s, 28 * s, color, 0)


def house(ctx, x, y, s=1.0, wall="#f4d7a8", roof="#c8553d", door="#7a4b2a"):
    """Bulgarian-ish house: (x, y) is bottom centre."""
    w, h = 110 * s, 80 * s
    rrect(ctx, x - w / 2, y - h, w, h, 4, wall)
    poly(ctx, [(x - w / 2 - 15 * s, y - h), (x, y - h - 55 * s), (x + w / 2 + 15 * s, y - h)], roof)
    rrect(ctx, x - 14 * s, y - 45 * s, 28 * s, 45 * s, 4, door)
    rrect(ctx, x + 22 * s, y - 62 * s, 24 * s, 24 * s, 3, "#bfe6ff")
    rrect(ctx, x - 46 * s, y - 62 * s, 24 * s, 24 * s, 3, "#bfe6ff")


def building(ctx, x, y, w, h, color="#f2a65a", lit=False, rows=None):
    """Block building with windows; (x, y) bottom-left."""
    rrect(ctx, x, y - h, w, h, 6, color)
    rows = rows or max(1, int(h // 42))
    cols = max(1, int(w // 38))
    for r in range(rows):
        for c in range(cols):
            wx = x + 12 + c * (w - 24) / cols
            wy = y - h + 14 + r * (h - 20) / rows
            on = lit and (r * 7 + c * 3) % 4 != 0
            rrect(ctx, wx, wy, (w - 24) / cols - 10, (h - 20) / rows - 14, 3,
                  "#ffe066" if on else "#bfe6ff", 2.5)


def bg_flag(ctx, x, y, s=1.0, t=0.0, pole=True):
    """Bulgarian tricolour waving; (x, y) is the top of the pole."""
    if pole:
        stroke_line(ctx, [(x, y), (x, y + 200 * s)], 6 * s, "#8a5a33")
    fw, fh = 110 * s, 72 * s
    for i, col in enumerate(("#ffffff", "#00966e", "#d62612")):
        ctx.new_path()
        y0 = y + i * fh / 3
        ctx.move_to(x, y0)
        for k in range(0, 11):
            px = x + fw * k / 10
            ctx.line_to(px, y0 + math.sin(k / 3 + t * 5) * 5 * s * k / 10)
        for k in range(10, -1, -1):
            px = x + fw * k / 10
            ctx.line_to(px, y0 + fh / 3 + math.sin(k / 3 + t * 5) * 5 * s * k / 10)
        ctx.close_path()
        paint(ctx, col, 0)
    ctx.new_path()
    ctx.move_to(x, y)
    for k in range(0, 11):
        ctx.line_to(x + fw * k / 10, y + math.sin(k / 3 + t * 5) * 5 * s * k / 10)
    for k in range(10, -1, -1):
        ctx.line_to(x + fw * k / 10, y + fh + math.sin(k / 3 + t * 5) * 5 * s * k / 10)
    ctx.close_path()
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(3)
    ctx.stroke()


def trophy(ctx, x, y, s=1.0, label_text=None, color="#ffc93c"):
    """Cup trophy; (x, y) is the bottom centre."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -45, -30, 90, 30, 6, "#8a5a33")
    rrect(ctx, -12, -70, 24, 42, 4, color)
    ctx.new_path()
    ctx.arc(-58, -130, 26, math.pi * 0.5, math.pi * 1.5)
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(9)
    ctx.stroke()
    ctx.new_path()
    ctx.arc(58, -130, 26, -math.pi * 0.5, math.pi * 0.5)
    ctx.stroke()
    ctx.new_path()
    ctx.move_to(-60, -165)
    ctx.line_to(60, -165)
    ctx.curve_to(60, -95, 25, -70, 0, -70)
    ctx.curve_to(-25, -70, -60, -95, -60, -165)
    ctx.close_path()
    paint(ctx, color)
    circle(ctx, -28, -140, 7, "#fff5cc", 0)
    if label_text:
        text(ctx, label_text, 0, -105, 34, INK)
    ctx.restore()


def sparkles(ctx, x, y, t, r=110, n=8, color="#ffe066"):
    for i in range(n):
        a = i * 2 * math.pi / n + t
        rr = r + math.sin(t * 4 + i) * 12
        sx, sy = x + math.cos(a) * rr, y + math.sin(a) * rr
        s = 6 + 4 * math.sin(t * 6 + i)
        poly(ctx, [(sx, sy - 2 * s), (sx + s / 2, sy - s / 2), (sx + 2 * s, sy),
                   (sx + s / 2, sy + s / 2), (sx, sy + 2 * s), (sx - s / 2, sy + s / 2),
                   (sx - 2 * s, sy), (sx - s / 2, sy - s / 2)], color, 2)


def confetti(ctx, t, n=60, seed=3):
    rnd = random.Random(seed)
    cols = ["#ef476f", "#ffd166", "#06d6a0", "#118ab2", "#ffffff", "#f78c6b"]
    for _ in range(n):
        x0 = rnd.uniform(0, W)
        sp = rnd.uniform(80, 180)
        y = (rnd.uniform(-H, 0) + t * sp) % (H + 40) - 20
        x = x0 + math.sin(t * 2 + x0) * 20
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(t * 3 + x0)
        ctx.rectangle(-6, -3, 12, 6)
        ctx.set_source_rgb(*rgb(rnd.choice(cols)))
        ctx.fill()
        ctx.restore()


def snow(ctx, t, n=70, seed=5):
    rnd = random.Random(seed)
    for _ in range(n):
        x0 = rnd.uniform(0, W)
        sp = rnd.uniform(25, 60)
        y = (rnd.uniform(0, H) + t * sp) % H
        x = x0 + math.sin(t + x0) * 15
        circle(ctx, x, y, rnd.uniform(2, 5), "#ffffff", 0)


# ---------------------------------------------------------------- people

def person(ctx, x, y, s=1.0, t=0.0, shirt="#4f86c6", skin="#f2c49b",
           hair="#5a3825", pants="#3d405b", talk=False, wave=0.0, walk=False,
           robe=None, mustache=False, hat=None, hold=None, facing=1, mood="smile",
           hair_style="short", blink_seed=0.0):
    """Cartoon person. (x, y) is between the feet. ``wave`` 0..1 raises the
    right arm; ``hold`` is a callable(ctx, hx, hy) drawn in the right hand."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s * facing, s)
    step = math.sin(t * 8) if walk else 0.0
    lift = abs(step) * 4 if walk else bob(t, 1.2, 1.5, blink_seed)
    ctx.translate(0, -lift)
    # legs
    if robe is None:
        stroke_line(ctx, [(-12, -70), (-12 + step * 12, 0)], 14, pants)
        stroke_line(ctx, [(12, -70), (12 - step * 12, 0)], 14, pants)
        ellipse(ctx, -12 + step * 12 - 4, 0, 13, 7, INK, 0)
        ellipse(ctx, 12 - step * 12 + 4, 0, 13, 7, INK, 0)
    # body
    if robe is not None:
        poly(ctx, [(-24, -130), (24, -130), (40, 0), (-40, 0)], robe)
    else:
        rrect(ctx, -28, -135, 56, 72, 18, shirt)
    # arms
    swing = -step * 0.5
    la = math.radians(20) + swing
    ax, ay = -26, -122
    stroke_line(ctx, [(ax, ay), (ax - math.sin(la) * 50, ay + math.cos(la) * 50)], 12,
                robe or shirt)
    circle(ctx, ax - math.sin(la) * 52, ay + math.cos(la) * 52, 8, skin, 3)
    ra = math.radians(-20) - swing - wave * (math.radians(150) + math.sin(t * 9) * 0.25)
    bx, by = 26, -122
    hx, hy = bx - math.sin(ra) * 52, by + math.cos(ra) * 52
    stroke_line(ctx, [(bx, by), (bx - math.sin(ra) * 50, by + math.cos(ra) * 50)], 12,
                robe or shirt)
    circle(ctx, hx, hy, 8, skin, 3)
    if hold:
        hold(ctx, hx, hy)
    # head
    hy0 = -170
    circle(ctx, 0, hy0, 36, skin)
    if hair_style == "short":
        ctx.new_path()
        ctx.arc(0, hy0, 37, math.pi * 1.05, math.pi * 1.95)
        ctx.close_path()
        paint(ctx, hair, 3)
    elif hair_style == "long":
        ctx.new_path()
        ctx.arc(0, hy0 - 2, 40, math.pi * 0.85, math.pi * 2.15)
        ctx.line_to(36, hy0 + 30)
        ctx.line_to(26, hy0 - 10)
        ctx.line_to(-26, hy0 - 10)
        ctx.line_to(-36, hy0 + 30)
        ctx.close_path()
        paint(ctx, hair, 3)
    elif hair_style == "bald":
        pass
    if hat == "monk":
        rrect(ctx, -34, hy0 - 70, 68, 42, 6, "#1d1d24")
        rrect(ctx, -40, hy0 - 34, 80, 10, 4, "#1d1d24")
    elif hat == "kalpak":
        rrect(ctx, -30, hy0 - 72, 60, 44, 12, "#2b2522")
    elif hat == "fez":
        poly(ctx, [(-24, hy0 - 30), (24, hy0 - 30), (18, hy0 - 66), (-18, hy0 - 66)], "#b5332e")
    elif hat == "cap":
        ctx.new_path()
        ctx.arc(0, hy0 - 10, 36, math.pi, 2 * math.pi)
        ctx.close_path()
        paint(ctx, shirt, 3)
        rrect(ctx, 0, hy0 - 16, 50, 10, 4, shirt, 3)
    # face
    blink = (t + blink_seed) % 3.1 < 0.12
    for ex in (-13, 13):
        if blink:
            stroke_line(ctx, [(ex - 5, hy0 - 4), (ex + 5, hy0 - 4)], 3)
        else:
            circle(ctx, ex, hy0 - 4, 4.5, INK, 0)
    circle(ctx, -22, hy0 + 10, 6, "#f59a8b", 0)
    circle(ctx, 22, hy0 + 10, 6, "#f59a8b", 0)
    if mustache:
        ctx.new_path()
        ctx.move_to(0, hy0 + 10)
        ctx.curve_to(-8, hy0 + 4, -22, hy0 + 8, -26, hy0 + 18)
        ctx.curve_to(-16, hy0 + 14, -6, hy0 + 16, 0, hy0 + 13)
        ctx.curve_to(6, hy0 + 16, 16, hy0 + 14, 26, hy0 + 18)
        ctx.curve_to(22, hy0 + 8, 8, hy0 + 4, 0, hy0 + 10)
        paint(ctx, hair, 2)
    if talk and math.sin(t * 14) > -0.2:
        ellipse(ctx, 0, hy0 + 18, 8, 5 + 3 * abs(math.sin(t * 11)), "#7a2a2a", 3)
    elif mood == "sad":
        ctx.new_path()
        ctx.arc(0, hy0 + 26, 9, 1.2 * math.pi, 1.8 * math.pi)
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(3.5)
        ctx.stroke()
    elif mood == "sneaky":
        stroke_line(ctx, [(-8, hy0 + 18), (8, hy0 + 15)], 3.5)
    elif not mustache:
        ctx.new_path()
        ctx.arc(0, hy0 + 10, 11, 0.15 * math.pi, 0.85 * math.pi)
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(3.5)
        ctx.stroke()
    ctx.restore()


# ---------------------------------------------------------------- map

# A rough outline of Bulgaria (lon, lat), good enough for a cartoon map.
BG_OUTLINE = [
    (22.67, 44.22), (23.3, 43.85), (24.0, 43.72), (25.0, 43.65), (25.6, 43.66),
    (26.1, 43.96), (27.0, 44.13), (27.9, 43.99), (28.58, 43.75), (28.0, 43.40),
    (27.92, 43.15), (27.75, 42.72), (27.45, 42.48), (27.72, 42.30), (28.02, 41.98),
    (27.3, 42.03), (26.6, 41.95), (26.35, 41.75), (25.9, 41.32), (25.0, 41.42),
    (24.1, 41.55), (23.6, 41.37), (22.93, 41.34), (22.95, 41.9), (22.36, 42.32),
    (22.75, 42.9), (22.45, 43.4), (22.37, 43.85),
]

CITIES = {
    "София": (23.32, 42.70), "Бургас": (27.47, 42.50), "Пловдив": (24.75, 42.15),
    "Варна": (27.91, 43.21), "Ловеч": (24.72, 43.14), "Плевен": (24.62, 43.42),
    "Търново": (25.63, 43.08), "Карлово": (24.81, 42.64), "Благоевград": (23.10, 42.02),
    "Стара Загора": (25.63, 42.43), "Тетевен": (24.27, 42.92), "Трявна": (25.49, 42.87),
    "Кочериново": (23.06, 42.08), "Рибарица": (24.36, 42.83),
}


class BGMap:
    """Projects lon/lat into a box on screen and draws the country."""

    def __init__(self, x, y, w):
        self.lon0, self.lon1, self.lat0, self.lat1 = 22.2, 28.8, 41.2, 44.3
        self.x, self.y, self.w = x, y, w
        self.k = w / (self.lon1 - self.lon0)
        self.h = (self.lat1 - self.lat0) * self.k * 1.3

    def pt(self, lon, lat):
        return (self.x + (lon - self.lon0) * self.k,
                self.y + (self.lat1 - lat) * self.k * 1.3)

    def city(self, name):
        return self.pt(*CITIES[name])

    def draw(self, ctx, fill="#a8d672", sea_color="#7cc3f0"):
        # Black Sea: the coastline (outline points 8..14) closed off to the east.
        coast = [self.pt(*p) for p in BG_OUTLINE[7:15]]
        east = min(W + 10, self.x + self.w + 60)
        top, bottom = self.y - 20, self.y + self.h + 20
        poly(ctx, coast + [(coast[-1][0], bottom), (east, bottom), (east, top),
                           (coast[0][0], top)], sea_color, 0)
        poly(ctx, [self.pt(*p) for p in BG_OUTLINE], fill, 5)

    def dot(self, ctx, name, scale=1.0, color="#ef476f", show=True, size=20, above=True):
        if scale <= 0:
            return
        x, y = self.city(name)
        circle(ctx, x, y, 9 * scale, color, 3)
        if show:
            text(ctx, name, x, y - 16 if above else y + 32, size * scale, INK,
                 outline="#ffffff")


# ---------------------------------------------------------------- pipeline

def spoken(s):
    """Expand the abbreviations of the printed text so the voice reads them
    as words ("2012 г." -> "2012 година", "120 км" -> "120 километра")."""
    s = re.sub(r"(\d{4}) г\.", r"\1 година", s)
    s = re.sub(r"(\d+) км\b", r"\1 километра", s)
    s = re.sub(r"(\d+) м\b", r"\1 метра", s)
    return s.replace("в. „", "вестник „")


class Scene:
    """``caption`` is the on-screen text (the exam's own wording); the voice
    reads ``narration``, which defaults to the caption with abbreviations
    spelled out."""

    def __init__(self, caption, draw, narration=None, pad=1.1):
        self.caption = caption
        self.narration = narration if narration is not None else spoken(caption)
        self.draw = draw
        self.pad = pad
        self.duration = None


def caption(ctx, s, alpha=1.0):
    if not s:
        return
    size = 34
    lines = wrap(ctx, s, size, W - 160)
    if len(lines) > 3:  # long sentences: smaller type so the art stays visible
        size = 28
        lines = wrap(ctx, s, size, W - 160)
    lh = size * 1.3
    h = lh * len(lines) + 26
    y0 = H - h - 18
    ctx.push_group()
    rrect(ctx, 50, y0, W - 100, h, 22, "#fffdf3", 4)
    for i, ln in enumerate(lines):
        text(ctx, ln, W / 2, y0 + 13 + lh * (i + 0.78), size, INK)
    ctx.pop_group_to_source()
    ctx.paint_with_alpha(alpha)


def title_card(title, subtitle, colors=("#ffd166", "#ef476f")):
    """A ready-made opening scene with a big wobbling title."""
    def draw(ctx, t, d):
        g = cairo.LinearGradient(0, 0, W, H)
        g.add_color_stop_rgb(0, *rgb(colors[0]))
        g.add_color_stop_rgb(1, *rgb(colors[1]))
        ctx.set_source(g)
        ctx.paint()
        for i in range(14):
            a = i * math.pi / 7 + t * 0.2
            ctx.new_path()
            ctx.move_to(W / 2, H / 2 - 60)
            ctx.arc(W / 2, H / 2 - 60, 1200, a, a + math.pi / 14)
            ctx.close_path()
            ctx.set_source_rgba(1, 1, 1, 0.12)
            ctx.fill()
        sc = max(pop(t, 0.1, 0.7), 1e-3)
        ctx.save()
        ctx.translate(W / 2, 250)
        ctx.scale(sc, sc)
        ctx.rotate(math.sin(t * 2) * 0.02)
        for i, ln in enumerate(wrap(ctx, title, 64, W - 160)):
            text(ctx, ln, 0, i * 78, 64, "#ffffff", outline=INK)
        ctx.restore()
        if t > 0.8:
            label(ctx, subtitle, W / 2, 470, 30, scale=pop(t, 0.8))
    return draw


def synth(text_, voice, out):
    import certifi
    # edge-tts builds its TLS context from certifi when it is imported; point
    # certifi at SSL_CERT_FILE first so proxies that re-sign TLS are trusted.
    bundle = os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE")
    if bundle:
        certifi.where = lambda: bundle
    import edge_tts

    async def go():
        await edge_tts.Communicate(text_, voice, rate="-10%").save(out)
    asyncio.run(go())


def duration_of(path):
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", path])
    return float(out)


def srt_time(sec):
    ms = int(round(sec * 1000))
    return "%02d:%02d:%02d,%03d" % (ms // 3600000, ms // 60000 % 60, ms // 1000 % 60, ms % 1000)


def render(scenes, out_mp4, voice="bg-BG-KalinaNeural", lead=0.45, preview=None):
    """Narrate, draw and encode ``scenes`` into ``out_mp4`` (+ .srt)."""
    work = tempfile.mkdtemp(prefix="cartoon-")
    wavs = []
    for i, sc in enumerate(scenes):
        wav = os.path.join(work, "s%02d.wav" % i)
        if sc.narration:
            mp3 = os.path.join(work, "s%02d.mp3" % i)
            synth(sc.narration, voice, mp3)
            sc.duration = lead + duration_of(mp3) + sc.pad
            src = ["-i", mp3]
            af = "adelay=%d,apad" % int(lead * 1000)
        else:
            sc.duration = sc.pad
            src = ["-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono"]
            af = "apad"
        subprocess.check_call(["ffmpeg", "-y", "-v", "error", *src, "-af", af,
                               "-t", "%.3f" % sc.duration, "-ar", "24000", "-ac", "1", wav])
        wavs.append(wav)
    lst = os.path.join(work, "list.txt")
    with open(lst, "w") as f:
        f.writelines("file '%s'\n" % w for w in wavs)
    audio = os.path.join(work, "audio.wav")
    subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                           "-i", lst, "-c", "copy", audio])

    write_srt(scenes, os.path.splitext(out_mp4)[0] + ".srt", lead)

    enc = subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra",
         "-s", "%dx%d" % (W, H), "-r", str(FPS), "-i", "-", "-i", audio,
         "-c:v", "libx264", "-preset", "slow", "-crf", "27", "-tune", "animation",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "64k", "-shortest",
         "-movflags", "+faststart", out_mp4], stdin=subprocess.PIPE)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    for i, sc in enumerate(scenes):
        frames = int(round(sc.duration * FPS))
        for f in range(frames):
            t = f / FPS
            ctx = cairo.Context(surf)
            ctx.save()
            sc.draw(ctx, t, sc.duration)
            ctx.restore()
            if i > 0:
                caption(ctx, sc.caption, ease(t / 0.35))
            fade = min(ease(t / 0.3), ease((sc.duration - t) / 0.25))
            if fade < 1:
                ctx.set_source_rgba(0, 0, 0, 1 - fade)
                ctx.paint()
            if preview is not None and f == frames // 2:
                surf.write_to_png(os.path.join(preview, "scene%02d.png" % i))
            surf.flush()
            enc.stdin.write(bytes(surf.get_data()))
    enc.stdin.close()
    if enc.wait() != 0:
        raise SystemExit("ffmpeg failed")


def write_srt(scenes, path, lead):
    start, n, out = 0.0, 0, []
    for sc in scenes:
        if sc.caption:
            n += 1
            out.append("%d\n%s --> %s\n%s\n" % (n, srt_time(start + lead * 0.5),
                                                srt_time(start + sc.duration - 0.2),
                                                sc.caption))
        start += sc.duration
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
