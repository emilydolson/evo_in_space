import glob
import sys

num = sys.argv[1]
env = sys.argv[2]

filenames = glob.glob("*env*/lineage_locs_"+num+".dat")

outfile = open("paths_"+num+"_"+env+".dat", "w")

for name in filenames:
    infile = open(name)
    path = infile.readline().split()[1:-1]
    infile.close()
    path = [int(i) for i in path]
    path = [[i%60, i//60] for i in path]
    outfile.write(str(path) + "\n")

outfile.close()
