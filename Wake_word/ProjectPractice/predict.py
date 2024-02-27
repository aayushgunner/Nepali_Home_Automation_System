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
        #inputs = inputs[:,:13, :]
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

    model=keras.models.load_model("last_new.keras")
    print("loaded pre trained model")


    optimiser = keras.optimizers.Adam(learning_rate=0.0001)
    model.compile(optimizer=optimiser,
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.summary()


    #model.save("last.keras")
    haha=predict_data(predict_path)
    predictions = model.predict(haha)
    prediction_labels= np.argmax(predictions, axis = 1)

    confidence = np.max(predictions, axis=1)
    max_confidence_index = np.argmax(confidence)
    min_confidence_index = np.argmin(confidence)
    max_confidence_prediction = prediction_labels[max_confidence_index]
    min_confidence_prediction = prediction_labels[min_confidence_index]
    max_confidence = confidence[max_confidence_index]
    min_confidence = confidence[min_confidence_index]


    #plot accuracy/error for training and validation
    print("\n Predictions")
    print("{}".format(prediction_labels))

    print ("\n Confidence")
    print(confidence);

    print("\nPrediction with maximum confidence:")
    print("Prediction:", max_confidence_prediction)
    print("Confidence:", max_confidence)
    
    if max_confidence_prediction ==2 and max_confidence>0.9999:
        print("dhoka detected")

    elif max_confidence_prediction ==1 and max_confidence>0.9999:
        print("batti detected")
    elif max_confidence_prediction ==2 and max_confidence>0.995 and min_confidence_prediction==2:
        print("dhoka detected")

    elif max_confidence_prediction == 1 and max_confidence>0.995 and min_confidence_prediction ==1:
        print("batti detected")

    elif max_confidence_prediction ==2 and max_confidence > 0.99 and min_confidence_prediction == 0 and min_confidence<0.95:
        print("dhoka detected")

    elif max_confidence_prediction == 1 and max_confidence > 0.99 and min_confidence_prediction ==0 and min_confidence <0.95:
        print("batti detected")
     
    elif max_confidence_prediction ==2 and max_confidence > 0.99 and min_confidence_prediction == 1 and min_confidence<0.95:
        print("dhoka detected")

    elif max_confidence_prediction ==1 and max_confidence > 0.99 and min_confidence_prediction == 2 and min_confidence<0.95:
        print("batti detected")

    

 
    else: print("Give the command again")
    test_loss, test_acc = model.evaluate(X_test, y_test)
    print('\nTest accuracy:', test_acc)
