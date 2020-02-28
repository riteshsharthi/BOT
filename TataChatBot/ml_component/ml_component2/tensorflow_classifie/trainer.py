import shutil
import numpy as np
import tflearn
import tensorflow as tf
import random
import os
import re
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
import time
from nltk.stem.lancaster import LancasterStemmer
from .dnn_graph import dnn_graph
from .rnn_classifications import rnn_classification
stemmer = LancasterStemmer()
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(os.path.join(base_dir, 'tensorflow_classifie'))
# os.path.join(base_dir, 'tensorflow_classifie')
ERROR_THRESHOLD = 0.55
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base_path = os.path.join(base_dir, 'tensorflow_classifie')
file_path =str(os.path.join(base_path, 'tf_data'))
file_path_model =str(os.path.join(base_path, 'tf_model'))

class TFTrainer(object):

    def __init__(self):
        from nltk.corpus import stopwords
        self.ignore_words =set(stopwords.words('english')) #['?','to','for']
        self.ignore_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}','want','let'])
        self.WH_Words = ["what","why","where","which","when","how","who","whom","whose"]
        # WH_Words2 = [i.capitalize() for i in WH_Words1]
        # self.WH_Words = [k.upper() for k in WH_Words1]+WH_Words2+WH_Words1
        # print("WH_Words", WH_Words)
        # self.remove_words = [self.ignore_words.remove(a) for a in WH_Words if a in self.ignore_words]
        # self.ignore_words=self.remove_words
        # print(list(list(self.ignore_words)-self.remove_words))
        self.meanigful_words = set(nltk.corpus.words.words())
        with open(os.path.join(file_path, "training_data.json")) as json_data:
            intents = json.load(json_data)
        words=[]
        for intent in intents['intents']:
            for pattern in intent['patterns']:
                w = nltk.word_tokenize(pattern)
                words.extend(w)
        self.none_dict_word = [w.lower() for w in words if w not in self.ignore_words]
        self.none_dict_word = list(set([w.lower() for w in self.none_dict_word if w.lower() not in self.meanigful_words]))
        self.meanigful_words = list(self.meanigful_words)+ list(self.none_dict_word)
        self.load_model()

    def main_trainer(self):
        words = []
        classes = []
        documents = []
        with open(os.path.join(file_path ,"training_data.json") ) as json_data :
            intents = json.load(json_data)

        for intent in intents['intents']:
            for pattern in intent['patterns']:
                # tokenize each word in the sentence
                w = nltk.word_tokenize(pattern)
                # add to our words list
                words.extend(w)
                # add to documents in our corpusap
                documents.append((w, intent['tag']))
                # add to our classes list
                if intent['tag'] not in classes:
                    classes.append(intent['tag'])

        words = [w.lower() for w in words if w not in self.ignore_words]

        words = sorted(list(set(words)))
        # remove duplicates
        classes = sorted(list(set(classes)))
        # num_classes= len(classes)+1
        training = []
        output = []
        output_empty = [0] * len(classes)

        # training set, bag of words for each sentence
        for doc in documents:
            # print('for doc:',doc)
            # initialize our bag of words
            bag = []
            # list of tokenized words for the pattern
            pattern_words = doc[0]
            # stem each word
            pattern_words = [word.lower() for word in pattern_words]
            # create our bag of words array
            for w in words:
                bag.append(1) if w in pattern_words else bag.append(0)

            # output is a '0' for each tag and '1' for current tag
            output_row = list(output_empty)
            output_row[classes.index(doc[1])] = 1

            training.append([bag, output_row])

        # shuffle our features and turn into np.array
        random.shuffle(training)
        training = np.array(training)
        
        # create train and test lists
        train_x = list(training[:,0])
        train_y = list(training[:,1])
        # reset underlying graph data
        model = dnn_graph(train_x, train_y)
        # model = rnn_classification(train_x, train_y, num_classes)
        test_dataset=[""]
        # Start training (apply gradient descent algorithm)

        model.fit(train_x, train_y, n_epoch=200, batch_size=3, show_metric=True)
        dump_data = {'words':words, 'classes':classes, 'documents':documents, 'train_x':train_x, 'train_y':train_y}
        # test_loss, test_acc = model.evaluate(test_dataset)
        with open(os.path.join(file_path_model,"model_data"), 'w') as fp:
            json.dump(dump_data, fp, indent=4)
        
        model.save(os.path.join(file_path_model,'model.tflearn'))

    def load_model(self):
        
        if not os.path.exists(os.path.join(file_path_model,"model.tflearn.index")):
            self.main_trainer()
        
        with open(os.path.join(file_path_model,"model_data"),"r") as fp:
            dump_data = json.load(fp)

        self.classes = dump_data["classes"]
        self.words = dump_data["words"]
        self.documents=dump_data["documents"]
        self.model = dnn_graph(dump_data["train_x"], dump_data["train_y"])
        self.model.load(os.path.join(file_path_model,'model.tflearn'))



    def tester_for_controller(self, sentence):
        results = self.model.predict([self.bow(sentence, self.words)])[0]
        max_intent_score=results.max()
        return max_intent_score

    def prob_mean(self,sentence):

        stop_words = set(stopwords.words('english'))

        print("stop_words",type(list(stop_words)))
        # print("------",[dd for dd in list(set(stop_words)) if dd not in list(set(self.WH_Words))])
        stop_words_new = [dd for dd in list(set(stop_words)) if dd.lower() not in list(set(self.WH_Words))]

        word_tokens = word_tokenize(sentence.lower())
        set_words = set(word_tokens)
        print("length of NLTK Words", len(self.meanigful_words))
        print("sentenec word",[ww for ww in list(set_words) if ww in self.meanigful_words])

        filtered_sentence = [w for w in word_tokens if w not in stop_words_new]
        remaing_words = [ww for ww in list(filtered_sentence) if ww in self.meanigful_words]
        # filtered_sentence = []
        # for w in word_tokens:

        #     if w not in self.ignore_words:
        #         filtered_sentence.append(w)
        print("filtered_sentence_____",filtered_sentence)
        data_dict_for_word ={}
        if len(filtered_sentence)==len(remaing_words):
            try:
                for i in filtered_sentence:
                    results_d = self.model.predict([self.bow(i, self.words)])
                    results_ddd = [[i, r] for i, r in enumerate(results_d[0])]
                    results_ddd.sort(key=lambda x: x[1], reverse=True)
                    return_list_dd = []
                    for r in results_ddd:
                        return_list_dd.append((self.classes[r[0]], r[1]))

                    data_dict_for_word[i]=return_list_dd
                print("DataFream \n ", pd.DataFrame(data_dict_for_word))
            except Exception as e:
                print("Exception in filtered_sentence",e)
            filter_data_intent = {}
            try:

                for k, v in data_dict_for_word.items():
                    for vv in v:
                        if vv[0] in filter_data_intent:
                            filter_data_intent[vv[0]].append(vv[1])
                        else:
                            filter_data_intent[vv[0]]=[vv[1]]
            except Exception as e:
                print("Exception in filter_data_intent", e)
            filnal_data = []
            try:

                for k1,v1 in filter_data_intent.items():
                    filnal_data.append((k1,sum(v1)/len(v1)))

                print("filnal_data",filnal_data)
                print("filnal_data length ", len(filnal_data))
            except Exception as e:
                print("Exception in filnal_data", e)
        else:
            filnal_data=[]
        return filnal_data

    def tester(self, sentence):
        Multi_THRESHOLD = 0.50
        Single_THRESHOLD = 0.90
        return_list_dd= self.prob_mean(sentence)
        print("@@@ return_list_dd @@@  ", return_list_dd)
        # print(self.meanigful_words)
        results_ddd = [[i[0], i[1]] for i in return_list_dd if float(i[1]) > Multi_THRESHOLD]
        print("results_ddd", results_ddd)

        All_Predicted_Results = self.model.predict([self.bow(sentence, self.words)])
        # print("@@@@@results_d@@@@@", All_Predicted_Results)
        Results_Single_THRESHOLD= [[i, r] for i, r in enumerate(All_Predicted_Results[0]) if float(r) > Single_THRESHOLD ]
        Results_Multi_THRESHOLD = [[i, r] for i, r in enumerate(All_Predicted_Results[0]) if float(r) > Multi_THRESHOLD]
        print(" Results_Single_THRESHOLD ", Results_Single_THRESHOLD)
        print(" Results_Multi_THRESHOLD ", Results_Multi_THRESHOLD)
        Results_Send=[]
        if Results_Single_THRESHOLD:
            Results_Send= Results_Single_THRESHOLD
        else:
            Results_Send=Results_Multi_THRESHOLD
        # print("result in tensorflow@@@@@SSDDDD",results_ddd, "-len--", len(results_ddd),"-----",dddd)
        Results_Multi_THRESHOLD.sort(key=lambda x: x[1], reverse=True)
        Return_List_Intent =[]
        for r in Results_Send:
            Return_List_Intent.append((self.classes[r[0]], r[1]))

        # print("All Intent -- : ",Return_List_Intent)

        # results = self.model.predict([self.bow(sentence, self.words)])[0]
        # filter out predictions below a threshold
        # results = [[i, r] for i, r in enumerate(results) if r > ERROR_THRESHOLD]
        # sort by strength of probability
        # print("@@@@@SS",results)
        # results.sort(key=lambda x: x[1], reverse=True)
        # return_list = []
        # for r in results:
        #     return_list.append((self.classes[r[0]], r[1]))

        # return Return_List_Intent
        return results_ddd

    def clean_up_sentence(self, sentence): 
        # tokenize the pattern
        sentence_words = nltk.word_tokenize(sentence)
        # stem each word
        sentence_words = [word.lower() for word in sentence_words]
        return sentence_words
        
    def bow(self, sentence, words, show_details=False):
        # tokenize the pattern
        sentence_words = self.clean_up_sentence(sentence)
        # bag of words
        bag = [0]*len(words)
        for s in sentence_words:
            for i,w in enumerate(words):
                if w == s:
                    bag[i] = 1
                    if show_details:
                        print("found in bag: %s" % w)

        return(np.array(bag))

# if __name__ == "__main__":
#     obj = TFTrainer()
#     print(obj.tester("job for puna plant"))
