# %%
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.stats as st
from encode_sequence import *

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

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
## simplify alphabet
for i in range(len(sequences)):
    sequences[i] = encode4(sequences[i])
times = letters['time']
letters = pd.DataFrame(index=letters.index)
letters['letters'] = sequences
letters['letters_og'] = sequences_og
letters['time'] = times
alphabet = sorted(list(set(sequences[i]) - set(['.'])))

# %%
### USE LETTER POSITIONS AS FEATURES
counts = {1: 'OIAE', # only look for first occurrence
          2: 'JKQXZ',
          3: 'BCFHMPVWY',
          4: 'G',
          5: 'L',
          6: 'DSU',
          8: 'N',
          9: 'TR',
          }
boardletters = ''.join([v*k for k, v in counts.items()])
features = []
for i, l in enumerate(boardletters):
    num = boardletters[:i].count(l) + 1
    features.append(l+str(num))

### ENCODE STRINGS AS LETTER POSITIONS
X1 = pd.DataFrame(index=passed, columns=features,
                 data=np.zeros((len(passed), len(features))))
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
for i in range(w-1):
    new = []
    for k in kmers:
        for l in alphabet:
            new.append(k+l)
    kmers = new

### ENCODE STRINGS AS KMER COUNTS
X2 = pd.DataFrame(index=passed, columns=kmers,
                 data=np.zeros((len(passed), len(kmers))))
for i in passed:
    seq = letters.at[i, 'letters']
    for j in range(len(seq)-w+1):
        X2.at[i, seq[j:j+w]] += 1

# %%
### TRAIN LINEAR REGRESSION MODEL
dataset = pd.merge(X1, X2, left_index=True, right_index=True)
y = letters.loc[passed, 'time'].copy()
X_train, X_test, y_train, y_test = train_test_split(dataset, y, test_size=0.2, random_state=42)

lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred = lr.predict(X_test)

# ### transform y_pred to gamma distribution
# # mu, sigma estimated from preds on y_train
# mu, sigma = (514.7762716465542, 33.62115526633094)
# # shape, loc, scale estimated from y_train
# shape, loc, scale = (11.08962739288571, 271.73724963181337, 21.915887559526098)
# uniform = st.norm.cdf(y_pred, mu, sigma)
# y_pred = st.gamma.ppf(uniform, shape, loc, scale)

# %%
### PLOT TRUE COMPLETION TIMES VS. PREDICTIONS
fig, ax = plt.subplots(figsize=(7,4))
ax.scatter(y_test, y_pred, s=4)
slope, y_int, r = st.linregress(y_test, y_pred)[:3]
x_regress = np.linspace(np.min(y_test), np.max(y_test), 1000)
y_regress = slope*x_regress + y_int
# ax.plot(x_regress, y_regress, color='red')
# ax.plot(y_test, y_test, color='black')
mae = np.mean(np.abs(y_test - y_pred))
# ax.set_title(f'Pearson\'s r: {round(r, 2)}, mean absolute error: {round(mae, 1)}s')
ax.set_xlabel('True completion time (s)', fontsize=12)
ax.set_ylabel('Predicted completion time (s)', fontsize=12)
ax.text(0.96, 0.05, f'Pearson\'s r: {round(r, 2)}\nMean absolute error: {round(mae, 1)}s',
        transform=ax.transAxes, ha='right')