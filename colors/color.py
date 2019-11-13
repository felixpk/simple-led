from colorsys import rgb_to_hsv, hsv_to_rgb


class HSV:
    def __init__(self, h, s, v):
        self.h: float = h
        self.s: float = s
        self.v: float = v

    def rgb(self) -> 'RGB':
        _rgb = hsv_to_rgb(self.h, self.s, self.v)
        return RGB(_rgb[0], _rgb[1], _rgb[2])

    def rgb_255(self) -> 'RGB255':
        _rgb = hsv_to_rgb(self.h, self.s, self.v)
        return RGB255(_rgb[0] * 255, _rgb[1] * 255, _rgb[2] * 255)

    def __repr__(self):
        return f"hsv({self.h}, {self.s}, {self.v})"


class RGB255:
    def __init__(self, r, g, b):
        self.r: int = int(r)
        self.g: int = int(g)
        self.b: int = int(b)

    def rgb(self) -> 'RGB':
        return RGB(float(self.r) / 255, float(self.g) / 255, float(self.b) / 255)

    def __repr__(self):
        return f"rgb({self.r}, {self.g}, {self.b})"


class RGB:
    def __init__(self, r, g, b):
        self.r: float = r
        self.g: float = g
        self.b: float = b

    def rgb_255(self) -> RGB255:
        return RGB255(self.r * 255, self.g * 255, self.b * 255)

    def hsv(self) -> HSV:
        _hsv = rgb_to_hsv(self.r, self.g, self.b)
        return HSV(_hsv[0], _hsv[1], _hsv[2])

    def __repr__(self):
        return f"rgb({self.r}, {self.g}, {self.b})"
