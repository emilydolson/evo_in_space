import glob
import sys
import avidaspatial

num = sys.argv[1]
env = sys.argv[2]

filenames = glob.glob("*"+env+"*/lineage_locs_"+num+".dat")

env = parse_environment_file("../config/env"+env+".cfg", (60, 60))

outfile = open("paths_"+num+"_"+env+".dat", "w")
outfile_env = open("env_seq_"+num+"_"+env+".dat", "w")

for name in filenames:
    infile = open(name)
    path = infile.readline().split()[1:-1]
    infile.close()
    path = [int(i) for i in path]
    path = [[i % 60, i // 60] for i in path]
    outfile.write(str(path) + "\n")
    env_seq = []
    for loc in path:
        env_seq.append(sorted(list(env[loc[1]][loc[0]])))

    outfile_env.write(",".join([str{i} for i in env_seq]) + "\n")

outfile.close()
outfile_env.close()
