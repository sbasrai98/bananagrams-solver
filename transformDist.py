# %%
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.stats as st
import pickle

# %%
### FIT NORMAL AND GAMMA DISTRIBUTIONS TO PREDS AND TRUTH
with open('preds.pkl', 'rb') as fin: preds = pickle.load(fin)
with open('truth.pkl', 'rb') as fin: truth = pickle.load(fin)

mu, sigma = st.norm.fit(preds)
x = np.linspace(min(preds), max(preds), 1000)
pdf = st.norm.pdf(x, mu, sigma)
# pdf
fig, ax = plt.subplots(figsize=(8,6))
# ax.hist([preds, truth], bins=100)
ax.hist(preds, bins=100, density=True)
ax.plot(x, pdf, linestyle='-', linewidth=3, color='red')
# plt.plot;

shape, loc, scale = st.gamma.fit(truth)
x = np.linspace(min(truth), max(truth), 1000)
pdf = st.gamma.pdf(x, shape, loc, scale)
# pdf
fig, ax = plt.subplots(figsize=(8,6))
ax.hist(truth, bins=100, density=True)
ax.plot(x, pdf, linestyle='-', linewidth=3, color='red')
plt.plot;

# %%
### SAMPLE FROM ESTIMATED NORMAL DISTRIBUTION AND TRANSFORM TO UNIFORM

sample = st.norm.rvs(mu, sigma, 50000, random_state=42)
uniform = st.norm.cdf(sample, mu, sigma)
fig, ax = plt.subplots(figsize=(8,6))
# ax.hist(uniform, bins=100)
# ax.hist(sample, bins=100)

# sample = st.gamma.rvs(shape, loc, scale, 50000, random_state=42)
# uniform = st.gamma.cdf(sample, shape, loc, scale)
# fig, ax = plt.subplots(figsize=(8,6))
# ax.hist(uniform, bins=100)
# ax.hist(sample, bins=100)

### TRANSFORM UNIFORM DRAWS INTO ESTIMATE GAMMA DISTRIBUTION
gamma = st.gamma.ppf(uniform, shape, loc, scale)
ax.hist([sample, gamma], bins=100)

