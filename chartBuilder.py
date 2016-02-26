import numpy as np
import pandas as pd

## Build a time range
timeH = 5
resolution = 1
timeH = np.arange(0, timeH, resolution)
chartArray = pd.DataFrame(timeH)

## def stepFail(time, timeI, timeR, timeH, perfPre, perfFail, perfRec):
    
## Similar to cbind in R. d.concat([chartArray, n], axis=1)
