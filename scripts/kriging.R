library(spatstat)
library(gstat)
library(spdep)
# library(rgdal)

data <- read.csv("~/geo866/evo_in_space/data/all_task_locs.csv")
envs <- unique(data$environment)
all_resources <- data.frame(x=double(), y=double(), count=integer(), not=integer(), nand=integer(), and=integer(), orn=integer(), or=integer(), andn=integer(), nor=integer(), xor=integer(), equ=integer(), env="", density=double())
all_resources <- data.frame()
i <- 1
for (env in envs){
  env_data <- subset(data, data$environment == env)
  env_data_ppp <- ppp(env_data$x, env_data$y, c(0,60), c(0,60))
  env_density <- density(env_data_ppp, bw=3, eps=1)
  env_density$v <- env_density$v/sum(env_density$v)
  resources <- read.csv(paste0("env",env,".csv", sep=""))
  density <- vector("numeric", 60*60)

  for (line in 1:length(resources$x)) {
    density[line] <- env_density$v[resources$x[line]+1,resources$y[line]+1]
  }
  resources$density <- density
  #resources$x <- resources$x+(i+59)
  #resources$y <- resources$y+(i+59)
  resources$env <- env
  i <- i+1
  all_resources <- rbind(all_resources, resources)
}
  spatial_data <- remove.duplicates(SpatialPointsDataFrame(data.frame(all_resources$x, all_resources$y), all_resources))
  #print(env)
  # res_lm <- lm(density~ (not==0) + (nand==0) + (and==0) + (or==0) + (nor==0) + (xor==0) + (andn==0) + (orn==0), data=resources)
  # print(summary(res_lm))
  res_lm <- lm(density~ not + nand + and + or + nor + xor + andn + orn, data=resources)
  
  #res_lm <- lm(density~ log(1+not) + log(1+nand) + log(1+and) + log(1+or) + log(1+nor) + log(1+xor) + log(1+andn) + log(1+orn), data=resources)
  
  print(summary(res_lm))
  # vario <- variogram(density~not+nand+and+or+xor, spatial_data)
  # plot(vario)
  # mod <- vgm(nugget=.00001, range=35, model="Sph", psill = 5.5e-04)
  # plot(vario, model=mod)

  #grid <- data.frame(1:59, 1:59)
  #grid <- SpatialGrid(GridTopology(c(0,0), c(1,1), c(59,59)))
  # resources <- SpatialPointsDataFrame(data.frame(resources$x, resources$y), resources)
  # krige_results <- krige(density~not+nand+and+or+xor, spatial_data, resources, model=mod)
  # spplot(krige_results['var1.pred'], col.regions=colorRampPalette(c('deepskyblue', "white", 'yellow', 'orangered'))(20))
  # not <- subset(resources, xor==1)
  # plot(density(ppp(not$x, not$y, c(0,59), c(0,59)), bw=3))

  adj <- matrix(ncol=59*59, nrow=59*59, 0)

  for (x in 1:59**2) {
    adj[x,x] <- 1
    left <- x-1
    right <- x + 1
    up <- x - 59
    down <- x + 59
  
    ul <- up - 1
    dl <- down -1
    ur <- up + 1
    dr <- down +1
    
    if (left %% 59 == 0) {
      left <- left + 59
      dl <- dl + 59
      ul <- ul - 59
    }

    if (right %% 59 == 1){
      right <- right - 59
      dr <- dr - 59
      ur <- ur - 59
    }
  
    if (up < 1) {
      up <- (59**2) + up
      ul <- (59**2) +ul
      ur <- (59**2) +ur
    }
  
    if (down > 59**2) {
      down <- down - 59**2
      dl <- dl - 59**2
      dr <- dr - 59**2
    }

    adj[x,left] <- 1
    adj[x, right] <- 1
    adj[x, up] <- 1
    adj[x, down] <- 1
    adj[x, dl] <- 1
    adj[x, dr] <- 1
    adj[x, ul] <- 1
    adj[x, ur] <- 1
  }

  # zeros <- matrix(ncol=3481, nrow=3481, 0)
  # full_adj <- adj
  # full_adj <- cbind(adj, zeros)
  # full_adj <- rbind(full_adj, cbind(zeros, adj))
  # for (i in 3:length(envs)) {
  #   new_row <- zeros
  #   new_col <- zeros
  #   for (j in 1:(i-2)) {
  #     # print(i)
  #     # print(j)
  #     # print(dim(new_col))
  #     # print(dim(new_row))
  #     # print("looping")
  #     new_row <- cbind(new_row, zeros)
  #     new_col <- rbind(new_col, zeros)
  #   }
  #   full_adj <- cbind(full_adj, new_col)
  #   new_row <- cbind(new_row, adj)
  #   full_adj <- rbind(full_adj, new_row)
  # }

  splm <- spautolm(density~not + nand + and + or + nor + xor + andn + orn, data=resources, listw=mat2listw(adj))
  print(summary(splm))
  print(cor(splm$fit$signal_trend, resources$density))
  plot(splm$fit$signal_trend, resources$density, xlab="SAR Trend", ylab="Density")
  plot(splm$fit$fitted.values, resources$density, xlab="SAR Fitted Values", ylab="Density")
}