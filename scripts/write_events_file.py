updates = []
loc_file = open("task_locs.csv")
for line in loc_file:
    if line.strip() == "":
        continue
    updates.append(int(line.split(",")[3]))
loc_file.close()
updates.sort()

event_file = open("hotspot-events.cfg", "w")
event_file.write("u begin Inject default-heads.org\n")

for update in updates:
    event_file.write("u " + str(update-1) + " DumpTaskGrid\n")

event_file.write("u " + str(updates[-1]) + " Exit\n")
event_file.close()
