import glob
import avidaspatial as avsp

import re

def atoi(text):
    # From http://stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inside
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    From http://stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inside
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split('(\d+)', text) ]

def main():
    files = glob.glob("grid_task.*.dat")
    files.sort(key=natural_keys)

    relevant_bits = list(range(1,10))
    firsts = {}

    for filename in files:
        #print filename
        data = avsp.agg_grid(avsp.load_grid_data(filename))
        for y in range(len(data)):
            for x in range(len(data[y])):
                if data[y][x][0] == "-":
                    data[y][x] = ""
                for bit in relevant_bits:
                    if len(data[y][x])-2 < bit:
                        continue

                    if int(data[y][x][-bit]):

                        update = "".join([s for s in filename if s.isdigit()])
                        firsts[bit] = (x,y,update)
                        relevant_bits.remove(bit)
        if not relevant_bits:
            break

    outfile = open("task_locs.csv", "w")
    for key in firsts:
        outfile.write(",".join([str(key), str(firsts[key][0]), str(firsts[key][1]), firsts[key][2]])+"\n")
    
    outfile.close()

main()
