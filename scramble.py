from random import shuffle, randint
# from colormath.color_objects import sRGBColor, LabColor 
# from colormath.color_conversions import convert_color
# from colormath.color_diff import delta_e_cie2000 
from view import print_v


def generate_color_array(config):
  colors = []
  print_v("Generating colors", config)
  for r in range(0, config['colors_per_channel']):
    for g in range(0, config['colors_per_channel']):
      for b in range(0, config['colors_per_channel']):
        colors.append((r * config['color_offset'], g * config['color_offset'], b * config['color_offset']))
  shuffle(colors)
  return colors

def insert_colors(colors, image, config):
  px = image.load()
  counter = 0
  total = config['img_width'] * config['img_height']
  percentage_pt = int(total / 100 / 10) 

  print_v("Inserting colors", config)

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
        print_v("###########  {:.1%}  ###########".format(counter / total), config)
      counter += 1

  print_v("###########  {:.1%}  ###########".format(1), config)


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
