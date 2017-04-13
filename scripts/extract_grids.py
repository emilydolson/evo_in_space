import shutil
import sys

updates = []
loc_file = open("task_locs.csv")
for line in loc_file:
    if line.strip() == "":
        continue
    updates.append(int(line.split(",")[3]))
loc_file.close()
updates.sort()

for update in updates:
    shutil.copy("grid_task."+str(update)+".dat*", sys.argv[1])
