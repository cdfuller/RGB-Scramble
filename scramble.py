from PIL import Image

NUM_COLORS = 64

colors = []

for r in range(0, 64):
  for g in range(0, 64):
    for b in range(0, 64):
      colors.append((r*4, g*4, b*4))

im = Image.new("RGB", (512, 512))

px = im.load()

for x in range(0, 512):
  for y in range(0, 512):
    px[x, y] = colors.pop()

# im.save("00-HELLO-RGB.png")

im.show()
