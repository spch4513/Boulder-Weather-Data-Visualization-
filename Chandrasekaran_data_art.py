"""
Firefly Cosmos - Boulder Weather Generative Field
"""

import csv
import os
import random
import pygame
from typing import Dict, Optional, List

from visual_objects import Firefly, FlowField, norm, lerp, hsl_to_rgb


WIDTH = 1400
HEIGHT = 800
FPS = 60
CSV_FILE = "boulder_weather.csv"
FIREFLY_COUNT = 4500


def parse_float(v: Optional[str]) -> Optional[float]:
    if v is None or v.strip() == "":
        return None
    try:
        return float(v)
    except:
        return None


def load_rows(path: str) -> List[Dict]:
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        for r in rdr:
            rows.append({
                "DATE": r.get("DATE"),
                "AWND": parse_float(r.get("AWND")),
                "PRCP": parse_float(r.get("PRCP")),
                "SNOW": parse_float(r.get("SNOW")),
                "TMAX": parse_float(r.get("TMAX")),
                "TMIN": parse_float(r.get("TMIN")),
            })
    return rows


def compute_stats(rows: List[Dict]) -> Dict[str, float]:
    stats = {}
    keys = ["AWND", "PRCP", "SNOW", "TMAX", "TMIN"]

    for k in keys:
        vals = [r[k] for r in rows if r[k] is not None]
        stats[f"{k}_min"] = min(vals) if vals else 0
        stats[f"{k}_max"] = max(vals) if vals else 1

    return stats


def make_fireflies(
    rows: List[Dict],
    stats: Dict[str, float],
    count: int
) -> List[Firefly]:

    fireflies = []

    for _ in range(count):
        row = random.choice(rows)

        # temperature controls color
        tmax = row["TMAX"]
        tmin = row["TMIN"]
        tavg = (tmax + tmin) / 2 if tmax is not None and tmin is not None else 0
        t_norm = norm(tavg, stats["TMIN_min"], stats["TMAX_max"])

        hue = lerp(210, 35, t_norm)
        sat = lerp(0.45, 0.75, t_norm)
        light = 0.60
        color = hsl_to_rgb(hue, sat, light)

        # precipitation controls size
        p_norm = norm(row["PRCP"], stats["PRCP_min"], stats["PRCP_max"])
        radius = lerp(3.5, 12, p_norm)

        # wind controls drift speed
        w_norm = norm(row["AWND"], stats["AWND_min"], stats["AWND_max"])
        speed_limit = lerp(30, 160, w_norm)

        # snow controls flicker speed
        s_norm = norm(row["SNOW"], stats["SNOW_min"], stats["SNOW_max"])
        flicker = lerp(1.5, 6.0, s_norm)

        # place anywhere on screen
        x = random.uniform(0, WIDTH)
        y = random.uniform(0, HEIGHT)

        depth = random.uniform(0.4, 1.0)

        ff = Firefly(x, y, color, radius, speed_limit, flicker, depth)
        fireflies.append(ff)

    return fireflies


def gradient_bg(surface):
    top = (6, 10, 28)
    bottom = (2, 4, 12)
    for y in range(HEIGHT):
        t = y / HEIGHT
        col = (
            int(top[0] * (1 - t) + bottom[0] * t),
            int(top[1] * (1 - t) + bottom[1] * t),
            int(top[2] * (1 - t) + bottom[2] * t),
        )
        pygame.draw.line(surface, col, (0, y), (WIDTH, y))


def run():
    csv_path = os.path.join(os.path.dirname(__file__), CSV_FILE)

    rows = load_rows(csv_path)
    stats = compute_stats(rows)

    flow = FlowField(WIDTH, HEIGHT)
    fireflies = make_fireflies(rows, stats, FIREFLY_COUNT)

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Firefly Cosmos - Boulder Weather")
    clock = pygame.time.Clock()

    running = True
    t = 0

    while running:
        dt = clock.tick(FPS) / 1000
        t += dt

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        gradient_bg(screen)

        for f in fireflies:
            f.update(dt, flow, t, WIDTH, HEIGHT)
            f.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    run()
