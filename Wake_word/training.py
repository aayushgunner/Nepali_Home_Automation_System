import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from keras import Sequential
from keras.layers import Dense, Activation, Dropout
from sklearn.metrics import confusion_matrix, classification_report


df = pd.read_pickle("final_audio_data_csv/audio_data.csv")                                      #loads saved csv

X = df["feature"].values                                                                        #separating column values in csv
X = np.concatenate(X, axis=0).reshape(len(X), 40)

y = np.array(df["class_label"].tolist())
y = to_categorical(y)                                                                           #one hot encoding 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)       #test train split


model = Sequential([
    Dense(256, input_shape=X_train[0].shape),
    Activation('relu'),
    Dropout(0.5),
    Dense(256),
    Activation('relu'),
    Dropout(0.5),
    Dense(2, activation='softmax')
])

print(model.summary())

model.compile(
    loss="categorical_crossentropy",
    optimizer='adam',
    metrics=['accuracy']
)


history = model.fit(X_train, y_train, epochs=1000)                                              #training
model.save("saved_model/WWD.h5")

print("Model Score: \n")
score = model.evaluate(X_test, y_test)
print(score)

