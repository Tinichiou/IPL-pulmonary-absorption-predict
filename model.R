#讀入model和參數
#傳入參數到R
args = commandArgs(trailingOnly=TRUE)

et <- readRDS("mtmodel.rds")
load("feature_minmax.Rdata")
library(extraTrees)

inputdata <- read.csv( paste0('./tmp/',args[1]), fileEncoding = "UTF-8-BOM")   #args[1]是padel.csv
len <- nrow(inputdata)
inputdata <- inputdata[,c("Name",feature)]

y.nhat = predict(et, inputdata[,feature], newtasks=rep(1,len))
#inputdata$y.nhat <- y.nhat

yhat_logka = (y.nhat*(max1-min1))+min1
inputdata$predicted_ka <- 10^(yhat_logka)
inputdata$absorption_halftime <- 0.693/(inputdata$predicted_ka)

#輸出檔案
colnames(inputdata)[1] <- "input order"
write.table(inputdata, paste0('./tmp/', args[2]), sep=',', row.names=FALSE, col.names=TRUE, quote=TRUE, na='NA', append=FALSE) #args[2]是output.csv


