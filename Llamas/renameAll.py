import os
# function that filters vowels
def FilterFiles(name):
    if('json' in name):
        return True
    else:
        return False
def main():
    path = "./data/wireframe/images/color_images/train"
    count = 1

    for root, dirs, files in os.walk(path):
        uniques = filter(FilterFiles, files)
        for i in uniques:
            pic = i.replace('.json', '_color_rect.png')
            count += 1
            os.rename(os.path.join(root, i), os.path.join(root, str(count) + ".json"))
            os.rename(os.path.join(root, pic), os.path.join(root, str(count) + ".png"))


if __name__ == '__main__':
    
    main()
   