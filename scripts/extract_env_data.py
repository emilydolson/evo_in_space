import avidaspatial as avsp
import sys

env = avsp.parse_environment_file(sys.argv[1], (60,60))

resources = ["not", "nand", "and", "orn", "or", "andn", "nor", "xor"]

print "x, y,count," + ",".join(resources)

for y in range(len(env.grid)):
    for x in range(len(env.grid[y])):
        count = len(env.grid[y][x])
        output = [x, y, count]
        for res in resources:
            dist = 0
            curr = env.grid[y][x]
            while res not in curr and dist < 60:
                dist += 1
                for i in range(-dist, dist):
                    for j in range(-dist, dist):
                        yval = y+i
                        xval = x+j
                        if yval < 0 or yval > 58 or xval < 0 or xval > 58:
                            continue
                        curr = curr.union(env.grid[yval][xval])
 
            output.append(dist)

        print ",".join([str(el) for el in output])
