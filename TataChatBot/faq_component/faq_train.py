# _____TF-IDF libraries_____
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from dashboard.models import FAQ
import pymongo

client = pymongo.MongoClient('localhost', 27017)
mydb = client["TATA_ChatBot"]
records = mydb["dashboard_faq"]


class Faq_Engine():
  def __init__(self):
   pass

  def faq_engine1(self,test_set_sentence):
    # import ipdb
    # ipdb.set_trace()
    sentences = []
    test_set = (test_set_sentence, "")
    all_faq = FAQ.objects.all()
    if len(all_faq)>0:
        for faq in all_faq:
            sentences.append(faq.question)


    # sentences = ['How to revive IPD bill',
    #              'How to reset HOPE Password',
    #              'How to delete vcard request',
    #              'How to fill old claims in UMBS',
    #              'How to access UMBS system on internet',
    #              'How to do timebooking on project',
    #              'Unable to login to mytatamotors',
    #              'Where are the medical benefit policies.',
    #              'Where is Q2T icon',
    #              'How to access OTP portal']



    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix_train = tfidf_vectorizer.fit_transform(sentences)  # finds the tfidf score with normalization
    tfidf_matrix_test = tfidf_vectorizer.transform(test_set)
    cosine = cosine_similarity(tfidf_matrix_test, tfidf_matrix_train)
    cosine = np.delete(cosine, 0)
    max = cosine.max()


    if (max < 0.53):
            new_max = max - 0.20
            response_index = np.where(cosine >= new_max)[0][0]  # list contain the similar elements near to max
            question=sentences[response_index]
            data = FAQ.objects.get(question=str(question))
            return data
    else:
            response_index = np.where(cosine == max)[0][0]  # no offset at all +3
            question = sentences[response_index]
            data = FAQ.objects.get(question=str(question))
            return data



if __name__ == '__main__':

    while 1:
        sentence = input("FAQ Engine  : ")
        faq_obj=Faq_Engine()
        #faq_obj.faq_engine1(sentence)
        a=faq_obj.faq_engine1(sentence)
        print(a)
