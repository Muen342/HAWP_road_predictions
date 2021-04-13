from PIL import Image, ImageDraw
import math
import cv2
import re

PATH = 'data/wireframe/images/'

f = open("train.json", "r")


newfile = f.read()

indexesw = [m.start() for m in re.finditer('"width":"', newfile)]
imagenames = []
for i in range(len(indexesw)):
    index2 = newfile[indexesw[i]+9:].index('"')
    fi = newfile[indexesw[i]+9:index2+ indexesw[i]+9]
    im = cv2.imread(PATH + fi)
    imagenames.append([im.shape, fi])
print('done reading')
for ima in imagenames:
    c = ima[0]
    newfile = newfile.replace('width":"'+ima[1]+'"','width":'+str(c[0])).replace('height":"'+ima[1]+'"','height":'+str(c[1]))
ff = open("train.json", "w")
ff.write(newfile)
