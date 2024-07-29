# %%
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import os

# %%

total_time = []
time_steps = []
word_lists = []
letters = []
ids = []

# mydir = 'games/'
# mydir = 'fails/'

for mydir in ['games/', 'fails/']:
    games = [x for x in os.listdir(mydir) if x[0].isupper()]
    for g in games:
        ids.append(g)
        with open(mydir+g+'/total_time.txt') as fin:
            lines = fin.readlines()
            total_time.append(float(lines[0].rstrip()))
            letters.append(lines[1].rstrip())
        with open(mydir+g+'/time_steps.txt') as fin:
            lines = fin.readlines()
            steps = [float(x.rstrip()) for x in lines[:-1]]
            time_steps.append(steps)
        with open(mydir+g+'/words.txt') as fin:
            lines = [x.rstrip() for x in fin.readlines()]
            word_lists.append(lines)

# %%

# df1: letters and total time
# df2: timesteps (get pass/fail by checking last column)
# df3: list of words for each run

# tids = ids[:3] + ids[-3:]
# tlets = letters[:3] + letters[-3:]
# ttots = total_time[:3] + total_time[-3:]
# tsteps = time_steps[:3] + time_steps[-3:]
# twords = word_lists[:3] + word_lists[-3:]

tids = ids
tlets = letters
ttots = total_time
tsteps = time_steps
twords = word_lists

# pad letters
for i, sequence in enumerate(tlets):
    if len(sequence) < 144:
        padded_seq = sequence + ('.' * (144 - len(sequence)))
        tlets[i] = padded_seq
df1 = pd.DataFrame(index=tids, columns=range(len(tlets[0])))
for i in df1.columns:
    df1.loc[:,i] = [x[i] for x in tlets]
df1['time'] = ttots
df1.index.name = 'id'

# pad times
for i, steps in enumerate(tsteps):
    padded_steps = [pd.NA]*20 + steps
    remaining = [pd.NA]*(144 - len(padded_steps))
    tsteps[i] = padded_steps + remaining
df2 = pd.DataFrame(index=tids, columns=range(len(tsteps[0])))
for i in df2.columns:
    df2.loc[:,i] = [x[i] for x in tsteps]
# don't really need a pass/fail. if last column is NA -> failed.
# times start at 21, but only 22 onwards give individual letter times
df2.index.name = 'id'

# pad word lists
maxlen = max([len(x) for x in twords])
for i, sequence in enumerate(twords):
    if len(sequence) < maxlen:
        padded_seq = sequence + ([''] * (maxlen - len(sequence)))
        twords[i] = padded_seq
df3 = pd.DataFrame(index=tids, columns=range(len(twords[0])))
for i in df3.columns:
    df3.loc[:,i] = [x[i] for x in twords]
df3.index.name = 'id'

df1.to_csv('data/letters.csv')
df2.to_csv('data/timesteps.csv')
df3.to_csv('data/words.csv')
