# %%
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.preprocessing.sequence import pad_sequences

# %%

# Assuming sequences and times are your data
# sequences: List of sequences of letters
# times: List of total times for each sequence

# Convert letters to numeric values
char_to_int = {char: idx for idx, char in enumerate(set("".join(sequences)))}
sequences_numeric = [[char_to_int[char] for char in sequence] for sequence in sequences]

# Pad sequences to the same length
max_length = max(len(sequence) for sequence in sequences_numeric)
X = pad_sequences(sequences_numeric, maxlen=max_length, padding='post')

# Convert times to numpy array
y = np.array(times)

# Build the LSTM model
model = Sequential()
model.add(LSTM(50, input_shape=(max_length, 1)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

# Reshape input data for LSTM [samples, timesteps, features]
X = np.expand_dims(X, axis=2)

# Train the model
model.fit(X, y, epochs=10, batch_size=32)

# Predict time for a new sequence
new_sequence = "ABCD"
new_sequence_numeric = [char_to_int[char] for char in new_sequence]
new_sequence_padded = pad_sequences([new_sequence_numeric], maxlen=max_length, padding='post')
new_sequence_padded = np.expand_dims(new_sequence_padded, axis=2)
predicted_time = model.predict(new_sequence_padded)

print(predicted_time)
