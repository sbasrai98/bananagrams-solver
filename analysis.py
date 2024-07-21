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


mydir = 'games/'
# mydir = 'fails/'
# mydir = 'test/'

games = [x for x in os.listdir(mydir) if x[0].isupper()]
for g in games:
    with open(mydir+g+'/total_time.txt') as fin:
        lines = fin.readlines()
        total_time.append(float(lines[0].rstrip()))
    with open(mydir+g+'/time_steps.txt') as fin:
        lines = fin.readlines()
        steps = [float(x.rstrip()) for x in lines[:-1]]
        time_steps.append(steps)
    with open(mydir+g+'/words.txt') as fin:
        lines = [x.rstrip() for x in fin.readlines()]
        word_lists.append(lines)

fig, ax = plt.subplots(figsize=(8,6))
ax.hist(total_time, bins=100)

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

means = []
sds = []
first21 = []

for t in time_steps:
    dsteps = []
    for i in range (1, len(t)):
        dsteps.append(t[i]-t[i-1])
    means.append(np.mean(dsteps))
    sds.append(np.std(dsteps))
    first21.append(t[0])

metric = sds
fig, ax = plt.subplots(figsize=(8,6))
ax.hist(metric, bins=30)
pd.Series(metric).describe()

# %%
### words in each 

word_counts = {}
for lst in word_lists:
    for w in lst:
        if w not in word_counts:
            word_counts[w] = 0
        word_counts[w] += 1
word_counts = pd.DataFrame({'word': word_counts.keys(),
                            'count': word_counts.values()})
word_counts.sort_values(by='count', ascending=False, inplace=True)
word_counts['len'] = [len(x) for x in word_counts['word']] 
word_counts = word_counts[word_counts['len'] >= 15]
fig, ax = plt.subplots(figsize=(7,5))

top = 20
data = word_counts['count'][:top]
labels = word_counts['word'][:top]
ax.bar(range(len(data)), data, width=0.5)
ax.set_xticks(range(len(data)))
ax.set_xticklabels(labels, rotation=45, ha='right')

# %%

dir1 = 'games/'
dir2 = 'fails/'

letters = []

for direc in [dir1, dir2]:
    games = [x for x in os.listdir(direc) if x[0].isupper()]
    l = []
    for g in games:
        with open(direc+g+'/total_time.txt') as fin:
            lines = fin.readlines()
            l.append(lines[1].rstrip())
    letters.append(l)

instant_fail = [x for x in letters[1] if len(x) == 21]
len(instant_fail)

# %%

def letter_frequencies(letters):
    all_letters = ''.join(letters)
    counts = {}
    for l in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        counts[l] = all_letters.count(l) / len(all_letters)
    return counts

counts1 = letter_frequencies(instant_fail) #[x[:21] for x in letters[1]]
counts2 = letter_frequencies([x[:21] for x in letters[0]])

fig, ax = plt.subplots(figsize=(7,5))
data = [counts2.values(), counts1.values()]
labels = counts1.keys()
ax.bar(np.arange(len(counts1))*2.3 - 0.7, data[0], width=0.7, align='edge')
ax.bar(np.arange(len(counts1))*2.3, data[1], width=0.7, align='edge')
ax.set_xticks(np.arange(len(counts1))*2.3)
ax.set_xticklabels(labels)