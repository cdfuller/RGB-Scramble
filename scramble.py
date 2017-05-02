from PIL import Image
import cProfile
from random import shuffle, randint
from datetime import datetime
# from colormath.color_objects import sRGBColor, LabColor 
# from colormath.color_conversions import convert_color
# from colormath.color_diff import delta_e_cie2000 


# Formula for calculating number of colors per channel
# N = number of bits per color.
# (2**N) ** (1/3)

##########
# 2**15

IMG_WIDTH = 256
IMG_HEIGHT = 128
COLORS_PER_CHANNEL = 32
COLOR_OFFSET = 8

##########
# 2**18

# IMG_WIDTH = 512
# IMG_HEIGHT = 512
# COLORS_PER_CHANNEL = 64
# COLOR_OFFSET = 4

image = Image.new("RGB", (IMG_WIDTH, IMG_HEIGHT))


def generate_color_array():
  colors = []
  print("Generating colors")
  for r in range(0, COLORS_PER_CHANNEL):
    for g in range(0, COLORS_PER_CHANNEL):
      for b in range(0, COLORS_PER_CHANNEL):
        colors.append((r * COLOR_OFFSET, g * COLOR_OFFSET, b * COLOR_OFFSET))
  shuffle(colors)
  return colors

def insert_colors(colors, image):
  px = image.load()
  counter = 0
  total = IMG_WIDTH * IMG_HEIGHT
  percentage_pt = int(total / 100) 

  print("Inserting colors")

  last_pixel = (0, 0, 0)

  for y in range(0, IMG_HEIGHT):
    for x in range(0, IMG_WIDTH):

      # Get random color for first pixel
      if counter == 0:
        pixel = colors.pop(randint(0, len(colors)))
      else:
        closest_color = colors[0]

        for c in colors:
          closest_color = min_color(last_pixel, closest_color, c)

        colors.remove(closest_color)
        pixel = closest_color

      px[x, y] = pixel
      last_pixel = pixel

      # Display status
      if counter % percentage_pt == 0:
        print("###########  {:.2%}  ###########".format(counter / total))
      counter += 1

  print("###########  {:.2%}  ###########".format(1))


def min_color(target, color1, color2):
  if calc_distance(target, color1) <= calc_distance(target, color2):
    return color1
  else:
    return color2


def calc_distance(color1, color2):
  r = color1[0] - color2[0]
  g = color1[1] - color2[1]
  b = color1[2] - color2[2]

  return r * r + g * g + b * b


# def get_closest_pixel(colors, pixel):
#   p = 0
#   for c in color:
#     p = min_color(pixel, p, c)
#   return p

# def min_lab_color(target, color1, color2):
#   if calc_lab_distance(target, color1) <= calc_lab_distance(target, color2):
#     return color1
#   else:
#     return color2

# def calc_lab_distance(color1, color2):
#   color1_rgb = sRGBColor(color1[0] / 255, color1[1] / 255, color1[2] / 255)
#   color2_rgb = sRGBColor(color2[0] / 255, color2[1] / 255, color2[2] / 255)
#   color1_lab = convert_color(color1_rgb, LabColor)
#   color2_lab = convert_color(color2_rgb, LabColor)
#   return delta_e_cie2000(color1_lab, color2_lab)

colors = generate_color_array()
cProfile.run("insert_colors(colors, image)")
# insert_colors(colors, image)

image.show()
# image.save("sandbox/RGB-"+str(int(datetime.now().timestamp()))+".png")

