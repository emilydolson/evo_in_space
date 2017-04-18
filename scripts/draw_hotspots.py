from avidaspatial import *
from patch_analysis import *
import sys
import shapely as shp
from shapely.geometry import MultiPoint
from descartes.patch import PolygonPatch
import pandas as pd

df = pd.read_csv("all_task_locs.csv")

env_id = sys.argv[1]

task_id=0
if len(sys.argv) > 2:
    task_id = int(sys.argv[2])

draw_points = "hotspots"
if len(sys.argv) > 3:
    draw_points = sys.argv[3]

env = parse_environment_file("../config/env"+env_id+".cfg", (60,60))

env = convert_world_to_phenotype(env)
env.grid, n = assign_ranks_by_cluster(env.grid, 100)

#length = get_pallete_length(hotspots)
#palette = sns.hls_palette(length, s=1)
#env.task_palette = palette
#print(len(env.task_palette))
#print(len(env.resource_palette))
env.resource_palette = sns.hls_palette(n, s=1, l=.5)
#env.resource_palette = [[0,0,0]] + env.resource_palette
env.task_palette = [(0,0,0), (0,0,0)]
print(n)
#paired_environment_phenotype_grid(env, hotspots, palette=env.task_palette)
plot_world(env, palette=env.resource_palette)
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())

ax = plt.gca()


colors = ["black", "black", "red", "pink", "yellow", "green", "cyan", "black", "white"] #["black", "black"] + sns.color_palette("husl", 7)#["black", "red", "orange", "yellow", "green", "cyan", "blue", "magenta", "white"]
print(colors)
ids = list(range(9,4,-1))
if task_id != 0:
    ids = [task_id]

patch_handles = []

if draw_points == "hotspots":
    for task_id in ids:

        hotspots = load_grid_data(str(task_id)+"_"+env_id+"_hotspots.csv", "int", delim=",")
        hotspots = agg_grid(hotspots, mode)

        ones = []

        for y in range(len(hotspots)):
            for x in range(len(hotspots[y])):
                if hotspots[y][x] == 0:
                    hotspots[y][x] = -1
                else:
                    ones.append((x,y))

        patches = traverse_core(ones, 60)


        to_remove = []
        for i in range(len(patches)):
            if len(patches[i]) < 30:
                to_remove.append(i)
                continue
            patches[i] = MultiPoint(patches[i])

        for i in reversed(to_remove):
            patches.pop(i)

        patch = 0
        for p in patches:
            if p.convex_hull.geom_type == "Polygon":
                data = p.convex_hull

            else: #p.convex_hull.geom_type == "LineString":
                data = p.convex_hull.buffer(.5)

            patch = PolygonPatch(data, facecolor='white', lw=3, edgecolor=colors[task_id-1], alpha=1, fill=False, zorder=2, label=task_id)

            ax.add_patch(patch)
            patch_handles.append(patch)

elif draw_points == "points":
    points = df[df.task == int(task_id)][df.environment == int(env_id)]

    plt.plot(points.x, points.y, ".", color=colors[task_id-1])

elif draw_points == "paths":
    pathfile = open("paths_"+str(task_id-1)+"_"+str(env_id)+".dat")
    lines = pathfile.readlines()[10:15]

    colors = sns.color_palette("bone", len(lines))
    for i,line in enumerate(lines):
        nums = eval(line.strip())
        (xs, ys) = zip(*nums)
        ax.add_line(plt.Line2D(xs, ys, linewidth=2, color=colors[i]))

    pathfile.close()
#plt.show()

name = "all" if len(ids)>1 else str(task_id)
name += "_" + draw_points

#legend = plt.legend(handles = patch_handles, bbox_to_anchor=(0.5, -0.01),
#                    loc=9, borderaxespad=0., frameon=True, ncol=9)
#legend.get_frame().set_facecolor('lightgrey')
plt.savefig(str(env_id)+"_" + name+".png", bbox_inches = 'tight', pad_inches = 0)
