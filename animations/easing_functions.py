import math


def ease_in(t: float):
    return 1.0 - math.cos(t * math.pi * 0.5)


def ease_out(t: float):
    return math.sin(t * math.pi * 0.5)


def smoothstep(t: float):
    return t * t * t * (t * (6.0 * t - 15.0) + 10.0)
