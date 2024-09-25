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
### GENERATE ALL 3-MERS

# test = [i+j+k for i in alphabet for j in alphabet for k in alphabet]
kmers = alphabet[:]
w = 3
for i in range(w-1): # easier to try different values..
    new = []
    for k in kmers:
        for l in alphabet:
            new.append(k+l)
    kmers = new
print(len(kmers))

# %%
### CONVERT STRINGS TO KMER COUNTS
X = pd.DataFrame(index=passed, columns=kmers,
                 data=np.zeros((len(passed), len(kmers))))
for i in passed:
    seq = letters.at[i, 'letters']
    for j in range(len(seq)-w+1):
        X.at[i, seq[j:j+w]] += 1

y = letters.loc[passed, 'time'].copy()
ylog = np.log(y)

# kmer_counts = np.sum(X, axis=0).sort_values(ascending=False)
# fig, ax = plt.subplots(figsize=(6,6))
# ax.plot(kmer_counts)

# %%
# add pos of JKQXZ (10 additional features)
X2 = X.copy()
X2['J1'] = X2['J2'] = X2['K1'] = X2['K2'] = X2['Q1'] = X2['Q2'] = \
    X2['X1'] = X2['X2'] = X2['Z1'] = X2['Z2'] = pd.NA
for i in passed[:]:
    seq = letters.at[i, 'letters_og']
    for l in 'JKQXZ':
        idx = [i for i in range(len(seq)) if seq[i] == l]
        for num in [0,1]:
            X2.at[i, l+str(num+1)] = idx[num]

# for colo in ['J1','J2','K1','K2','Q1','Q2','X1','X2','Z1','Z2']:
#     print(colo, st.pearsonr(X2[colo], y)[0])

# %%
## get r for each variable vs times independently..
corrs = pd.DataFrame(index=X.columns, columns=['r','mag'])
for col in X.columns:
    r, p = st.pearsonr(X[col], y)
    corrs.at[col, 'r'] = r
    corrs.at[col, 'mag'] = np.abs(r)
usecols = corrs.sort_values(by='mag', ascending=False).iloc[:,:]
usecols
# usecols.index

# 0.2445560831755841 leave off 3
# %%
# only keep columns with a 3 in it?
# cols_with_3 = [x for x in X.columns if '3' in x]
# X = X.loc[:,cols_with_3]
# X2 = X.loc[:, usecols.index]
# X2 = X2.iloc[:, 27:]

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X2, y, test_size=0.2, random_state=42)
# X_train, X_test, y_train, y_test = train_test_split(X, ylog, test_size=0.2, random_state=42)

# %%
### DIMENSIONALITY REDUCTION WITH PCA
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

scaler = StandardScaler()
scaled_data = scaler.fit_transform(X_train)

pca = PCA(n_components=500)
# Fit the PCA model to the data and transform it
data_pca = pca.fit_transform(scaled_data)
# print("Principal Components:\n", data_pca)
# print("Explained Variance Ratio:\n", pca.explained_variance_ratio_)
# print("Principal Axes (components):\n", pca.components_)

# PREPARE TEST SET
scaled_test = scaler.transform(X_test)
pca_test = pca.transform(scaled_test)

# %%
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_classification

rf = RandomForestRegressor(n_estimators=500, max_leaf_nodes=None,
                                 n_jobs=-1, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

# rf.fit(data_pca, y_train)
# y_pred_rf = rf.predict(pca_test)

# %%
from sklearn.linear_model import LinearRegression
lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)


# from sklearn.preprocessing import PolynomialFeatures
# poly_features = PolynomialFeatures(degree=2, include_bias=False)
# X_train_poly = poly_features.fit_transform(X_train)
# lr = LinearRegression()
# lr.fit(X_train_poly, y_train)
# X_test_poly = poly_features.fit_transform(X_test)
# y_pred_lr = lr.predict(X_test_poly)


# %%
from sklearn.linear_model import Lasso
lasso = Lasso(alpha=0.001, max_iter=3000, tol=1e-9)
lasso.fit(X_train, y_train)
y_pred_ls = lasso.predict(X_test)

# lasso.fit(data_pca, y_train)
# y_pred_ls = lasso.predict(pca_test)

# %%
from sklearn.linear_model import ElasticNet
en = ElasticNet(alpha=0.01, l1_ratio=0.999, max_iter=5000)
en.fit(X_train, y_train)
y_pred_en = en.predict(X_test)

# en.fit(data_pca, y_train)
# y_pred_en = en.predict(pca_test)


# %%
from sklearn import ensemble

params = {
    "n_estimators": 100,
    "max_depth": 7,
    "min_samples_split": 5,
    "learning_rate": 0.01,
    "loss": "squared_error",
}

gb = ensemble.GradientBoostingRegressor(**params)
gb.fit(X_train, y_train)
y_pred_gb = gb.predict(X_test)

# %%
# preds = y_pred_rf
preds = y_pred_lr
# preds = np.exp(y_pred_lr)
# preds = y_pred_ls
# preds = y_pred_en
# preds = y_pred_gb
fig, ax = plt.subplots(figsize=(8,6))
ax.scatter(y_test, preds, s=4)
st.pearsonr(y_test, preds)

# preds = preds ** 1.04
# ax.scatter(y_test, preds, s=4)
# st.pearsonr(y_test, preds)


# ax.scatter(np.exp(y_test), preds, s=4)
# st.pearsonr(np.exp(y_test), preds)

# encode2, w=3, 0.24096269643535118
# encode3, w=3, 0.2431318548515956

# split data evenly
# try polynomial regression
# k fold CV 