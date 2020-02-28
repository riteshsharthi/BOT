import re
import os
import sys
import glob
import json
import string
import numpy as np
import nltk
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from many_stop_words import get_stop_words
from nltk.tokenize import wordpunct_tokenize
from pprint import pprint

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base_path_data = os.path.join(base_dir, 'initial_classifirer', 'data')

"""
Class to perform pickle operations
"""
class LogisticClassifier():
    def __init__(self):
        self.labels = list(filter(lambda x: not (x.endswith("~") or x.startswith("client")), os.listdir(base_path_data)))
        self.vectorizer = TfidfVectorizer( max_features = None, strip_accents = 'unicode',
                            analyzer = "word", ngram_range=(1,1), use_idf = 1, smooth_idf = 1, tokenizer=self.tokenize, stop_words='english') 
    
    def tokenize(self, text):
        text = text.lower()
        tokens = []
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        stop_words = set(get_stop_words('en'))
        stop_words_punct = [s for s in string.punctuation]
        text = re.sub(r'\.',' ', text)
        text = re.sub(r'\s+',' ', text)
        sents = sent_detector.tokenize(text.strip())
        # print sents[0:1]
        for stext in sents[0:1]:
            # tokens += filter(lambda x: x not in stop_words, wordpunct_tokenize(stext))
            tokens += wordpunct_tokenize(stext)
        return tokens
    
    def getData(self):
        xdata = []
        ydata = []
        train_path = base_path_data
        try:
            for ifile in self.labels:
                with open(os.path.join(train_path,ifile),"r") as tf:


                    tmpdata = tf.readlines()
                tmpdata = [ i.replace("\n","") for i in tmpdata ]
                tmpdata = [ i for i in tmpdata if i != "" ]
                for i in tmpdata:
                    xdata.append(i)
                    ydata.append(self.labels.index(ifile))
        except:
            import traceback
            print (traceback.format_exc())
        
        return xdata, ydata
        
    """
    Function to train classifier
    """
    def train(self):
        X_train, Y_train = self.getData()
        vectors_train = self.vectorizer.fit_transform(X_train)
        self.classifier = OneVsRestClassifier( LogisticRegression( C = 10.0, multi_class = "multinomial", solver = "lbfgs" ) )
        self.classifier.fit(vectors_train, Y_train)
        # print "logostic classifier accuracy=====>",self.classifier.score(vectors_train, Y_train)

    """
    Function to test classifier
    """
    def test(self, query):
        modifier_dict = {"general.text":"general",
                         "subjective.text":"product"
           
        }
        self.train()
        classifier_result = {}
        vectors_test = self.vectorizer.transform([query])
        pred = self.classifier.predict(vectors_test)
        predp = self.classifier.predict_proba(vectors_test)
        predp = predp.tolist()[0]
        max_ind =  predp.index(max(predp))
        classifier_result["class"] = modifier_dict[self.labels[max_ind]]
        classifier_result["prediction"] = {self.labels[max_ind]: round(max(predp)*100.0, 2)*0.6}
        # with_confidence,with_confusion = max(predp),max(filter(lambda n:n != max(predp),predp))
        # confident_on,confused_on = modifier_dict[self.labels[predp.index(with_confidence)]],modifier_dict[self.labels[predp.index(with_confusion)]]
        # classifier_result =  [confident_on, confused_on] if (with_confidence - with_confusion) < .05 else [confident_on]
        # print dict(zip([confident_on, confused_on], [with_confidence,with_confusion])) , classifier_result
        return classifier_result


if __name__ == '__main__':
        while(True):
            qr = input("=>")
            result = LogisticClassifier()
            d = result.test(qr)
            print (d)
            
            
            
