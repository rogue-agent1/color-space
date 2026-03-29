#!/usr/bin/env python3
"""Color space converter — RGB, HSL, HSV, CMYK, hex."""
import sys, math

def rgb_to_hex(r, g, b): return f"#{r:02x}{g:02x}{b:02x}"
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
        if mx == r: h = ((g-b)/d + (6 if g < b else 0)) / 6
        elif mx == g: h = ((b-r)/d + 2) / 6
        else: h = ((r-g)/d + 4) / 6
    return round(h*360, 1), round(s*100, 1), round(l*100, 1)

def hsl_to_rgb(h, s, l):
    h, s, l = h/360, s/100, l/100
    if s == 0: v = int(l*255); return v, v, v
    def hue2rgb(p, q, t):
        if t < 0: t += 1
        if t > 1: t -= 1
        if t < 1/6: return p + (q-p)*6*t
        if t < 1/2: return q
        if t < 2/3: return p + (q-p)*(2/3-t)*6
        return p
    q = l*(1+s) if l < 0.5 else l+s-l*s; p = 2*l - q
    return (int(hue2rgb(p,q,h+1/3)*255), int(hue2rgb(p,q,h)*255), int(hue2rgb(p,q,h-1/3)*255))

def rgb_to_cmyk(r, g, b):
    if r == g == b == 0: return 0, 0, 0, 100
    c, m, y = 1-r/255, 1-g/255, 1-b/255
    k = min(c, m, y)
    return (round((c-k)/(1-k)*100,1), round((m-k)/(1-k)*100,1), round((y-k)/(1-k)*100,1), round(k*100,1))

def main():
    if len(sys.argv) < 2: print("Usage: color_space.py <demo|test>"); return
    if sys.argv[1] == "test":
        assert rgb_to_hex(255, 128, 0) == "#ff8000"
        assert hex_to_rgb("#ff8000") == (255, 128, 0)
        h, s, l = rgb_to_hsl(255, 0, 0)
        assert h == 0 and s == 100 and l == 50
        r, g, b = hsl_to_rgb(0, 100, 50)
        assert r == 255 and g == 0 and b == 0
        r2, g2, b2 = hsl_to_rgb(120, 100, 50)
        assert g2 == 255
        c, m, y, k = rgb_to_cmyk(255, 0, 0)
        assert k == 0 and c == 0 and m == 100 and y == 100
        _, _, _, k2 = rgb_to_cmyk(0, 0, 0); assert k2 == 100
        # Grayscale roundtrip
        r3, g3, b3 = hsl_to_rgb(0, 0, 50)
        assert r3 == g3 == b3
        print("All tests passed!")
    else:
        for name, rgb in [("Red",(255,0,0)),("Green",(0,255,0)),("Blue",(0,0,255))]:
            print(f"{name}: hex={rgb_to_hex(*rgb)}, hsl={rgb_to_hsl(*rgb)}, cmyk={rgb_to_cmyk(*rgb)}")

if __name__ == "__main__": main()
