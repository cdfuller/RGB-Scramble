import argparse
from controller import run

# Minimum similarity threshold
# Logarithmic range: 0 to 195075

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
