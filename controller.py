from scramble import *

def run(config):
  colors = generate_color_array(config)
  image = Image.new("RGB", (config['img_width'], config['img_height']))

  if config['verbose']:
    # Show stats after running
    cProfile.runctx("insert_colors(colors, image, config)", {"colors": colors, "image":image, "insert_colors": insert_colors, 'config': config}, {})
  else:
    insert_colors(colors, image, config)

  # Save image
  if config['save_output']:
    filename = "RGB-{}-D{}-T{}.png".format(int(datetime.now().timestamp()), config['color_depth'], config['threshold'])
    image.save("sandbox/{}".format(filename))
    print_v("Saved {}".format(filename), config)

  image.show()