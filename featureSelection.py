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
        #   11: 'O',
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
results = pd.DataFrame(columns=['r', 'mse'])

X_train, X_test, y_train, y_test = train_test_split(X1, y, test_size=0.2, random_state=42)

for i, lst in enumerate(leave1):
    # print(lst)
    # keep = 'B' + ''.join(lst)  # jkqxz
    keep = ''.join(lst)
    keep_cols = [x for x in X1.columns if x[0] in keep]
    # print(len(keep_cols))

    data_train = X_train[keep_cols]
    data_test = X_test[keep_cols]
    
    # X_train.shape

    lr = LinearRegression()
    lr.fit(data_train, y_train)
    y_pred_lr = lr.predict(data_test)
    # y_pred_lr = lr.predict(X_train)

    # truth = y_train

    r, p = st.pearsonr(y_test, y_pred_lr)
    mse = mean_squared_error(y_test, y_pred_lr)
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
