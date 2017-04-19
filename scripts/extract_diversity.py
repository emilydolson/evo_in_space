import glob
from avidaspatial import *
import random
import scipy.stats
import os
import sys

dir_list = glob.glob(sys.argv[1])

outname = "diversity_ranks.csv"
if len(sys.argv) > 2:
    outname = sys.argv[2]

data = ["env, ud, task, x, y, div, rank"]

for dir_name in dir_list:
    env_num = dir_name.split("_")[-2]
    
    if not os.path.exists(dir_name + "/task_locs.csv"):
        continue

    task_loc_file = open(dir_name + "/task_locs.csv")
    task_locs = task_loc_file.readlines()
    task_loc_file.close()

    task_dict = {}
    for line in task_locs:
        sline = line.split(",")
        task_dict[int(sline[3])] = [int(i) for i in sline[:3]]

    grids = glob.glob(dir_name+"/data/grid_task.*.dat")

    for j in range(len(grids)):
        
        ud = int(grids[j].split(".")[-2])
        if ud+1 not in task_dict:
            continue
        env = load_grid_data(grids[j])
        env = agg_grid(env, mode)
        div_map = diversity_map(env, neighbor_func=get_25_neighbors)
        task = task_dict[ud+1]

        div = div_map[task[2]][task[1]]
        rank = scipy.stats.percentileofscore(flatten_array(div_map), div, kind="strict")
        print(rank)
        data.append(",".join([str(i) for i in [env_num, ud, task[0], task[1], task[2], div, rank]]))

outfile = open(outname, "w")
outfile.write("\n".join(data))
outfile.close()
