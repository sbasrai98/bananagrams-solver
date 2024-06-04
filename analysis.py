# %%
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import os

# %%

total_time = []
time_steps = []

mydir = 'games/'
# mydir = 'fails/'

games = [x for x in os.listdir(mydir) if x[0].isupper()]
for g in games:
    with open(mydir+g+'/total_time.txt') as fin:
        lines = fin.readlines()
        total_time.append(float(lines[0].rstrip()))
    
    with open(mydir+g+'/time_steps.txt') as fin:
        lines = fin.readlines()
        # print(lines[-2])
        # for l in lines: print(l[-2])
        steps = [float(x.rstrip()) for x in lines[:-1]]
        time_steps.append(steps)
    

fig, ax = plt.subplots(figsize=(8,6))
ax.hist(total_time, bins=20)

fig, ax = plt.subplots(figsize=(8,6))
for steps in time_steps:
    ax.step(steps, range(len(steps)), where='post')

steps_arr = pd.concat([pd.Series(x) for x in time_steps], axis=1)
if mydir == 'games/':
    ax.step(np.mean(steps_arr, axis=1), range(len(steps)), where='post',
            linewidth=3, color='black', linestyle='dashed')

pd.Series(total_time).describe()

# %%

# cluster by sequence, by time steps
# are there similar time step sequences with disparate letters?
# or vice versa?

# within each run, get distribution(mean, var) of time steps
# what is the distributiion of mean, var across the runs?