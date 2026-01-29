out = open("segments.txt", "w")

with open("segments_full.txt") as f:
    lines = [l.strip() for l in f if l.strip()]

i = 0
while i < len(lines):
    if lines[i].startswith("L"):
        n = int(lines[i].split()[1])
        coords = []
        for j in range(i+1, i+1+n):
            x, y = map(float, lines[j].split())
            coords.append((x, y))

        # Split polylines into segments
        if len(coords) >= 2:
            for k in range(len(coords) - 1):
                x1, y1 = coords[k]
                x2, y2 = coords[k+1]
                out.write(f"{x1} {y1} {x2} {y2}\n")

        i += 1 + n
    else:
        i += 1

out.close()
