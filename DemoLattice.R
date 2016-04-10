# Building the Lattice plot to demo what this will look like
# This seems like hard coding, but remember what you need to do
# You have to split out the different variables
# then you need to rbind the variables you want on every facet to the 
# variables that will have their own facet.
# then you rbind the whole thing and run it through ggplot with a facet_wrap
hNeed <- filter(hDat, variable=='Need'& Run == 0)
hPerf <- filter(hDat, variable=='Performance' & Run == 0)
hRes <- filter(hDat, variable != 'Performance' & variable != 'Need' & Run == 0)
hIR <- filter(hDat, variable == 'IntegralResilience' & Run == 0)
hQR <- filter(hDat, variable == 'QuotientResilience' & Run == 0)
hRF <- filter(hDat, variable == 'ResilienceFactor' & Run == 0)
hNS <- filter(hDat, variable == 'IntegralResilienceNoSubstitution' & Run == 0)
h0 <- filter(hDat, Run == 0)
need <- hNeed$value[1]
perf <- distinct(select(hPerf, value))
perfT <- c(0, 15, 15, 78, 78, 99)
perfV <- c(1.2, 1.2, .082, .082, 1.03, 1.03)
performance <- data.frame(perfT, perfV)
colnames(performance) <- c('Time', 'value')
IR <- rbind(hIR, hPerf, hNeed)
QR <- rbind(hQR, hPerf, hNeed)
RF <- rbind(hRF, hPerf, hNeed)
NS <- rbind(hNS, hPerf, hNeed)
IR$face <- 'Integral Resilience'
QR$face <- 'Quotient Resilience'
RF$face <- 'Resilience Factor'
NS$face <- 'Integral Resilience No Substitution'
Res <- rbind(IR, QR, RF, NS)
f <- ggplot(aes(Res$Time, Res$value), data=Res)
f <- f + geom_line(aes(color=variable))  + xlab("Time Horizon") + ylab("Performance Value")
f <- f + facet_wrap(~ face, nrow = 2, ncol = 2)