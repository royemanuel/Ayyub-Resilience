import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import expon, lognorm, uniform
import seaborn as sns
import os

######################################################
#                                                    #
#      Defining Variables                            #
#               For use                              #
#                                                    #
######################################################

# Build a time range
timeH = 50
resolution = 0.01
fTime = 15
rTime = 40
pLevel = 1.2
fLevel = 0.6
rLevel = .95

timeH = np.arange(0, timeH, resolution)
chartArray = pd.DataFrame({'Time': timeH})


# Similar to cbind in R. d.concat([chartArray, n], axis=1)
# The plan is to build a function for each type of foundational
# performance: Reliability, Step (to include availability), and
# Resilience triangle

# The reliability function
# time: the input time that the function works on
# failTime: the time the failure occurs
# preLevel: the level of performance before failure
# failLevel: the level of performance at the time of failure

######################################################
#                                                    #
#      Defining Functions                            #
#               For use                              #
#                                                    #
######################################################


# Build the performance curve and append to the time
def buildPerf(resArray, pFunc, *args):
    return resArray['Time'].apply(lambda x: pFunc(x, *args))


# Stakeholder Need defined as 1
def statusQuo(resArray):
    sNeed = np.ones(len(timeH))
    resArray['StakeN'] = pd.DataFrame({'StakeN': sNeed})
    return resArray


# A range of status quo needs
# The failure portion of a step function with no recovery
def stepFail(time, failTime, preLevel, failLevel):
    if time < failTime:
        return preLevel
    else:
        return failLevel


# A step function failure with a recovery
def stepFR(time, failTime, recTime, preLevel, failLevel, recLevel):
    if time < failTime:
        return preLevel
    elif time < recTime:
        return failLevel
    else:
        return recLevel


# A linear failure to the failLevel followed by an immediate start
# to a linear recovery
def triPerf(time, failTime, recTime, preLevel, failLevel, recLevel):
    if time < failTime:
        return preLevel
    elif time < recTime:
        prof = failLevel + (time - failTime)*(recLevel - failLevel) / \
          (recTime-failTime)
        return prof
    else:
        return recLevel


# Quotient Resilience formulation
def quotRes(resArray):
    resPerf = resArray['Performance']
    disValue = resPerf.min(axis=0)
    denValue = resPerf[0] - disValue
    qrArray = resPerf.apply(lambda x: (x - disValue) / denValue)
    # qrArray = pd.DataFrame({'QR': qrArray})
    # outArray = pd.concat([resArray, qrArray], axis=1)
    return qrArray


# Bekera formulation for the case where there is no initial recovery
# action portion. S_p = 1 for these assumtions, and recovery is the
# final value of the metric.
# Change to use 'loc' functionality
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
            resPerf[i] = resArray.loc[i, 'Performance'] * disValue / \
              (resArray['Performance'][0]**2)
    return resPerf

# brDF = bekResFac(chartArray)
# brDF = pd.DataFrame({'BR': brDF})

# I changes these so stPoint was i-1 and endpoint was i. Is that correct?


def perfArea(resArray):
    row = resArray.shape[0]
    holder = np.zeros(resArray.shape[0])
    holder = pd.Series(holder)
    for i in range(1, row):
        # Calculating the area from the previous point to the final
            # point as a triangle. Not perfect for step functions, but
            # close enough for now
        stPoint = resArray.loc[i-1, 'Performance'] / 2
        endPoint = resArray.loc[i, 'Performance'] / 2
        area = stPoint + endPoint
        holder[i] = holder[i-1] + area
    return holder


def targArea(resArray):
    holder = np.zeros(resArray.shape[0])
    holder = pd.Series(holder)
    row = resArray.shape[0]
    for i in range(1, row):
        # Calculating the area from the previous point to the final
        # point as a triangle. Not perfect for step functions, but
        # close enough for now
        stPoint = resArray.loc[i-1, 'StakeN'] / 2
        endPoint = resArray.loc[i, 'StakeN'] / 2
        area = stPoint + endPoint
        holder[i] = holder[i-1] + area
    return holder

# Build a lower triangular array and add the columns to get the
# cumulative value


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

# def vecTargArea(resArray):
#    area = (resArray['Performance']+resArray['Performance'].shift(1))/2


def ayyubRes(resArray):
    # Find the area of each time sequence
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

###########################################
#           Sample Chart Array to use     #
###########################################

# chartArray = statusQuo(chartArray)
# chartArray['Performance'] = buildPerf(chartArray, stepFR, fTime, rTime,
#                                      pLevel, fLevel, rLevel)
# chartArray['QR'] = quotRes(chartArray)
# chartArray['BR'] = bekResFac(chartArray)
# chartArray['IR'] = ayyubRes(chartArray)
# chartArray['RnS'] = nonSubRes(chartArray)


# baseBuild yields the time ticker and the Stakeholder Need Model 
def baseBuild(maxTimeH, resolution, stakeNeed, *args):
    timeH = np.arange(0, maxTimeH, resolution)
    pltArray = pd.DataFrame({'Time': timeH})
    pltArray = stakeNeed(pltArray, *args)
    return pltArray


# perfBuild yields the performance of the system. Takes statusQuo,
# stepFR, stepFail, and triPerf as arguments for the shape of the
# performance curve
def perfBuild(baseArray, perfFunc, *args):
    baseArray['Performance'] = buildPerf(baseArray, perfFunc, *args)
    return baseArray


# resBuild builds columns of quotient resilience, FB resilience, and
# ayyub resilience
def resBuild(baseArray):
    baseArray['QR'] = quotRes(baseArray)
    baseArray['RF'] = bekResFac(baseArray)
    baseArray['IR'] = ayyubRes(baseArray)
    baseArray['RnS'] = nonSubRes(baseArray)
    return baseArray


# extResBuild builds the columns of the extended QR, FB, and IR.
###############################################################
###############################################################
#                                                             #
#            Build some                                       #
#                        Random Dataframes                    #
#                                     For mass building       #
#                                                             #
###############################################################
###############################################################

failSeries = expon.rvs(scale=20, size=100)
# Calculate lognorm parameters
muLog = np.log(15/np.sqrt(1+(10/15**2)))
sigLog = np.sqrt(np.log(1 + 10/15**2))
recoverSeries = np.exp(lognorm.rvs(sigLog, loc=muLog, size=100))
failPerf = 0.1 * uniform.rvs(size=100)
recoveryPerf = 0.9 + 0.2 * uniform.rvs(size=100)


paramArray = pd.DataFrame({'FailTime': failSeries,
                           'RecoverTime': failSeries + recoverSeries,
                           'FailPerformance': failPerf,
                           'RecoveryPerformance': recoveryPerf})

paramArray2 = pd.DataFrame({'FailTime': 15,
                            'RecoverTime': 15 + recoverSeries,
                            'FailPerformance': failPerf,
                            'RecoveryPerformance': recoveryPerf})


###############################################################
###############################################################
#                                                             #
#            Run the resilience                               #
#                        metric builder                       #
#                                 through the paramArray      #
#                                                             #
###############################################################
###############################################################

def resDistribution(timeH, resolution, stakeNeed, pFunc, pArray, *args):
    baseArray = baseBuild(timeH, resolution, stakeNeed, *args)
    resArray = pd.DataFrame()
    # print(baseArray.tail())
    for i in range(0, pArray.shape[0]):
        f = perfBuild(baseArray, pFunc, pArray.loc[i, 'FailTime'],
                      pArray.loc[i, 'RecoverTime'],
                      1.2,
                      pArray.loc[i, 'FailPerformance'],
                      pArray.loc[i, 'RecoveryPerformance'])
        f = resBuild(f)
        f.loc[:, 'Run'] = i
        resArray = resArray.append(f, ignore_index=True)
        del f
    g = pd.melt(resArray, id_vars=['Time', 'Run'],
                value_vars=['StakeN', 'Performance', 'QR', 'RF', 'IR', 'RnS'])
    return g

# h = resDistribution(100, 1, statusQuo, stepFR, paramArray)
# j = resDistribution(100, 1, statusQuo, triPerf, paramArray)


def resDistributionSTK(timeH, resolution, stakeNeed, pFunc, pArray, *args):
    baseArray = baseBuild(timeH, resolution, stakeNeed, *args)
    resArray = pd.DataFrame()
    # print(baseArray.tail())
    for i in range(0, pArray.shape[0]):
        baseArray['StakeN'] = baseArray['StakeN'] * (1 - 1 / pArray.shape[0])
        f = perfBuild(baseArray, pFunc, pArray.loc[i, 'FailTime'],
                      pArray.loc[i, 'RecoverTime'],
                      1.2,
                      pArray.loc[i, 'FailPerformance'],
                      pArray.loc[i, 'RecoveryPerformance'])
        f = resBuild(f)
        f.loc[:, 'Run'] = i
        resArray = resArray.append(f, ignore_index=True)
        del f
    g = pd.melt(resArray, id_vars=['Time', 'Run'],
                value_vars=['StakeN', 'Performance', 'QR', 'RF', 'IR', 'RnS'])
    return g
