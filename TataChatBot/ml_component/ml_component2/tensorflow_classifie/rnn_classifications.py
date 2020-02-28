from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.datasets import reuters
import keras

def rnn_classification(x_train,y_train, num_classes):
                max_words = 10000
                batch_size = 32
                epochs = 2
                # print(y_train)
                # num_classes = max(y_train) + 1
                # tokenizer = Tokenizer(num_words=max_words)
                # x_train = tokenizer.sequences_to_matrix(x_train, mode='binary')
                # y_train = keras.utils.to_categorical(y_train, num_classes=num_classes)
                model = Sequential()
                model.add(Dense(512, input_shape=(max_words,)))
                model.add(Activation('relu'))
                model.add(Dropout(0.5))
                model.add(Dense(num_classes))
                model.add(Activation('softmax'))
                model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
                model.fit(x_train, y_train, epochs=2, verbose=0)

                return model

        # # (x_train,y_train),(x_test, y_test)= reuters.load_data(num_words=None, test_split=0.2)
        # num_classes =max(y_train)+1
        # # word_index=reuters.get_word_index()
        # # print((x_train,y_train))
        # # index_to_word = {}
        # # for key , value in word_index.items():
        # #     index_to_word[value]=key
        # #
        # # print(index_to_word[43])
        #
        #
        # max_words= 10000
        # tokenizer = Tokenizer(num_words=max_words)
        # x_train= tokenizer.sequences_to_matrix(x_train, mode='binary')
        # # x_test= tokenizer.sequences_to_matrix(x_test, mode='binary')
        #
        # y_train = keras.utils.to_categorical(y_train, num_classes=num_classes)
        # # y_test = keras.utils.to_categorical(y_test, num_classes=num_classes)
        #
        #
        #
        # model = Sequential()
        # model.add(Dense(512, input_shape=(max_words,)))
        # model.add(Activation('relu'))
        # model.add(Dropout(0.5))
        # model.add(Dense(num_classes))
        # model.add(Activation('softmax'))
        # model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        # print(model.metrics_names)
        #
        # batch_size = 32
        # epochs =2
        # history = model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, verbose=1, validation_split=0.1)
        # # score = model.evaluate(x_test,y_test, batch_size=batch_size, verbose=1)
        #
        # # print("test loss : ", score[0])
        # # print("accuracy loss : ", score[1])
        # return  model