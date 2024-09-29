# %%
import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.stats as st
from encode_sequence import *

import itertools
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# %%
### LOAD DATA ###
letters = pd.read_csv('data/letters.csv', index_col='id')
timesteps = pd.read_csv('data/timesteps.csv', index_col='id')

passed = pd.Series(timesteps[~pd.isna(timesteps.iloc[:,143])].index)
failed = pd.Series(timesteps[pd.isna(timesteps.iloc[:,143])].index)
instant_fail = pd.Series(timesteps[pd.isna(timesteps.iloc[:,20])].index)

## get sequences as strings
sequences = [''.join(letters.iloc[i, :-1]) for i in range(letters.shape[0])]
sequences_og = sequences[:]
# simplify alphabet
simplify = True
# simplify = False
if simplify:
    for i in range(len(sequences)):
        sequences[i] = encode3(sequences[i])
        # sequences[i] = encode4(sequences[i])
        
times = letters['time']
letters = pd.DataFrame(index=letters.index)
letters['letters'] = sequences
letters['letters_og'] = sequences_og
letters['time'] = times
letters

alphabet = sorted(list(set(sequences[i]) - set(['.'])))
alphabet

# %%
### USE LETTER POSITIONS AS FEATURES
counts = {2: 'JKQXZ',
          3: 'BCFHMPVWY', #HP
          4: 'G',
          5: 'L',
          6: 'DSU',
          8: 'N',
          9: 'TR',
        #   11: 'O',  # 0.1% gain if including 1st occurrence
        #   12: 'I',
        #   13: 'A',
        #   18: 'E'
          }

boardletters = ''
for k, v in counts.items(): 
    boardletters += (v*k)
features = []
for i, l in enumerate(boardletters):
    num = boardletters[:i].count(l) + 1
    features.append(l+str(num))
print(len(features))

### ENCODE STRINGS AS LETTER POSITIONS
X1 = pd.DataFrame(index=passed, columns=features,
                 data=np.zeros((len(passed), len(features))))
y = letters.loc[passed, 'time'].copy()
for i in passed[:]:
    seq = letters.at[i, 'letters_og']
    for k, v in counts.items():
        for l in v:
            idx = [x for x in range(len(seq)) if seq[x] == l]
            for num in range(1, k+1):
                X1.at[i, l+str(num)] = idx[num-1]    
X1.shape
# %%
### ADD DISTANCES BETWEEN JKQXZ
pos_distance = ['Jdist', 'Kdist', 'Qdist', 'Xdist', 'Zdist']
X1_extra = pd.DataFrame(index=passed, columns=pos_distance,
                 data=np.zeros((len(passed), len(pos_distance))))
for i in passed[:]:
    seq = letters.at[i, 'letters_og']
    
    for k, v in [(2, counts[2])]:
        for l in v:
            idx = [x for x in range(len(seq)) if seq[x] == l]
            dist = idx[1] - idx[0]
            X1_extra.at[i, l+'dist'] = dist
            # for num in range(1, k+1):
            #     X1.at[i, l+str(num)] = idx[num-1]    

X1_extra.shape

# %%
combos = list(itertools.combinations(X1.columns[:10], 2))
combos = [x[0]+'-'+x[1] for x in combos]
X1_extra = pd.DataFrame(index=passed, columns=combos,
                 data=np.zeros((len(passed), len(combos))))
for i in passed[:]:
    seq = letters.at[i, 'letters_og']
    for combo in combos:
        a, b = combo.split('-')
        X1_extra.at[i, combo] = np.abs(X1.at[i, a] - X1.at[i, b])
    
X1_extra.shape


X1 = pd.merge(X1, X1_extra, left_index=True, right_index=True)
X1.shape
# %%
## generate all sets of 'BCFHMPVWYGLDSUNTR'

# Function to generate all possible subsets
def generate_subsets(sequence):
    subsets = []
    for r in range(len(sequence) + 1):
        subsets.extend(itertools.combinations(sequence, r))
    return subsets
                            #B
# all_subsets = pd.Series(generate_subsets('BCFHMPVWYGLDSUNTR'))
# all_subsets

all_letters = 'JKQXZBCFHMPVWYGLDSUNTR'
leave1 = [list(all_letters)]
for l in all_letters:
    leave1.append(list(all_letters.replace(l, '')))
leave1 = pd.Series(leave1)
leave1

# %%
leaveN = [list(X1.columns[:90])]
for i in range(2,10):
    # leaveout = [x for x in X1.columns if x[0] in bad and int(x[1:]) < i]
    # leaveN.append(leaveout)

    starting = list(X1.columns[:90])
    bad = 'OAIE'

    addon = [x for x in X1.columns if x[0] in bad and int(x[1:]) < i]
    leaveN.append(starting + addon)

leaveN = pd.Series(leaveN)
leaveN

leaveN = [list(X1.columns[:])]

# %%
results = pd.DataFrame(columns=['r', 'mse'])

X_train, X_test, y_train, y_test = train_test_split(X1, y, test_size=0.2, random_state=42)

# for i, lst in enumerate(leave1):
for i, lst in enumerate(leaveN):
    # print(lst)
    # keep = 'B' + ''.join(lst)  # jkqxz
    # keep = ''.join(lst)
    # keep_cols = [x for x in X1.columns if x[0] in keep]
    
    keep_cols = lst
    # print(len(keep_cols))


    data_train = X_train[keep_cols]
    data_test = X_test[keep_cols]


    # X_train.shape

    lr = LinearRegression()
    lr.fit(data_train, y_train)
    y_pred_lr = lr.predict(data_test)
    truth = y_test
    # y_pred_lr = lr.predict(data_train)
    # truth = y_train    
    r, p = st.pearsonr(truth, y_pred_lr)
    mse = mean_squared_error(truth, y_pred_lr)
    results.loc[i] = r, mse

    # if i % 50 == 0: print(f'{i} / {all_subsets.shape[0]}')

results
# %%
fig, ax = plt.subplots(figsize=(8,6))
ax.hist([preds, truth], bins=100)
# ax.hist(truth, bins=100)
# ax.hist(preds, bins=100)
plt.plot;

# %%
import pickle

with open('preds.pkl', 'wb') as fout:
    pickle.dump(preds, fout, pickle.HIGHEST_PROTOCOL)
with open('truth.pkl', 'wb') as fout:
    pickle.dump(truth, fout, pickle.HIGHEST_PROTOCOL)
