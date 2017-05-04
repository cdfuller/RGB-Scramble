from PIL import Image
import cProfile
from random import shuffle, randint
from datetime import datetime
from colormath.color_objects import sRGBColor, LabColor 
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000 


# Formula for calculating number of colors per channel
# N = number of bits per color.
# (2**N) ** (1/3)

##########
# 2**15
COLOR_DEPTH = 15
IMG_WIDTH = 256
IMG_HEIGHT = 128
COLORS_PER_CHANNEL = 32
COLOR_OFFSET = 8

##########
# # 2**18
# COLOR_DEPTH = 18
# IMG_WIDTH = 512
# IMG_HEIGHT = 512
# COLORS_PER_CHANNEL = 64
# COLOR_OFFSET = 4

##########
# 2**24
# COLOR_DEPTH = 24
# IMG_WIDTH = 4096
# IMG_HEIGHT = 4096
# COLORS_PER_CHANNEL = 256
# COLOR_OFFSET = 1

COLOR_DISTANCE_THRESHOLD = 1000

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
  percentage_pt = int(total / 100 / 10) 

  print("Inserting colors")

  last_pixel = (0, 0, 0)
  # pixel = colors.pop(randint(0, len(colors)))

  for y in range(0, IMG_HEIGHT):
    for x in range(0, IMG_WIDTH):

      # Get random color for first pixel
      if counter == 0:
        pixel = colors.pop(randint(0, len(colors)))
      else:

        i = 0
        current_distance = 999999
        target_color = 0
        
        if y > 0:
          target_color = avg_color([px[x, y-1], last_pixel])
        else:
          target_color = last_pixel

        while current_distance > COLOR_DISTANCE_THRESHOLD and i < len(colors):
          d = calc_distance(target_color, colors[i])
          if d < current_distance:
            current_distance = d
            closest_color = colors[i]
          
          i += 1

        colors.remove(closest_color)
        pixel = closest_color

      px[x, y] = pixel
      last_pixel = pixel

      # Display status
      if counter % percentage_pt == 0:
        print("###########  {:.1%}  ###########".format(counter / total))
      counter += 1

  print("###########  {:.1%}  ###########".format(1))


# def min_color(target, color1, color2):
#   if calc_distance(target, color1) <= calc_distance(target, color2):
#     return color1
#   else:
#     return color2

# Returns an int ranging 0 to 195075. 0 being the same, 195075 being completely opposite
def calc_distance(color1, color2):
  r = color1[0] - color2[0]
  g = color1[1] - color2[1]
  b = color1[2] - color2[2]
  return r * r + g * g + b * b

def avg_color(colors):
  c = {'r': 0, 'g': 0, 'b': 0}
  for color in colors:
    c['r'] += color[0]
    c['g'] += color[1]
    c['b'] += color[2]
  c['r'] = c['r'] / len(colors)
  c['g'] = c['g'] / len(colors)
  c['b'] = c['b'] / len(colors)
  return (int(c['r']), int(c['g']), int(c['b']))


# def min_lab_color(target, color1, color2):
#   if calc_lab_distance(target, color1) <= calc_lab_distance(target, color2):
#     return color1
#   else:
#     return color2


# Returns a float ranging 0 to 100. 0 being the same, 100 being completely opposite
# def calc_lab_distance(color1, color2):
#   color1_rgb = sRGBColor(color1[0] / 255, color1[1] / 255, color1[2] / 255)
#   color2_rgb = sRGBColor(color2[0] / 255, color2[1] / 255, color2[2] / 255)
#   color1_lab = convert_color(color1_rgb, LabColor)
#   color2_lab = convert_color(color2_rgb, LabColor)
#   return delta_e_cie2000(color1_lab, color2_lab)

colors = generate_color_array()
cProfile.run("insert_colors(colors, image)")
# insert_colors(colors, image)

filename = "RGB-D{}-T{}-{}.png".format(COLOR_DEPTH, COLOR_DISTANCE_THRESHOLD, int(datetime.now().timestamp()))

image.save("sandbox/{}".format(filename))
print("Saved {}".format(filename))
image.show()

