#Rename CSV so it can be accessed easily 
data<-read.csv("all_task_locs.csv")

#Select a task to start with 
task2<-subset(data, data$task==2)

#Create point pattern object for the data
library(spatstat)
task2PP<-ppp(task2$x, task2$y, c(0,58), c(0,58))
plot(task2PP)

#Kernel Density of point pattern 
bw=3
task2.density<-density(task2PP, sigma=bw)
plot(task2.density, col=heat.colors(10))
axis(1)

#Create grid to run simulations in 
uniformgrid<-rsyst(win=c(0,58,0,58), dx=1, dy=1)

#Establishing some matrices, variables, etc.
num.sims<-1000
cutoff<-0.95*num.sims
simulations<-vector("list", num.sims)
max.values<-vector("numeric", num.sims)


#Loop to remove random points and simulate new kernel density grids with 23 points 100 times
#storing each simulation point pattern/kernel map, as well as max value from each density function
for(i in 1:num.sims) {
  remove<-sample(1:59**2, 23) #number of points to remove from grid
  simulations[[i]]<-density(subset.ppp(uniformgrid, remove),bw)
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
    if(locations[x,y]<task2.density$v[x,y]) {
      hotspots[x,y]<-1
      }
    }  
}




