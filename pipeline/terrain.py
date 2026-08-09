#!/usr/bin/env python3
"""Build the fleet monitor's terrain backdrop: a dark-styled hillshade of BC and
surroundings from AWS/Mapzen Terrain Tiles (terrarium encoding), web-mercator z7.

Output: terrain-bc.jpg + the world-coordinate bounds the page needs to place it.
World coords on the page: x = lon, y = -(180/pi)*asinh(tan(lat)) — i.e. mercator
degrees — so a mercator tile mosaic maps linearly onto the canvas.
"""
import io, sys, time, urllib.request
import numpy as np
from PIL import Image

Z, X0, X1, Y0, Y1 = 7, 14, 23, 36, 44          # x,y inclusive: 10 x 9 tiles = 2560 x 2304 px
URL = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"

def fetch(z, x, y):
    for attempt in range(4):
        try:
            with urllib.request.urlopen(URL.format(z=z, x=x, y=y), timeout=60) as r:
                return Image.open(io.BytesIO(r.read())).convert("RGB")
        except Exception as e:
            print(f"  retry {x}/{y}: {e}", file=sys.stderr)
            time.sleep(2)
    raise SystemExit(f"tile {x}/{y} failed")

W, H = (X1 - X0 + 1) * 256, (Y1 - Y0 + 1) * 256
elev = np.zeros((H, W), dtype=np.float64)
for ty in range(Y0, Y1 + 1):
    for tx in range(X0, X1 + 1):
        im = np.asarray(fetch(Z, tx, ty), dtype=np.float64)
        e = im[:, :, 0] * 256 + im[:, :, 1] + im[:, :, 2] / 256 - 32768
        elev[(ty - Y0) * 256:(ty - Y0 + 1) * 256, (tx - X0) * 256:(tx - X0 + 1) * 256] = e
    print(f"row {ty} done", file=sys.stderr)

# Hillshade (az 315, alt 45), pixel-unit gradients — style, not survey.
gy, gx = np.gradient(elev)
gx /= 60.0; gy /= 60.0                          # vertical exaggeration tune
slope = np.pi / 2 - np.arctan(np.hypot(gx, gy))
aspect = np.arctan2(-gx, gy)
az, alt = np.radians(315), np.radians(45)
shade = np.sin(alt) * np.sin(slope) + np.cos(alt) * np.cos(slope) * np.cos(az - np.pi / 2 - aspect)
shade = np.clip(shade, 0, 1)

# Dark-theme composite: deep base, faint hypsometric lift, hillshade modulation, flat dark sea.
t = np.clip(elev / 2600.0, 0, 1) ** 0.7          # elevation tint 0..1
lo = np.array([15.0, 16.0, 20.0]); hi = np.array([46.0, 48.0, 58.0])
rgb = lo[None, None, :] + (hi - lo)[None, None, :] * t[:, :, None]
rgb *= (0.55 + 0.75 * shade)[:, :, None]
sea = elev <= 0
rgb[sea] = np.array([9.0, 11.0, 15.0])
img = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
out = sys.argv[1] if len(sys.argv) > 1 else "terrain-bc.jpg"
img.save(out, "JPEG", quality=84, optimize=True)

lon = lambda x: x * 360 / 2 ** Z - 180
mercdeg = lambda y: -180 * (1 - 2 * y / 2 ** Z)
print(f"wrote {out} {W}x{H}")
print(f"world bounds: x0={lon(X0)} x1={lon(X1 + 1)} y0={mercdeeg(Y0) if False else mercdeg(Y0)} y1={mercdeg(Y1 + 1)}")
