# %%
import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.optimizers import Adam

import matplotlib as mpl
import matplotlib.pyplot as plt

# %%
# Assuming sequences and times are your data
# sequences: List of sequences of letters
# times: List of total times for each sequence

mydir = '/Users/sbasrai/Desktop/projects/bananagrams-solver/gamesets/2k/games/'
# mydir = 'fails/'

times = []
sequences = []

games = [x for x in os.listdir(mydir) if x[0].isupper()]
for g in games:
    with open(mydir+g+'/total_time.txt') as fin:
        lines = fin.readlines()
        times.append(float(lines[0].rstrip()))
        sequences.append(lines[1].rstrip())

# %%
# Convert letters to numeric values
char_to_int = {char: idx for idx, char in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}
sequences_numeric = [[char_to_int[char] for char in sequence] for sequence in sequences]

# Pad sequences to the same length
max_length = max(len(sequence) for sequence in sequences_numeric)
X = pad_sequences(sequences_numeric, maxlen=max_length, padding='post')

# Convert times to numpy array
y = np.array(times)

# Reshape input data for LSTM [samples, timesteps, features]
X = np.expand_dims(X, axis=2)

# %%
# Build the LSTM model
model = Sequential()
model.add(LSTM(128, return_sequences=True, input_shape=(max_length, 1)))
model.add(Dropout(0.3))
model.add(LSTM(64, return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(32))
model.add(Dropout(0.3))
model.add(Dense(1))
optimizer = Adam(learning_rate=0.001)
model.compile(optimizer=optimizer, loss='mean_squared_error')



# %%

# Train the model
model.fit(X, y, epochs=100, batch_size=64, validation_split=0.2)



# %%
# LOAD TEST SET
testdir = '/Users/sbasrai/Desktop/projects/bananagrams-solver/testset/'

test_times = []
test_sequences = []

games = [x for x in os.listdir(testdir) if x[0].isupper()]
for g in games:
    with open(testdir+g+'/total_time.txt') as fin:
        lines = fin.readlines()
        test_times.append(float(lines[0].rstrip()))
        test_sequences.append(lines[1].rstrip())

# %%

predictions = []
for new_sequence in test_sequences:
    # Predict time for a new sequence
    # new_sequence = "ABCD"
    new_sequence_numeric = [char_to_int[char] for char in new_sequence]
    new_sequence_padded = pad_sequences([new_sequence_numeric], maxlen=max_length, padding='post')
    new_sequence_padded = np.expand_dims(new_sequence_padded, axis=2)
    predicted_time = model.predict(new_sequence_padded)
    predictions.append(predicted_time)

# %%

fig, ax = plt.subplots(figsize=(8,8))
ax.scatter(test_times, predictions)
