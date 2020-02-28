# _____TF-IDF libraries_____
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import os
import json
# _____helper Libraries_____
import pickle
import csv
import timeit
import random


class Faq_Engine():
  def __init__(self):
   pass

  def faq_engine1(self,test_set_sentence):
    import ipdb
    ipdb.set_trace()
    csv_file_path1 = os.path.join(os.path.dirname(os.path.dirname(__file__)))
    csv_file_path = csv_file_path1 + "/nlp_engine/" + 'mydata2.csv'
    tfidf_vectorizer_pikle_path = "tfidf_vectorizer11.pickle"
    tfidf_matrix_train_pikle_path ="tfidf_matrix_train11.pickle"
    i = 0
    sentences = []
    test_set = (test_set_sentence, "")
    sentences.append(" No you.")
    sentences.append(" No you.")


    try:
        ##--------------to use------------------#
        f = open(tfidf_vectorizer_pikle_path, 'rb')
        tfidf_vectorizer = pickle.load(f)
        f.close()

        f = open(tfidf_matrix_train_pikle_path, 'rb')
        tfidf_matrix_train = pickle.load(f)
        f.close()

    except:
        # ---------------to train------------------#
        start = timeit.default_timer()

        with open(csv_file_path, "r") as sentences_file:
            reader = csv.reader(sentences_file, delimiter=',')
            for row in reader:
                sentences.append(row[0])
                i += 1

        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix_train = tfidf_vectorizer.fit_transform(sentences)  # finds the tfidf score with normalization


        f = open(tfidf_vectorizer_pikle_path, 'wb')
        pickle.dump(tfidf_vectorizer, f)
        f.close()

        f = open(tfidf_matrix_train_pikle_path, 'wb')
        pickle.dump(tfidf_matrix_train, f)
        f.close()
        # -----------------------------------------#

    tfidf_matrix_test = tfidf_vectorizer.transform(test_set)
    cosine = cosine_similarity(tfidf_matrix_test, tfidf_matrix_train)
    cosine = np.delete(cosine, 0)
    max = cosine.max()
    response_index = 0

    if (max<=0.90):
        a=""
        return a

    else:
        if (max < 0.53):
            new_max = max - 0.20
            list = np.where(cosine >= new_max)  # list contain the similar elements near to max

        else:
            response_index = np.where(cosine == max)[0][0]  # no offset at all +3

    j = 0
    k=0

    with open(csv_file_path, "r") as sentences_file:
        reader = csv.reader(sentences_file, delimiter=',')
        for row in reader:
            j += 1  # we begin with 1 not 0 &    j is initialized by 0
            k += 1
            try:
                if j == response_index :
                 a = row[0],row[1],row[2],row[3],row[4],row[5]

                 return a
                if j==list[0][0]:

                        x =  row[0],row[1],row[2],row[3],row[4],row[5]
                if k == list[0][1]:
                        b =row[0],row[1],row[2],row[3],row[4],row[5]


                        return x,b

            except Exception as e:
                       print("Excepti on in faq ", e)



if __name__ == '__main__':

    while 1:
        sentence = input("FAQ Engine  : ")
        faq_obj=Faq_Engine()
        #faq_obj.faq_engine1(sentence)
        a=faq_obj.faq_engine1(sentence)
        print(a)
