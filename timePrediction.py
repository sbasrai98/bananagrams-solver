# %%
import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.stats as st
from encode_sequence import *

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
### USE KMER COUNTS AS FEATURES
kmers = alphabet[:]
w = 3
for i in range(w-1): # easier to try different values..
    new = []
    for k in kmers:
        for l in alphabet:
            new.append(k+l)
    kmers = new
print(len(kmers))

### CONVERT STRINGS TO KMER COUNTS
X2 = pd.DataFrame(index=passed, columns=kmers,
                 data=np.zeros((len(passed), len(kmers))))
for i in passed:
    seq = letters.at[i, 'letters']
    for j in range(len(seq)-w+1):
        X2.at[i, seq[j:j+w]] += 1

# %%
## get r for each variable vs times independently..
corrs = pd.DataFrame(index=X.columns, columns=['r','mag'])
for col in X.columns:
    r, p = st.pearsonr(X[col], y)
    corrs.at[col, 'r'] = r
    corrs.at[col, 'mag'] = np.abs(r)
usecols = corrs.sort_values(by='mag', ascending=False)
usecols
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(usecols)

# %%
from sklearn.model_selection import train_test_split
# dataset = X1
# dataset = X2
dataset = pd.merge(X1, X2, left_index=True, right_index=True)
X_train, X_test, y_train, y_test = train_test_split(dataset, y, test_size=0.2, random_state=42)

# %%
from sklearn.linear_model import LinearRegression
lr = LinearRegression()
lr.fit(X_train, y_train)
# y_pred_lr = lr.predict(X_test)
y_pred_lr = lr.predict(X_train)

# %%
# preds = y_pred_rf
preds = y_pred_lr

# truth = y_test
truth = y_train

fig, ax = plt.subplots(figsize=(8,6))
ax.scatter(truth, preds, s=4)
st.pearsonr(truth, preds)

# %%
fig, ax = plt.subplots(figsize=(8,6))
ax.hist([preds, truth], bins=100)
# ax.hist(truth, bins=100)
# ax.hist(preds, bins=100)
plt.plot;