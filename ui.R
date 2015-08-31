# ui.R
shinyUI(fluidPage(
    titlePanel("Practical Resilience Metrics (Ayyub 2015)"),
    sidebarLayout(
    sidebarPanel(
        sliderInput("t.hor", "Time Horizon in Years:",
                    min=1, max=100, value=10),
        sliderInput("lambda", "Arrival Frequency in 1/Years:",
                    min=0, max=5, value=.05, step=.05),
        sliderInput("p.fail", "Probability of Failure Given a Disturbance:",
                    min=0, max=1, value=.5),
        sliderInput("t.rec", "Time to Recover in Years:",
                    min=1, max=100, value=4),
        sliderInput("q.pri", "Nominal Performance Level:",
                    min=0, max=1, value=1),
        sliderInput("q.rec", "Minimum Performance during Recovery:",
                    min=0, max=1, value=0),
        radioButtons("recType", "Recovery Profile Type:",
                     c("Linear" = "lin",
                       "Step" = "step"))
    ),
        mainPanel(
            plotOutput("res.v.recovery"),
            plotOutput("res.v.prob"),
            plotOutput("res.v.ratio")
        )
    )
))
