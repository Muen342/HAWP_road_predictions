f = open("outputs/hawp/last_checkpoint", "r")
num = f.read()[-6:-4]
print(num)
num = int(num) - 1
if(num < 10 and num > 0):
    final = "outputs/hawp/model_0000" + str(num) + ".pth"
else:
    final = "outputs/hawp/model_000" + str(num) + ".pth"
print(final)
f = open("outputs/hawp/last_checkpoint", "w")
f.write(final)
f.close()