#!/usr/bin/env python3
"""Rotating ASCII Christmas tree. Ctrl+C to quit."""
import math
import random
import shutil
import sys
import time

W, H = 60, 30          # canvas size
HEIGHT = 22            # tree height in rows
RADIUS = 11.0          # base radius
TIERS = 4
FPS = 24

random.seed(7)
# Foliage points: (angle, y in 0..1 from top, radial jitter) -> cone with tiers
points = []
for _ in range(1600):
    t = random.random()
    tier = int(t * TIERS)
    local = (t * TIERS) % 1.0
    r = RADIUS * (tier + 1 + local) / (TIERS + 1) * (0.55 + 0.45 * random.random() ** 0.5)
    points.append((random.random() * math.tau, t, r, random.choice("*&@#o%")))
ornaments = []
for _ in range(26):
    t = 0.12 + random.random() * 0.85
    r = RADIUS * (t + 0.05) * 0.95
    ornaments.append((random.random() * math.tau, t, r, random.choice("OoQ0@")))
trunk = [(a * math.tau / 12, 1.0 + k * 0.04, 1.6, "|") for a in range(12) for k in range(3)]


def frame(angle, tick):
    buf = [[" "] * W for _ in range(H)]
    z = [[-1e9] * W for _ in range(H)]
    cx, top = W // 2, 4

    def plot(x, y, depth, ch):
        sx = int(round(cx + x * 1.0))
        sy = int(round(top + y))
        if 0 <= sx < W and 0 <= sy < H and depth > z[sy][sx]:
            z[sy][sx] = depth
            buf[sy][sx] = ch

    def proj(a, t, r):
        a += angle
        return r * math.cos(a) * 1.9, t * HEIGHT, r * math.sin(a)

    for a, t, r, ch in points:
        x, y, d = proj(a, t, r)
        shade = ".:+*" if d < 0 else "*&@#"
        plot(x, y, d, ch if d > 0 else ("." if d < -4 else ":"))
    for a, t, r, ch in trunk:
        x, y, d = proj(a, t, r)
        plot(x, y, d, "H")
    for i, (a, t, r, ch) in enumerate(ornaments):
        x, y, d = proj(a, t, r)
        if d > -2 and (tick // 6 + i) % 3:
            plot(x, y, d + 100, ch)
    # star on top, blinking
    plot(0, -1, 1e6, "*" if tick // 6 % 2 else "+")
    plot(-1, -1, 1e6, "-"); plot(1, -1, 1e6, "-")
    plot(0, -2, 1e6, "|")
    lines = ["".join(row).rstrip() for row in buf]
    lines.append("Merry Christmas!".center(W))
    return "\n".join(lines)


def main():
    if shutil.get_terminal_size().columns < W:
        print(f"Terminal too narrow (need {W} columns).")
        return
    angle, tick = 0.0, 0
    sys.stdout.write("\x1b[2J\x1b[?25l")
    try:
        while True:
            sys.stdout.write("\x1b[H" + frame(angle, tick) + "\n")
            sys.stdout.flush()
            angle += 0.07
            tick += 1
            time.sleep(1 / FPS)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\x1b[?25h\n")


if __name__ == "__main__":
    main()
