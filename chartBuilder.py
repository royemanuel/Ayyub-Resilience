import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
########################################################
##                                                    ##
##      Defining Variables                            ##
##               For use                              ##
##                                                    ##
########################################################

## Build a time range
timeH = 50
resolution = 0.01
fTime = 15
rTime = 40
pLevel = 1.2
fLevel = 0.6
rLevel = .95

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

########################################################
##                                                    ##
##      Defining Functions                            ##
##               For use                              ##
##                                                    ##
########################################################

## Build the performance curve and append to the time
def buildPerf(resArray, pFunc, *args):
    return resArray['Time'].apply(lambda x: pFunc(x, *args))

## Stakeholder Need defined as 1
def statusQuo(resArray):
    sNeed = np.ones(len(timeH))
    resArray['StakeN'] = pd.DataFrame({'StakeN':sNeed})
    return resArray


def stepFail(time, failTime, preLevel,  failLevel):
    if time < failTime:
        return preLevel
    else:
        return failLevel

def stepFR(time, failTime, recTime, preLevel, failLevel, recLevel):
    if time < failTime:
        return preLevel
    elif time < recTime:
        return failLevel
    else:
        return recLevel

def triPerf(time, failTime, recTime, preLevel, failLevel, recLevel):
    if time < failTime:
        return preLevel
    elif time < recTime:
        prof = failLevel + (time - failTime)*(recLevel - failLevel) / (recTime-failTime)
        return prof
    else:
        return recLevel




## Quotient Resilience formulation
def quotRes(resArray):
    resPerf = resArray['Performance']
    disValue = resPerf.min(axis=0)
    denValue = resPerf[0] - disValue
    qrArray = resPerf.apply(lambda x: (x - disValue) / denValue)
    ## qrArray = pd.DataFrame({'QR': qrArray})
    ## outArray = pd.concat([resArray, qrArray], axis=1)
    return qrArray



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
    return resPerf

## brDF = bekResFac(chartArray)
## brDF = pd.DataFrame({'BR': brDF})

## I changes these so stPoint was i-1 and endpoint was i. Is that correct?
def perfArea(resArray):
    row = resArray.shape[0]
    holder = np.zeros(resArray.shape[0])
    holder = pd.Series(holder)
    for i in range(1,row):
        ## Calculating the area from the previous point to the final
            ## point as a triangle. Not perfect for step functions, but
            ## close enough for now
        stPoint = resArray.loc[i-1,'Performance'] / 2
        endPoint = resArray.loc[i, 'Performance'] / 2
        area = stPoint + endPoint
        holder[i] = holder[i-1] + area
    return holder
def targArea(resArray):
    holder = np.zeros(resArray.shape[0])
    holder = pd.Series(holder)
    row = resArray.shape[0]
    for i in range(1,row):
        ## Calculating the area from the previous point to the final
        ## point as a triangle. Not perfect for step functions, but
        ## close enough for now
        stPoint = resArray.loc[i-1,'StakeN'] / 2
        endPoint = resArray.loc[i, 'StakeN'] / 2
        area = stPoint + endPoint
        holder[i] = holder[i-1] + area
    return holder

## Build a lower triangular array and add the columns to get the
## cumulative value
def vecSum(array):
    df = pd.DataFrame()
    for i in range(0, len(array)):
        df[str(i)] = array.shift(i)
    dSum = df.sum(axis=1)
    return dSum

def ayyubRes2(resArray):
    p = vecSum(resArray['Performance'])
    t = vecSum(resArray['StakeN'])
    return p / t

##def vecTargArea(resArray):
##    area = (resArray['Performance']+resArray['Performance'].shift(1))/2

def ayyubRes(resArray):
    ## Find the area of each time sequence
    pA = perfArea(resArray)
    tA = targArea(resArray)
    ayyRes = pA / tA
    return ayyRes

def nonSubRes(resArray):
    nsrArray = np.zeros(resArray.shape[0])
    row = resArray.shape[0]
    for i in range(0, row):
        if resArray.loc[i, 'StakeN'] > resArray.loc[i, 'Performance']:
            nsrArray[i] = resArray.loc[i, 'Performance']
        else:
            nsrArray[i] = resArray.loc[i, 'StakeN']
    nsrArray = pd.DataFrame({'Performance': nsrArray})
    pA = perfArea(nsrArray)
    tA = targArea(resArray)
    nsRes = pA / tA
    return nsRes



chartArray = statusQuo(chartArray)
chartArray['Performance'] = buildPerf(chartArray, stepFR, fTime, rTime,
                                      pLevel, fLevel, rLevel)
chartArray['QR'] = quotRes(chartArray)
chartArray['BekR'] = bekResFac(chartArray)
chartArray['AyyR'] = ayyubRes(chartArray)
chartArray['NonSubRes'] = nonSubRes(chartArray)

## Function to tie it all together

def baseBuild(maxTimeH, resolution, stakeNeed, *args):
    timeH = np.arange(0, maxTimeH, resolution)
    pltArray = pd.DataFrame({'Time': timeH})
    pltArray = stakeNeed(pltArray, *args)
    return pltArray


def resBuild(baseArray, perfFunc, *args):
    baseArray['Performance'] = buildPerf(baseArray, perfFunc, *args)
    baseArray['Quotient Resilience'] = quotRes(baseArray)
    baseArray['Resilience Factor'] = bekResFac(baseArray)
    baseArray['Resilience with Substitution'] = ayyubRes(baseArray)
    baseArray['Resilience without Substitution'] = nonSubRes(baseArray)
    return baseArray

