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
    ## I think I need to get rid of this part
    resPerf = resArray.loc[:,'Performance']
    ## end this part
    failIndex = resPerf.idxmin(axis=0)
    disValue = resPerf.min(axis=0)
    row = resPerf.shape[0]
    print(row)
    for i in range(0, row):
        ## Actually make this another function and apply it as a lambda
        ## to the Array
        if (i < failIndex):
            resPerf.loc[i] = np.nan
        else:
            resPerf[i] = resArray.loc[i, 'Performance'] * disValue / (resArray.loc[0,'Performance']**2)
    return resPerf
