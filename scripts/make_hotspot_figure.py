from avidaspatial import *
from patch_analysis import *
import sys
import shapely as shp
from shapely.geometry import MultiPoint
from descartes.patch import PolygonPatch
import pandas as pd
from collections import OrderedDict
plt.rcParams["figure.figsize"] = (16,8.5)
df = pd.read_csv("../analyze/all_task_locs.csv")

env_ids = [50013, 50047, 50048, 50060, 50061, 50062, 50063, 50065]
task_list = ["NOT", "NAND", "AND", "ORN", "OR", "ANDN", "NOR", "XOR", "EQU"]

task_id=0
if len(sys.argv) > 2:
    task_id = int(sys.argv[2])

draw_points = "hotspots"
if len(sys.argv) > 3:
    draw_points = sys.argv[3]

envs = parse_environment_file_list(["../config/env"+str(env_id)+".cfg" for env_id in env_ids], (60,60))


envs = [convert_world_to_phenotype(env) for env in envs]

for env in envs:
    env.grid, n = assign_ranks_by_cluster(env.grid, 100)

    #length = get_pallete_length(hotspots)
    #palette = sns.hls_palette(length, s=1)
    #env.task_palette = palette
    #print(len(env.task_palette))
    #print(len(env.resource_palette))
    env.resource_palette = sns.hls_palette(n, s=1, l=.5)
    #env.resource_palette = [[0,0,0]] + env.resource_palette
    env.task_palette = [(0,0,0), (0,0,0)]

linestyles = ["-", "--", "-", "-", "-", ":", "-", "--","--"]
letters = ["A", "B", "C", "D","E", "F","G","H","I"]
ids = list(range(9,0,-1))
if task_id != 0:
    ids = [task_id]

plt.Figure()

colors = ["red", "yellow", "green", "turquoise", "orange", "blue", "pink", "black", "white"]#["black", "red", "orange", "yellow", "green", "cyan", "blue", "magenta", "white"]
patch_handles = []
for fig_num in range(1,9):
    plt.subplot(2, 4, fig_num)

    #paired_environment_phenotype_grid(env, hotspots, palette=env.task_palette)
    plot_world(envs[fig_num-1], palette=envs[fig_num-1].resource_palette)


    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())

    ax = plt.gca()

    if draw_points == "hotspots":
        for task_id in ids:

            hotspots = load_grid_data("../analyze/"+str(task_id) + "_" + str(env_ids[fig_num-1]) + "_hotspots.csv", "int", delim=",")
            hotspots = agg_grid(hotspots, mode)

            ones = []

            for y in range(len(hotspots)):
                for x in range(len(hotspots[y])):
                    if hotspots[y][x] == 0:
                        hotspots[y][x] = -1
                    else:
                        ones.append((x,y))

            patches = traverse_core(ones, world_size=(60,60))

            for i in range(len(patches)):
                patches[i] = MultiPoint(patches[i])

            patch = 0
            for p in patches:

                if p.convex_hull.geom_type == "Polygon":
                    data = p.convex_hull

                else: #p.convex_hull.geom_type == "LineString":
                    data = p.convex_hull.buffer(.5)
                print(task_list[task_id-1], p, p.convex_hull.geom_type)
                patch = PolygonPatch(data, facecolor='white', lw=2, ls=linestyles[task_id-1], edgecolor=colors[task_id-1], alpha=1, fill=False, zorder=2, label=task_id-1)

                ax.add_patch(patch)
                ax.text(0.02, 0.98, letters[fig_num-1], transform=ax.transAxes,fontsize=20, va='top')

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

# From ectamur's answer to
# http://stackoverflow.com/questions/13588920/stop-matplotlib-repeating-labels-in-legend
patch_handles.sort(key=lambda x:int(x.get_label()))

labels = [task_list[int(h.get_label())] for h in patch_handles]
by_label = OrderedDict(zip(labels, patch_handles))

legend = plt.legend(by_label.values(), by_label.keys(),
                    bbox_to_anchor=(0, 0, 1, 1), bbox_transform=plt.gcf().transFigure,
                    loc="lower center", borderaxespad=0., frameon=True, ncol=9)
legend.get_frame().set_facecolor('lightgrey')
plt.tight_layout()
plt.savefig("../figs"+str(env_id)+"_" + name+".png", bbox_inches = 'tight', pad_inches = 0)
