import PIL.Image as Image
from random import shuffle, randrange
import math
import time
import cProfile

# NUMTOSEARCH = 1000


def mulColor(color, factor):
    return (int(color[0]*factor), int(color[1]*factor), int(color[2]*factor))


def makeAllColors(arg):
    colors = []
    for r in range(0, arg):
        for g in range(0, arg):
            for b in range(0, arg):
                colors.append((r, g, b))
    return colors

def distance(color1, color2):
    return math.sqrt(pow(color2[0]-color1[0], 2) + pow(color2[1]-color1[1], 2) + pow(color2[2]-color1[2], 2))

def getClosestColor(to, colors):
    closestColor = colors[0]
    d = distance(to, closestColor)
    for color in colors:
        if distance(to, color) < d:
            closestColor = color
            d = distance(to, closestColor)
    return closestColor

imgsize = (256, 128)
#imgsize = (10, 10)
colors = makeAllColors(32)
shuffle(colors)
factor = 255.0/32.0
img = Image.new("RGB", imgsize, "white")
#start = (imgsize[0]/4, imgsize[1]/4)
start = (int(imgsize[0]/2), 0)
startColor = colors.pop(randrange(len(colors)))
img.putpixel(start, mulColor(startColor, factor))

#color = getClosestColor(startColor, colors)
#img.putpixel((start[0]+1, start[1]), mulColor(color, factor))

edgePixels = [(start, startColor)]
donePositions = [start]
recentlyDone = [] + donePositions
def run():
    for pixel in edgePixels:
        if len(colors) > 0:
            color = getClosestColor(pixel[1], colors)
            # color = getClosestColor(pixel[1], colors[:NUMTOSEARCH])
        m = [(pixel[0][0]-1, pixel[0][1]), (pixel[0][0]+1, pixel[0][1]), (pixel[0][0], pixel[0][1]-1), (pixel[0][0], pixel[0][1]+1)]
        if len(donePositions) >= imgsize[0]*imgsize[1]:
            break
        for pos in m:
            if not pos in recentlyDone and not pos in donePositions:
            # if not pos in donePositions:
                if not (pos[0] < 0 or pos[1] < 0 or pos[0] >= img.size[0] or pos[1] >= img.size[1]):
                    img.putpixel(pos, mulColor(color, factor))
                    #print(color)
                    donePositions.append(pos)
                    if len(recentlyDone) > 1000:
                        recentlyDone.pop(0)
                    recentlyDone.append(pos)
                    edgePixels.append((pos, color))
                    colors.remove(color)
                    if len(colors) > 0:
                        color = getClosestColor(pixel[1], colors)
                        # color = getClosestColor(pixel[1], colors[:NUMTOSEARCH])
        print((len(donePositions) * 1.0) / (imgsize[0]*imgsize[1]))
    print(len(donePositions))
    filename = "colors-" + str(int(time.time())) + ".png"
    img.save(filename)

if __name__ == "__main__":
    print("main ran")
    cProfile.run('run()')
    # run();
