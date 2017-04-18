from avidaspatial import *
import matplotlib.pyplot as plt
import seaborn as sns

updates = []
locs = []
loc_file = open("task_locs.csv")
for line in loc_file:
    if line.strip() == "":
        continue
    sline = line.split(",")
    updates.append(int(sline[3]))
    locs.append([int(sline[1]), int(sline[2])])
loc_file.close()

sns.set_style("whitegrid", {'axes.grid' : False})

for i,update in enumerate(updates):
    fig = plt.figure()
    world = load_grid_data("data/grid_task."+str(update-1)+".dat")
    world = agg_grid(world, mode)

    data = diversity_map(world, neighbor_func=get_25_neighbors)
    pal = sns.color_palette("bone")
    pal.reverse()
    denom = 4.64
    grid = color_grid(data, pal, denom, False)

    plt.tick_params(labelbottom="off", labeltop="off", labelleft="off",
                    labelright="off", bottom="off", top="off", left="off",
                    right="off")
    plt.imshow(grid)
    plt.tight_layout()

    plt.plot([locs[i][0]], [locs[i][1]], "o", color="green")
    plt.savefig("task_"+str(i)+"_diversity.png", dpi=500, bbox_inches="tight")
