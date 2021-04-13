import json
import math
import cv2
import re
from os import listdir
from os.path import isfile, join
path = "./data/wireframe/images"
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
def FilterFiles(name):
    if('json' in name):
        return True
    else:
        return False
uniques = filter(FilterFiles, onlyfiles)
tofile = []
def calcDist(X,Y):
    return math.sqrt((float(X[0])-float(Y[0]))*(float(X[0])-float(Y[0]))+ (float(X[1])-float(Y[1]))*(float(X[1])-float(Y[1])))

def genLine (X,Y):
    
    if((float(Y[0])-float(X[0])) == 0):
        m = math.inf
        # if vertical use b as x intercept
        b = X[0]
    else:
        m = (float(Y[1])-float(X[1]))/(float(Y[0])-float(X[0]))
        b = float(X[1])-(m*float(X[0]))
    return [m,b]

def getMidpoint(X, Y):
    return [(float(X[0])+float(Y[0]))/2,(float(X[1])+float(Y[1]))/2]
def findIntersect(line, Y):
    if(math.abs(line[0]) == math.inf):
        return [line[1], Y[1]]
    elif(line[0] == 0):
        return [Y[0], line[1]]
    else:
        m = -1/line[0]
        b2 = float(Y[1])-(m*float(Y[0]))
        x = (b2-line[1])/(line[0]-m)
        y = m*x+b2
        return [x,y]

def getRange(current, ra, l):
    if(current - ra < 0):
        lower = 0
    else:
        lower = current - ra
    if(current + ra > len(l) - 1):
        upper = len(l) - 1
    else:
        upper = current + ra
    return [lower, upper]

def getAngle(m1,m2):
    if(((1+(m1*m2))) == 0):
        return 90
    return math.degrees(math.atan((m1-m2)/(1+(m1*m2))))

def getAlter(popped, index):
    count = 0
    for p in popped:
        if(p < index):
            count +=1
    return count

def isOnSameLine(X,Y):
    mid1 = getMidpoint(X[0],X[1])
    mid2 = getMidpoint(Y[0],Y[1])
    l1 = genLine(X[0],X[1])
    if(abs(getAngle(genLine(mid1,mid2)[0],l1[0])) < 2):
        return True
    else:
        return False

slopetol = 5
pixtol = 30
reach = 2
count = 0

toval = []
totest = []

for i in uniques:
    if(count %2000 == 0):
        print(count)
    count +=1


    with open(path + '/' + i) as json_file:
        data = json.load(json_file)
        filename = i.replace('json','png')
        lines = []
        line_color = (100, 50, 0)
        for i in data['lanes']:
            templine = []
            for j in i['markers']:
                first = [float(j['pixel_start']['x']),float(j['pixel_start']['y'])]
                second = [float(j['pixel_end']['x']),float(j['pixel_end']['y'])]
                if(first == second):
                    continue
                templine.append([first,second])
            index = 0
            while(index < len(templine)):
                compareline = templine[index]
                l = genLine(templine[index][0],templine[index][1])
                rang = getRange(index,reach,templine)
                checklines = []
                for index2 in range(rang[0],rang[1]):
                    if(index2 != index and getAngle(genLine(templine[index2][0],templine[index2][1])[0],l[0]) < slopetol and calcDist(getMidpoint(compareline[0],compareline[1]),getMidpoint(templine[index2][0],templine[index2][1])) < pixtol and isOnSameLine(compareline,templine[index2]) == False ):
                        checklines.append([templine[index2], index2])
                maxLength = calcDist(compareline[0],compareline[1])
                maxindex = index
                for line in checklines:
                    length = calcDist(line[0][0],line[0][1])
                    if(length > maxLength):
                        maxindex = line[1]
                        maxLength = length
                popped = []
                for line in checklines:
                    if(line[1] != maxindex):
                        alter = getAlter(popped,line[1])
                        templine.pop(line[1]-alter)
                        popped.append(line[1])

                if(index != maxindex):
                    alter = getAlter(popped, index)
                    templine.pop(index-alter)
                index += 1


            lines = lines + templine
        edges_pos = []
        edges_neg = []
        juncs = []
        for lin in lines:
            if(lin[0] not in juncs):
                juncs.append(lin[0])
            if(lin[1] not in juncs):
                juncs.append(lin[1])

        for line in lines:
            edges_pos.append([juncs.index(line[0]), juncs.index(line[1])])
        if(count % 6 != 0):
            for i in range(len(juncs)):
                for j in range(i+1, len(juncs)):
                    add = [i,j]
                    if(add not in edges_pos):
                        edges_neg.append(add)
        im2 = cv2.imread(path + '/' + filename)
        width = im2.shape[0]
        height = im2.shape[1]
        obj = {}
        obj["height"] = height
        obj["width"] = width
        obj["edges_positive"] = edges_pos
        obj["edges_negative"] = edges_neg
        obj["filename"] = filename
        obj["junctions"] = juncs
        if(count % 6 != 1 and count % 6 != 0):
            tofile.append(obj)
        elif(count % 6 == 1):
            toval.append(obj)
        elif(count % 6 == 0):
            totest.append(obj)

totest_real = []
for test in totest:
    newobj = {}
    newobj["height"] = test["height"]
    newobj["width"] = test["width"]
    newlines = []
    juncs = test["junctions"]
    for line in test["edges_positive"]:
        point1 = juncs[line[0]]
        point2 = juncs[line[1]]
        newlines.append([point1[0],point1[1],point2[0],point2[1]])
    newobj["lines"] = newlines
    newobj["filename"] = test["filename"]
    newobj["junc"] = juncs
    totest_real.append(newobj)

with open('val.json', 'w') as f:
    json.dump(toval, f)
with open('test.json', 'w') as f:
    json.dump(totest_real, f)
with open('train.json', 'w') as f:
    json.dump(tofile, f)