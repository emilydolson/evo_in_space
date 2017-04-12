import glob
from avidaspatial import *
import random
import scipy.stats

dir_list = glob.glob("env_*_1*")

data = ["env, ud, task, x, y, div, rank"]

for dir_name in dir_list:
    env_num = dir_name.split("_")[-2]
    task_loc_file = open(dir_name + "/task_locs.csv")
    task_locs = task_loc_file.readlines()
    task_loc_file.close()

    task_dict = {}
    for line in task_locs:
        sline = line.split(",")
        task_dict[int(sline[3])] = [int(i) for i in sline[:3]]

    envs = parse_environment_file_list(glob.glob(dir_name+"/data/grid_task.*.dat"), (60, 60))

    for env in envs:
        ud = int(env.name.split(".")[-1])
        env = agg_grid(env, mode)
        div_map = diversity_map(env)
        task = task_dict[ud+1]
        div = div_map[task[2]][task[1]]
        rank = scipy.stats.percentileofscore(flatten_array(div_map), div)

        data.append(",".join([str(i) for i in [env_num, ud, task[0], taxk[1], task[2], div, rank]]))

outfile = open("diversity_ranks.csv")
outfile.write("\n".join(data))
outfile.close()
