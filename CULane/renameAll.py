import os
# function that filters vowels
def FilterFiles(name):
    if('lines' in name):
        return True
    else:
        return False
def main():
    path = "./temp"
    count = 1

    for root, dirs, files in os.walk(path):
        uniques = filter(FilterFiles, files)
        for i in uniques:
            pic = i.replace('lines.txt', 'jpg')
            count += 1
            os.rename(os.path.join(root, i), os.path.join(root, str(count) + ".lines.txt"))
            os.rename(os.path.join(root, pic), os.path.join(root, str(count) + ".jpg"))


if __name__ == '__main__':
    
    main()
   