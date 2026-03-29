#!/usr/bin/env python3
"""Color space conversions — RGB, HSL, HSV, HEX, CMYK."""
import sys, math

def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hsl(r, g, b):
    r, g, b = r/255, g/255, b/255
    mx, mn = max(r,g,b), min(r,g,b)
    l = (mx+mn)/2
    if mx == mn: h = s = 0
    else:
        d = mx - mn
        s = d/(2-mx-mn) if l > 0.5 else d/(mx+mn)
        if mx == r: h = ((g-b)/d + (6 if g<b else 0))/6
        elif mx == g: h = ((b-r)/d + 2)/6
        else: h = ((r-g)/d + 4)/6
    return round(h*360), round(s*100), round(l*100)

def hsl_to_rgb(h, s, l):
    h, s, l = h/360, s/100, l/100
    if s == 0: r = g = b = l
    else:
        def hue2rgb(p, q, t):
            if t < 0: t += 1
            if t > 1: t -= 1
            if t < 1/6: return p + (q-p)*6*t
            if t < 1/2: return q
            if t < 2/3: return p + (q-p)*(2/3-t)*6
            return p
        q = l*(1+s) if l < 0.5 else l+s-l*s
        p = 2*l - q
        r = hue2rgb(p, q, h+1/3)
        g = hue2rgb(p, q, h)
        b = hue2rgb(p, q, h-1/3)
    return round(r*255), round(g*255), round(b*255)

def rgb_to_cmyk(r, g, b):
    if r == g == b == 0: return 0, 0, 0, 100
    r, g, b = r/255, g/255, b/255
    k = 1 - max(r, g, b)
    c = (1-r-k)/(1-k)
    m = (1-g-k)/(1-k)
    y = (1-b-k)/(1-k)
    return round(c*100), round(m*100), round(y*100), round(k*100)

def test():
    assert rgb_to_hex(255, 0, 128) == "#ff0080"
    assert hex_to_rgb("#ff0080") == (255, 0, 128)
    h, s, l = rgb_to_hsl(255, 0, 0)
    assert h == 0 and s == 100 and l == 50
    r, g, b = hsl_to_rgb(0, 100, 50)
    assert (r, g, b) == (255, 0, 0)
    r2, g2, b2 = hsl_to_rgb(120, 100, 50)
    assert (r2, g2, b2) == (0, 255, 0)
    c, m, y, k = rgb_to_cmyk(255, 0, 0)
    assert c == 0 and m == 100 and y == 100 and k == 0
    print("  color_space: ALL TESTS PASSED")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Color space converter")
