"""Render the citizenship-test cartoons.

    python3 make.py 1 2 3            # full videos into ../
    python3 make.py --stills 1 /tmp  # one PNG per scene, no audio (fast preview)
"""

import importlib
import os
import sys

import cairo

import cartoon

HERE = os.path.dirname(os.path.abspath(__file__))
NAMES = {"1": "variant-1-burgas", "2": "variant-2-levski", "3": "variant-3-teteven"}


def stills(story, outdir, d=6.0):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, cartoon.W, cartoon.H)
    for i, sc in enumerate(story.SCENES):
        ctx = cairo.Context(surf)
        ctx.save()
        sc.draw(ctx, d * 0.7, d)
        ctx.restore()
        if i:
            cartoon.caption(ctx, sc.caption)
        surf.write_to_png(os.path.join(outdir, "v%s-%02d.png" % (story.__name__[-1], i)))


def main(argv):
    if argv and argv[0] == "--stills":
        stills(importlib.import_module("story" + argv[1]), argv[2])
        return
    for n in argv or sorted(NAMES):
        story = importlib.import_module("story" + n)
        out = os.path.join(HERE, "..", NAMES[n] + ".mp4")
        cartoon.render(story.SCENES, out, voice=story.VOICE)
        print("wrote", os.path.normpath(out))


if __name__ == "__main__":
    main(sys.argv[1:])
