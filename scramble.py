from PIL import Image
import cProfile
from random import shuffle, randint
from datetime import datetime
from colormath.color_objects import sRGBColor, LabColor 
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000 

# Minimum similarity threshold
# Logarithmic range: 0 to 195075
# 
# COLOR_DISTANCE_THRESHOLD = 2000

# Formula for calculating number of colors per channel
# N = number of bits per color.
# (2**N) ** (1/3)

presets = {
  15: {
    "color_depth": 15,
    "colors_per_channel": 32,
    "color_offset": 8,
    "img_width": 256,
    "img_height": 128,
  },
  18: {
    "color_depth": 18,
    "colors_per_channel": 64,
    "color_offset": 4,
    "img_width": 512,
    "img_height": 512,
  },
  24: {
    "color_depth": 24,
    "colors_per_channel": 256,
    "color_offset": 1,
    "img_width": 4096,
    "img_height": 4096,
  },
}

def generate_color_array(config):
  colors = []
  print("Generating colors")
  for r in range(0, config['colors_per_channel']):
    for g in range(0, config['colors_per_channel']):
      for b in range(0, config['colors_per_channel']):
        colors.append((r * config['color_offset'], g * config['color_offset'], b * config['color_offset']))
  shuffle(colors)
  return colors

def insert_colors(colors, image):
  px = image.load()
  counter = 0
  total = config['img_width'] * config['img_height']
  percentage_pt = int(total / 100 / 10) 

  print("Inserting colors")

  last_pixel = (0, 0, 0)
  # pixel = colors.pop(randint(0, len(colors)))

  for y in range(0, config['img_height']):
    for x in range(0, config['img_width']):

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

        while current_distance > config['threshold'] and i < len(colors):
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

def run(config):
  colors = generate_color_array(config)
  image = Image.new("RGB", (config['img_width'], config['img_height']))

  if config['verbose']:
    # Show stats after running
    cProfile.runctx("insert_colors(colors, image)", {"colors": colors, "image":image, "insert_colors": insert_colors}, {})
  else:
    insert_colors(colors, image)

  # Save image
  if config['save_output']:
    filename = "RGB-{}-D{}-T{}.png".format(int(datetime.now().timestamp()), config['color_depth'], config['threshold'])
    image.save("sandbox/{}".format(filename))
    print("Saved {}".format(filename))

  image.show()

if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--depth', help='set the color depth of the output image', type=int, choices=[15, 18, 24], default=15)
  parser.add_argument('-t', '--threshold', help='set the threshold for color similarity', type=int, default=200)
  parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
  parser.add_argument('--no-save', help='don\'t save output file', action='store_false')
  args = parser.parse_args()

  config = presets[args.depth]
  config['verbose'] = args.verbose
  config['threshold'] = args.threshold
  config['save_output'] = args.no_save

  run(config);
