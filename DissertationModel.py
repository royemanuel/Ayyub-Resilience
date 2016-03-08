import simpy
import numpy as np
import pandas as pd
import scipy.stats as st

class Aircraft(object):
    ## Pull the resting fail time and the flying fail time. Add the times
    ## in the simulator u
    def __init__(self, env):
        self.env = env
        self.action = env.process(self.run())
        self.restFailtime = ## pull a number
        self.flyFailtime = ## pull a number
    def rest(self):
        ## Low failure rate for this one
        ## failTime = random pull
        if failTime < 
    def fly(self):
        ## Higher failure rate for this one
    
