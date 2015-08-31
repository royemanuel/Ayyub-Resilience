# This is my first attempt at puttin together Bilal's metric.
# Compute the anti-resilience metric for a step function
AntiResSF <- function(t.hor, t.rec, q.pri, q.rec){
    (t.rec) * (q.pri - q.rec) / (q.pri * t.hor)
}
# Linear recovery anti-resilience
AntiResLR <- function(t.hor, t.rec, q.pri, q.rec){
    (t.rec) * (q.pri - q.rec) / (2 *(q.pri * t.hor))
}
# Compute the resilience metric with step recovery
ResilienceStep <- function(lambda, p.fail, t.hor, t.rec, q.pri, q.rec){
    1 - exp(- lambda * t.hor * (1 - p.fail *
                                    AntiResSF(t.hor, t.rec,
                                              q.pri, q.rec))) +
                                                  exp(- lambda * t.hor)
}
# Resilience using linear recovery
ResilienceLinear <- function(lambda, p.fail, t.hor, t.rec, q.pri, q.rec){
    1 - exp(- lambda * t.hor * (1 - p.fail *
                                    AntiResLR(t.hor, t.rec,
                                              q.pri, q.rec))) +
                                                  exp(- lambda * t.hor)
}
ResilienceTLone <- function(lambda, p.fail, t.hor, t.rec, q.pri, q.rec){
    1 - exp(- (1 - p.fail *
                   AntiResLR(t.hor, t.inc, t.rec,
                             q.pri, q.rec))) +
                                 exp(- 1)
}
# Attempt at a plot of the Resilience as the difference between
                                        # t.inc and t.rec grows
# res.plot <- ggplot(data.frame(x=c(0, 8)), aes(x)) +
#     stat_function(fun=function(x)ResilienceLinear(lambda=.25, t.hor=4,
#                      p.fail=.1, t.rec=x, q.pri=1, q.rec=0.75),
#                  geom="line", aes(color="0.1")) +
#    stat_function(fun=function(x)ResilienceLinear(lambda=.25, t.hor=4,
#                      p.fail=.25, t.rec=x, q.pri=1, q.rec=0.75),
#                  geom="line", aes(color="0.25")) +
#    stat_function(fun=function(x)ResilienceLinear(lambda=.25, t.hor=4,
#                      p.fail=.5, t.rec=x, q.pri=1, q.rec=0.75),
#                  geom="line", aes(color="0.5")) +
#    scale_color_manual("Values of p", values=c("0.1" = "blue", "0.25" = "red",
#                                                          "0.5" = "green"))
#res.plot
