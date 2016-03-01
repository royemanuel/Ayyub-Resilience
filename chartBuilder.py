import numpy as np
import pandas as pd

## Build a time range
timeH = 5
resolution = 1
fTime = 2
pLevel = 1.2
fLevel = 0.2
timeH = np.arange(0, timeH, resolution)
chartArray = pd.DataFrame({'Time': timeH})
## Stakeholder Need defined as 1
sNeed = np.ones(len(timeH))
sNeed = pd.DataFrame({'StakeN':sNeed})
chartArray = pd.concat([chartArray, sNeed], axis=1)



## Similar to cbind in R. d.concat([chartArray, n], axis=1)
## The plan is to build a function for each type of foundational
## performance: Reliability, Step (to include availability), and
## Resilience triangle

## The reliability function
## time: the input time that the function works on
## failTime: the time the failure occurs
## preLevel: the level of performance before failure
## failLevel: the level of performance at the time of failure

def stepFail(time, failTime, preLevel,  failLevel):
    if time < failTime:
        return preLevel
    else:
        return failLevel

## Build the performance curve and append to the time
perfArray = chartArray['Time'].apply(lambda x:
                                     stepFail(x, fTime, pLevel, fLevel))
## I may want to save the concat for later, but i'll build it iteratively
## for now so I can watch what is going on.
chartArray = pd.concat([chartArray, pd.DataFrame({'Performance':
                                                  perfArray})], axis=1 )

## Quotient Resilience formulation
def quotRes(resArray):
    resPerf = resArray['Performance']
    disValue = resPerf.min(axis=0)
    denValue = resPerf[0] - disValue
    qrArray = resPerf.apply(lambda x: (x - disValue) / denValue)
    qrArray = pd.DataFrame({'QR': qrArray})
    outArray = pd.concat([resArray, qrArray], axis=1)
    return outArray

chartArray = quotRes(chartArray)

## Bekera formulation for the case where there is no initial recovery
## action portion. S_p = 1 for these assumtions, and recoery is the
## final value of the metric.

## Change to use 'loc' functionality

def bekResFac(resArray):
    resPerf = np.zeros(resArray.shape[0])
    resPerf = pd.Series(resPerf)
    failIndex = resArray['Performance'].idxmin(axis=0)
    disValue = resArray['Performance'].min(axis=0)
    row = resPerf.shape[0]
    for i in range(0, row):
        if (i < failIndex):
            resPerf.loc[i] = np.nan
        else:
            resPerf[i] = resArray.loc[i,'Performance'] * disValue / (resArray['Performance'][0]**2)
    print(resPerf)
    return resPerf

brDF = bekResFac(chartArray)
brDF = pd.DataFrame({'BR': brDF})
chartArray = pd.concat([chartArray, brDF], axis=1)

def ayyubRes(resArray):
    holdP = np.zeros(resArray.shape[0])
    holdP = pd.Series(holdP)
    holdT = np.zeros(resArray.shape[0])
    holdT = pd.Series(holdT)
    ## Find the area of each time sequence
    row = resArray.shape[0]
    def perfArea(resArray, holder):
        for i in range(1,row):
            ## Calculating the area from the previous point to the final
            ## point as a triangle. Not perfect for step functions, but
            ## close enough for now
            stPoint = resArray.loc[i-1,'Performance'] / 2
            endPoint = resArray.loc[i-1, 'Performance'] / 2
            area = stPoint + endPoint
            holder[i] = holder[i-1] + area
        return holder
    def targArea(resArray, holder):
        for i in range(1,row):
            ## Calculating the area from the previous point to the final
            ## point as a triangle. Not perfect for step functions, but
            ## close enough for now
            stPoint = resArray.loc[i-1,'StakeN'] / 2
            endPoint = resArray.loc[i-1, 'StakeN'] / 2
            area = stPoint + endPoint
            holder[i] = holder[i-1] + area
        return holder
    pA = perfArea(resArray, holdP)
    tA = targArea(resArray, holdT)
    ayyRes = pA / tA
    return ayyRes

ar = ayyubRes(chartArray)
chartArray = pd.concat([chartArray,pd.DataFrame({'AR': ar})], axis=1)

