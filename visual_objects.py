import math
import random
from typing import Optional, Tuple, List


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def norm(value: Optional[float], vmin: float, vmax: float) -> float:
    if value is None:
        return 0.0
    if vmax == vmin:
        return 0.0
    t = (value - vmin) / (vmax - vmin)
    return clamp(t, 0.0, 1.0)


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * clamp(t, 0.0, 1.0)


def hsl_to_rgb(h: float, s: float, l: float) -> Tuple[int, int, int]:
    c = (1 - abs(2 * l - 1)) * s
    hp = (h / 60) % 6
    x = c * (1 - abs(hp % 2 - 1))
    r = g = b = 0

    if 0 <= hp < 1:
        r, g, b = c, x, 0
    elif 1 <= hp < 2:
        r, g, b = x, c, 0
    elif 2 <= hp < 3:
        r, g, b = 0, c, x
    elif 3 <= hp < 4:
        r, g, b = 0, x, c
    elif 4 <= hp < 5:
        r, g, b = x, 0, c
    elif 5 <= hp < 6:
        r, g, b = c, 0, x

    m = l - c / 2
    return (int((r + m) * 255),
            int((g + m) * 255),
            int((b + m) * 255))


# ------------------------------------------------------------
# FLOW FIELD
# ------------------------------------------------------------
class FlowField:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def vector(self, x: float, y: float, t: float):
        nx = x / self.width
        ny = y / self.height

        angle = (
            math.sin(nx * 3 + t * 0.2)
            + math.cos(ny * 4 - t * 0.15)
            + math.sin((nx + ny) * 2.5 + t * 0.1)
        )

        speed = 70
        return math.cos(angle) * speed, math.sin(angle) * speed


# ------------------------------------------------------------
# FIREFLY CLASS
# ------------------------------------------------------------
class Firefly:
    def __init__(self, x, y, color, radius, speed_limit, flicker_rate, depth):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0

        self.color = color
        self.radius = radius
        self.speed_limit = speed_limit
        self.flicker_rate = flicker_rate
        self.flicker_phase = random.uniform(0, math.pi * 2)

        self.depth = depth
        self.trail: List[Tuple[float, float]] = []

    def apply_flow(self, flow: 'FlowField', dt: float, t: float):
        fx, fy = flow.vector(self.x, self.y, t)
        self.vx += fx * dt * self.depth
        self.vy += fy * dt * self.depth

        speed = math.hypot(self.vx, self.vy)
        if speed > self.speed_limit:
            scale = self.speed_limit / speed
            self.vx *= scale
            self.vy *= scale

    def update(self, dt: float, flow: 'FlowField', t: float, w: int, h: int):
        self.apply_flow(flow, dt, t)

        self.x += self.vx * dt + math.sin(t * 0.8 + self.depth * 10) * 0.4
        self.y += self.vy * dt + math.cos(t * 0.9 + self.depth * 12) * 0.4

        if self.x < 0: self.x += w
        if self.x > w: self.x -= w
        if self.y < 0: self.y += h
        if self.y > h: self.y -= h

        self.flicker_phase += self.flicker_rate * dt

        self.trail.append((self.x, self.y))
        if len(self.trail) > 6:
            self.trail.pop(0)

    def alpha(self) -> float:
        return 0.7 + 0.3 * math.sin(self.flicker_phase)

    def draw(self, surface):
        import pygame

        a = clamp(self.alpha(), 0, 1)

        for i in range(3, 0, -1):
            r = int(self.radius * (i / 3))
            strength = int(a * (80 + 40 * i))

            glow = pygame.Surface((r * 2 + 2, r * 2 + 2), pygame.SRCALPHA)
            pygame.draw.circle(glow, (*self.color, strength), (r + 1, r + 1), r)
            surface.blit(glow, (int(self.x) - r, int(self.y) - r))
