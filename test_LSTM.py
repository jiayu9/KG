import re
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical

# Define the path to the input file
input_file_path = 'processed_data.txt'

# Read and process the content of the file
rule_heads = []
rule_bodies = []
with open(input_file_path, 'r') as file:
    lines = file.readlines()
    for line in lines:
        if '<-' in line:
            head, body = line.split('<-', 1)
            rule_heads.append(head.strip())
            rule_bodies.append(body.strip())

# Tokenize the text
tokenizer = Tokenizer()
tokenizer.fit_on_texts(rule_heads + rule_bodies)
rule_heads_seq = tokenizer.texts_to_sequences(rule_heads)
rule_bodies_seq = tokenizer.texts_to_sequences(rule_bodies)

# Pad the sequences
max_seq_length = max(max(len(seq) for seq in rule_heads_seq), max(len(seq) for seq in rule_bodies_seq))
rule_heads_seq_padded = pad_sequences(rule_heads_seq, maxlen=max_seq_length, padding='post')
rule_bodies_seq_padded = pad_sequences(rule_bodies_seq, maxlen=max_seq_length, padding='post')

# Convert targets to one-hot encoded format
rule_heads_seq_padded = to_categorical(rule_heads_seq_padded, num_classes=len(tokenizer.word_index) + 1)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(rule_bodies_seq_padded, rule_heads_seq_padded, test_size=0.2, random_state=42)


# Define the LSTM model
vocab_size = len(tokenizer.word_index) + 1
embedding_dim = 100

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, embedding_dim),
    tf.keras.layers.LSTM(128, return_sequences=True),
    tf.keras.layers.LSTM(128),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(vocab_size, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.summary()


# Train the model
history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test))


# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test Loss: {loss}')
print(f'Test Accuracy: {accuracy}')
