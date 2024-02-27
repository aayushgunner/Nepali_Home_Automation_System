import json
import numpy as np
from sklearn.model_selection import train_test_split
import keras
import json
DATA_PATH = "all_mfcc_new.json"
predict_path = "atti.json"

def load_data(data_path):

    with open(data_path, "r") as fp:
        data = json.load(fp)

    X = np.array(data["mfcc"])
    y = np.array(data["labels"])
    return X, y

def predict_data(predict_path):
    with open (predict_path , "r") as fp:
        data=json.load(fp)

        inputs = np.array(data["mfcc"])
        inputs = inputs[:,:13, :]
        return inputs
def prepare_datasets(test_size, validation_size):

    # load data
    X, y = load_data(DATA_PATH)

    # create train, validation and test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
    X_train, X_validation, y_train, y_validation = train_test_split(X_train, y_train, test_size=validation_size)
    X_train = np.array(X_train)
    return X_train, X_validation, X_test, y_train, y_validation, y_test


def build_model(input_shape):

    # build network topology
    model = keras.Sequential()

    # 2 LSTM layers
    model.add(keras.layers.LSTM(64, input_shape=input_shape, return_sequences=True))
    model.add(keras.layers.LSTM(64))

    # dense layer
    model.add(keras.layers.Dense(64, activation='relu'))
    model.add(keras.layers.Dropout(0.3))

    # output layer
    model.add(keras.layers.Dense(3, activation='softmax'))


    return model


if __name__ == "__main__":

    # get train, validation, test splits
    X_train, X_validation, X_test, y_train, y_validation, y_test = prepare_datasets(0.25, 0.2)
 
    # create network
    input_shape = (X_train.shape[1], X_train.shape[2]) # 130, 13

    try:
     model=keras.models.load_model("last_new.keras")
     print("loaded pre trained model")

    except(OSError, IOError):
        print ("Creating a new model")
        model = build_model(input_shape)

    # compile model
    optimiser = keras.optimizers.Adam(learning_rate=0.0001)
    model.compile(optimizer=optimiser,
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.summary()

    # train model
    history = model.fit(X_train, y_train, validation_data=(X_validation, y_validation), batch_size=32, epochs=100)

    model.save("last_new.keras")
   # haha=predict_data(predict_path)
    #predictions = model.predict(haha)
    #prediction_labels= np.argmax(predictions, axis = 1)

    #confidence = np.max(predictions, axis=1)
   # plot accuracy/error for training and validation
    #print("\n Predictions")
    #print("{}".format(prediction_labels))

    #print ("\n Confidence")
    #print(confidence);
   
    #if "{}".format(prediction_labels) == "[1]":
     #   print("Batti detected")

    #elif "{}".format(prediction_labels) == "[2]":
     #   print('Dhoka detected')
    # evaluate model on test set
    test_loss, test_acc = model.evaluate(X_test, y_test)
    print('\nTest accuracy:', test_acc)
