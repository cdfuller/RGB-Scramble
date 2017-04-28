from PIL import Image
from collections import deque
import cProfile

IMG_WIDTH = 4096
IMG_HEIGHT = 4096

image = Image.new("RGB", (IMG_WIDTH, IMG_HEIGHT))


def generate_color_array():
  colors = []
  print("Generating colors")
  for r in range(0, 256):
    for g in range(0, 256):
      for b in range(0, 256):
        colors.append((r, g, b))
  return colors

def insert_colors(colors, image):
  px = image.load()
  counter = 0
  total = IMG_WIDTH * IMG_HEIGHT
  percentage_pt = int(total / 100 / 10) 
  colors = deque(colors)

  print("Inserting colors")

  for x in range(0, IMG_WIDTH):
    for y in range(0, IMG_HEIGHT):
      counter += 1
      # print(counter, counter / total)
      if counter % percentage_pt == 0:
        print("{}%".format(counter / total * 100))
      
      px[x, y] = colors.pop()

      # if counter % 2 == 0:
      #   px[x, y] = colors.pop()
      # else:
      #   px[x, y] = colors.popleft()

  print("100%")
  # return image
# im.save("03-HELLO-24-BIT.png")

colors = generate_color_array()
# cProfile.run("insert_colors(colors, image)")
insert_colors(colors, image)

image.show()


# def sort_by_hue(color1, color2):

