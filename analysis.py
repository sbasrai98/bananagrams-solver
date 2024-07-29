# %%
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import os

# %%
### LOAD DATA ###
letters = pd.read_csv('data/letters.csv', index_col='id')
timesteps = pd.read_csv('data/timesteps.csv', index_col='id')
words = pd.read_csv('data/words.csv', index_col='id')

passed = pd.Series(timesteps[~pd.isna(timesteps.iloc[:,143])].index)
failed = pd.Series(timesteps[pd.isna(timesteps.iloc[:,143])].index)
instant_fail = pd.Series(timesteps[pd.isna(timesteps.iloc[:,20])].index)

# %%
### COMPLETION TIME DISTRIBUTION ###
total_time = letters.loc[passed, 'time']
# total_time = letters.loc[failed, 'time']

fig, ax = plt.subplots(figsize=(6,4))
ax.hist(total_time, bins=100)
# ax.set_ylim(0,30)
ax.axvline(x=np.mean(total_time), color='red', linestyle='dashed')
ax.set_xlabel('Completion Time (seconds)')
ax.set_ylabel('Frequency')
pd.Series(total_time).describe()

# %%
### PIE CHART ###
colors = ['green', 'red', 'orange']
data = [len(passed), len(instant_fail), len(failed) - len(instant_fail)]
# wedge_labels = [str(round(x / letters.shape[0], 2)) for x in data]
fig, ax = plt.subplots(figsize=(6,6))
ax.pie(data,
        wedgeprops={'linewidth':2, 'edgecolor':'black'},
        textprops={'fontsize':14},
        startangle=90, counterclock=True,
        colors=colors,
        labels=data # wedge_labels
        )
handles = [mpl.patches.Patch(facecolor=color, edgecolor='black') for color in colors]
labels = ['Completed', 'Instant Fails', 'Other Fails']
ax.legend(handles=handles, labels=labels, ncol=len(handles),
           frameon=False, fontsize=14,
           loc=(-0.14, 0),
           )

# %%
### TIME STEPS ###
subset = passed
# subset = failed
fig, ax = plt.subplots(figsize=(8,6))
for i in subset:
    ax.step(timesteps.loc[i], range(timesteps.shape[1]), where='post')
if subset is passed:
    ax.step(np.mean(timesteps.loc[subset,:], axis=0), range(timesteps.shape[1]),
            where='post', linewidth=2, color='black', linestyle='dashed')

# %%
### AVERAGE INCORPORATION TIME FOR EACH LETTER ###
# start from i=21, checking what i21 - i20 is to get time for letter21
incorp_times = {x:[] for x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'}

for id in range(letters.shape[0]):
    for i in range(21, timesteps.shape[1]):
        l = letters.iat[id, i]
        start = timesteps.iat[id, i-1]
        end = timesteps.iat[id, i]
        if not pd.isna(end):
            incorp_times[l].append(end-start)

for k,v in incorp_times.items(): print(k, len(v))
# %%
data = [np.mean(incorp_times[x]) for x in list(incorp_times)]
labels = list(incorp_times)

fig, ax = plt.subplots(figsize=(7,5))
ax.bar(range(len(data)), data, )#width=0.7, align='edge')
ax.set_xticks(range(len(data)))
ax.set_xticklabels(labels)

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
word_counts = word_counts[word_counts['len'] == 6]
fig, ax = plt.subplots(figsize=(7,5))

top = 20
data = word_counts['count'][:top]
labels = word_counts['word'][:top]
ax.bar(range(len(data)), data, width=0.5)
ax.set_xticks(range(len(data)))
ax.set_xticklabels(labels, rotation=45, ha='right')

# %%

dir1 = 'games/' # gamesets/2k/
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

# %%

# can calculate average incorporation time for each letter..