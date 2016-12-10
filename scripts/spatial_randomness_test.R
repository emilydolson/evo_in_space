library(spatstat)

#Rename CSV so it can be accessed easily 
data<-read.csv("all_task_locs.csv")

#Function to process all point patterns:

process.patterns <- function(task.num, env, bw=3, num.sims=10) {

  task<-subset(data, data$task==task.num & data$environment == env)
  
  #Create point pattern object for the data
  taskPP<-ppp(task$x, task$y, c(0,59), c(0,59))
  png(paste0(c(task.num, env, "points.png"), collapse="_"))
  plot(taskPP, main=paste0(c("Task ", task.num, ", Environment: ", env), collapse = ""))
  dev.off()
  
  #Kernel Density of point pattern 
  task.density<-density(taskPP, sigma=bw)
  png(paste0(c(task.num, env, "density.png"), collapse="_"))
  plot(task.density, col=heat.colors(10), main=paste0(c("Task ", task.num, ", Environment: ", env), collapse = ""))
  dev.off()
  
  #Create grid to run simulations in 
  uniformgrid<-rsyst(win=c(0,59,0,59), dx=1, dy=1)
  
  #Establishing some matrices, variables, etc.
  cutoff<-0.95*num.sims
  simulations<-vector("list", num.sims)
  max.values<-vector("numeric", num.sims)

  #Loop to remove random points and simulate new kernel density grids with 23 points 100 times
  #storing each simulation point pattern/kernel map, as well as max value from each density function
  for(i in 1:num.sims) {
    remove<-sample(1:59**2, length(task$x)) #number of points to keep from grid
    simulations[[i]]<-density(subset.ppp(uniformgrid, remove), bw)
    max.values[[i]]<-max(simulations[[i]])
  }
  
  #Matrix that mimics actual environment grid to place results into
  locations<-matrix(nrow=59, ncol=59)
  
  #Loop to put sorted 95% confidence values for each location for all the simulations into locations matrix
  for(x in 1:59) {
    for(y in 1:59) {
      location.values<-vector("numeric", num.sims) 
      for(i in 1:num.sims) {
        location.values[[i]]<-simulations[[i]]$v[x,y]
      }
      sorted.values<-sort(location.values)
      locations[x,y]<-sorted.values[cutoff]
    }
  }
  
  #Matrix that will define differences between simulations and empirical data
  hotspots<-matrix(0,nrow=59, ncol=59)
  
  #Loop to differentiate high test values from simulated data in each location to find "significant" areas of evolution
  for(x in 1:59) {
    for(y in 1:59) {
      if(locations[x,y]<task.density$v[x,y]) {
        hotspots[x,y]<-1
        }
      }  
  }
  
  png(paste0(c(task.num, env, "hotspots.png"), collapse="_"))
  image(hotspots, main=paste0(c("Task ", task.num, ", Environment: ", env), collapse = ""))
  dev.off()
  
  write.table(hotspots, file = paste0(c(task.num, env, "hotspots.csv"), collapse="_"), row.names = FALSE, col.names = FALSE, sep=",")
}

for (task in unique(data$task)) {
  for (environment in unique(data$environment)) {
    print(task)
    print(environment)
    process.patterns(task, environment, num.sims = 1000)
  }
}
