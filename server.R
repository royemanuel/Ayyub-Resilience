# server.R
library(shiny)
library(ggplot2)
# This is my first attempt at putting together Bilal's metric.
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
    1 - exp(- lambda / 100 * t.hor * (1 - p.fail *
                                    AntiResSF(t.hor, t.rec,
                                              q.pri, q.rec))) +
                                                  exp(- lambda / 100* t.hor)
}
# Resilience using linear recovery
ResilienceLinear <- function(lambda, p.fail, t.hor, t.rec, q.pri, q.rec){
    1 - exp(- lambda / 100* t.hor * (1 - p.fail *
                                    AntiResLR(t.hor, t.rec,
                                              q.pri, q.rec))) +
                                                  exp(- lambda / 100 * t.hor)
}
shinyServer(function(input, output){
    output$res.v.recovery <- renderPlot({
        if (input$recType == "lin"){
            p <- ggplot(data.frame(x=c(0, input$t.rec)), aes(x)) +
                stat_function(fun=function(x)ResilienceLinear(lambda=input$lambda,
                                  p.fail=input$p.fail, t.hor=input$t.hor,
                                  t.rec=x, q.pri=input$q.pri,
                                  q.rec=input$q.rec))
        } else {
            p <- ggplot(data.frame(x=c(0, input$t.rec)), aes(x)) +
                stat_function(fun=function(x)ResilienceStep(lambda=input$lambda,
                                  p.fail=input$p.fail, t.hor=input$t.hor,
                                  t.rec=x, q.pri=input$q.pri,
                                  q.rec=input$q.rec))
        }
        p <- p + scale_x_continuous("Recovery Time") +
            scale_y_continuous("Resilience")
#       p <- p # + annotate("text", x=1, y=c(.98, .975, .970, .965,
#                                          .960, .955),
#                         label=c(paste("Time Horizon =", input$t.hor),
#                             paste("Lambda =", input$lambda),
#                             paste("Failure Probability =", input$p.fail),
#                             paste("Nominal Performance = ",
#                                   100*input$q.pri, "%"),
#                             paste("Failure Performance =",
#                                   100*input$q.rec, "%"),
#                             paste("Recovery Profile =",
#                                   ifelse(input$recType == "lin",
#                                          "Linear", "Step"))))
        print(p)
    })
    output$res.v.prob <- renderPlot({
        if (input$recType == "lin"){
            q <- ggplot(data.frame(x=c(0.01, 1)), aes(x)) +
                stat_function(fun=function(x)ResilienceLinear(lambda=input$lambda,
                                  p.fail=x, t.hor=input$t.hor,
                                  t.rec=input$t.rec, q.pri=input$q.pri,
                                  q.rec=input$q.rec))
        } else {
            q <- ggplot(data.frame(x=c(0.01, 1)), aes(x)) +
                stat_function(fun=function(x)ResilienceStep(lambda=input$lambda,
                                  p.fail=x, t.hor=input$t.hor,
                                  t.rec=input$t.rec, q.pri=input$q.pri,
                                  q.rec=input$q.rec))
        }
        q <- q + scale_x_continuous("Probability", limits=c(.01,1)) +
            coord_trans(xtrans = "log10")
            print(q)

    })
#   output$res.v.ratio <- renderPlot({
#       if (input$recType == "lin"){
#           m <- ggplot(data.frame(x=c(0,100),y=c(0,1)), aes(x * y)) +
#               stat_function(fun=function(x)ResilienceLinear(lambda=y,
#                                 p.fail=input$p.fail, t.hor=x,
#                                 t.rec=input$t.rec, q.pri=input$q.pri,
#                                 q.rec=input$q.rec))
#       } else {
#           m <- ggplot(data.frame(x=c(0,100), y=c(0,1)), aes(x * y)) +
#               stat_function(fun=function(x)ResilienceStep(lambda=input$lambda,
#                                 p.fail=x, t.hor=input$t.hor,
#                                 t.rec=input$t.rec, q.pri=input$q.pri,
#                                 q.rec=input$q.rec))
#       }
#       print(m)
#   })
})
