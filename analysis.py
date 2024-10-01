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

fig, ax = plt.subplots(figsize=(7,3))
ax.hist(total_time, bins=100)
# ax.set_ylim(0,30)
ax.axvline(x=np.mean(total_time), color='red', linestyle='dashed')
ax.set_xlabel('Completion Time (s)')
ax.set_ylabel('Frequency')
print(letters.shape[0])
print(len(passed) / letters.shape[0])
ax.text(0.77, 0.9, f'Average: {round(np.mean(total_time), 1)}s',
        transform=ax.transAxes)
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
        labels=data, # wedge_labels
        # labeldistance=0.6
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
fig, ax = plt.subplots(figsize=(7,3))
for i in subset:
    ax.step(timesteps.loc[i], range(timesteps.shape[1]), where='post', linewidth=1)
if subset is passed:
    ax.step(np.mean(timesteps.loc[subset,:], axis=0), range(timesteps.shape[1]),
            where='post', linewidth=2, color='black', linestyle='dashed')
ax.set_xlabel('Completion Time (s)')
ax.set_ylabel('Letters Incorporated')

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
mean_incorp = {data[i]:labels[i] for i in range(len(labels))}
mean_incorp
data = sorted(data, reverse=True)
labels = [mean_incorp[i] for i in data]

fig, ax = plt.subplots(figsize=(7,3))
ax.bar(range(len(data)), data, )#width=0.7, align='edge')
ax.set_xticks(range(len(data)))
ax.set_xticklabels(labels)
ax.set_ylabel('Average Incorporation Time (s)')

# %%
### words in each 

word_counts = {}
word_lists = [words.loc[i].dropna() for i in words.index]
for lst in word_lists:
    for w in lst:
        if w not in word_counts:
            word_counts[w] = 0
        word_counts[w] += 1
word_counts = pd.DataFrame({'word': word_counts.keys(),
                            'count': word_counts.values()})
word_counts.sort_values(by='count', ascending=False, inplace=True)
word_counts['len'] = [len(x) for x in word_counts['word']] 
word_counts = word_counts[word_counts['len'] == 4]
fig, ax = plt.subplots(figsize=(7,5))

top = 20
data = word_counts['count'][:top]
labels = word_counts['word'][:top]
ax.bar(range(len(data)), data, width=0.5)
ax.set_xticks(range(len(data)))
ax.set_xticklabels(labels, rotation=45, ha='right')

# %%
### COMPARE FIRST 21 LETTERS FOR COMPLETED VS. INSTANT FAIL
passed_21 = letters.loc[passed, map(str,range(21))].values.flatten()
instant_fail_21 = letters.loc[instant_fail, map(str,range(21))].values.flatten()

def letter_frequencies(letters):
    all_letters = ''.join(letters)
    counts = {}
    for l in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        counts[l] = all_letters.count(l) / len(all_letters)
    return counts

passed_freq = letter_frequencies(passed_21)
instant_fail_freq = letter_frequencies(instant_fail_21)

labels = sorted(list(passed_freq), key=lambda x: -passed_freq[x])
data = [[passed_freq[k] for k in labels],
        [instant_fail_freq[k] for k in labels]]

fig, ax = plt.subplots(figsize=(7,3))
ax.bar(np.arange(len(passed_freq))*2.3 - 0.7, data[0], width=0.7, align='edge')
ax.bar(np.arange(len(passed_freq))*2.3, data[1], width=0.7, align='edge')
ax.set_xticks(np.arange(len(passed_freq))*2.3)
ax.set_xticklabels(labels)
ax.set_ylabel('Frequency')
ax.legend(labels=['Completed', 'Instant Fails'], frameon=False)
