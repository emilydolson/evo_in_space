import glob


outfile = open("all_task_locs.csv", "w")
outfile.write("task,x,y,update,rep,environment\n")
files = glob.glob("*/task_locs.csv")
for filename in files:
    env = filename.split("/")[-2].split("_")[1]
    rep = filename.split("/")[-2].split("_")[-1]
    infile = open(filename)
    for line in infile.readlines():
        outfile.write(line.strip() + "," + rep + "," + env + "\n")

outfile.close()
