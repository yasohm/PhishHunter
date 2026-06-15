"""Generate PNG icons for the PhishGuard extension using stdlib only."""
import struct
import zlib
import os

ICONS_DIR = os.path.join(os.path.dirname(__file__), '..', 'icons')

def make_png(size, r, g, b, shape='shield'):
    """Create a solid-color PNG with a simple shield silhouette."""
    pixels = []
    cx, cy = size / 2, size / 2

    for y in range(size):
        row = []
        for x in range(size):
            nx = (x - cx) / (size * 0.45)
            ny = (y - cy) / (size * 0.45)

            # Shield shape: top half is rounded rectangle, bottom is triangle point
            in_shape = False
            # Upper rectangle portion
            if -0.85 <= nx <= 0.85 and -0.90 <= ny <= 0.15:
                # Rounded corners
                corner_r = 0.25
                cx2, cy2 = abs(abs(nx) - (0.85 - corner_r)), abs(max(ny, -0.90 + corner_r) - (-0.90 + corner_r))
                if abs(nx) <= 0.85 - corner_r or abs(ny + 0.90) >= corner_r or (abs(nx) - (0.85 - corner_r))**2 + (ny + 0.90 + corner_r)**2 <= corner_r**2:
                    in_shape = True
            # Lower triangle (shield tip)
            if 0.10 <= ny <= 1.0 and abs(nx) <= (1.0 - ny) * 0.90:
                in_shape = True

            if in_shape:
                # Slight gradient: lighter at top
                factor = max(0.7, 1.0 - ny * 0.15)
                pr = min(255, int(r * factor))
                pg = min(255, int(g * factor))
                pb = min(255, int(b * factor))
                row.extend([pr, pg, pb, 255])
            else:
                row.extend([0, 0, 0, 0])  # transparent

        pixels.append(bytes(row))

    def chunk(name, data):
        crc = zlib.crc32(name + data) & 0xFFFFFFFF
        return struct.pack('>I', len(data)) + name + data + struct.pack('>I', crc)

    raw = b''.join(b'\x00' + row for row in pixels)
    compressed = zlib.compress(raw, 9)

    png  = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 6, 0, 0, 0))  # RGBA
    png += chunk(b'IDAT', compressed)
    png += chunk(b'IEND', b'')
    return png


ICONS = [
    ('icon-16.png',           16,  30,  64, 175),  # blue  — default
    ('icon-48.png',           48,  30,  64, 175),
    ('icon-128.png',         128,  30,  64, 175),
    ('icon-safe-48.png',      48,  22, 163,  74),  # green — safe
    ('icon-suspicious-48.png',48, 234,  88,  12),  # orange— suspicious
    ('icon-dangerous-48.png', 48, 220,  38,  38),  # red   — dangerous
]

os.makedirs(ICONS_DIR, exist_ok=True)

for filename, size, r, g, b in ICONS:
    path = os.path.join(ICONS_DIR, filename)
    data = make_png(size, r, g, b)
    with open(path, 'wb') as f:
        f.write(data)
    print(f'  Created {filename} ({size}x{size})')

print('Done.')
