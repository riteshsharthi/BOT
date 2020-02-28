# _____TF-IDF libraries_____
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from dashboard.models import FAQ
import pymongo
import pickle
import time
import timeit
client = pymongo.MongoClient('localhost', 27017)
mydb = client["TATA_ChatBot"]
records = mydb["dashboard_faq"]


class Faq_Engine():
  def __init__(self):
   pass


  def max_cosine_value(self,test_set_sentence):
      sentences = []
      test_set = (test_set_sentence, " ")
      all_faq = FAQ.objects.all()
      if len(all_faq) > 0:
            for faq in all_faq:
                sentences.append(faq.question)

      tfidf_vectorizer = TfidfVectorizer(stop_words='english',encoding='utf-8',decode_error='ignore',lowercase=True,analyzer='word',norm='l1',use_idf=False, smooth_idf=False, sublinear_tf=True)
      tfidf_matrix_train = tfidf_vectorizer.fit_transform(sentences)  # finds the tfidf score with normalization
      stop = timeit.default_timer()
      tfidf_matrix_test = tfidf_vectorizer.transform(test_set)
      cosine = cosine_similarity(tfidf_matrix_train, tfidf_matrix_test)
      max_cosine = cosine.max()

      return max_cosine


  def faq_engine1(self,test_set_sentence):

    sentences = []
    test_set = (test_set_sentence, "")
    all_faq = FAQ.objects.all()
    if len(all_faq)>0:
        for faq in all_faq:
            sentences.append(faq.question)

    # print("sentences : ",len(sentences))
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix_train = tfidf_vectorizer.fit_transform(sentences)  # finds the tfidf score with normalization
    # print("tfidf_matrix_train : ",tfidf_matrix_train)
    tfidf_matrix_test = tfidf_vectorizer.transform(test_set)
    # print("tfidf_matrix_test : ", tfidf_matrix_test)
    cosine = cosine_similarity(tfidf_matrix_test, tfidf_matrix_train)
    cosine = np.delete(cosine, 0)
    print("cosine len : ", len(cosine))
    print("cosine_similarity ---",cosine)
    # print("cosine_similarity dtype ---", type(cosine))
    all_positive = [{index[0]:n} for index, n in np.ndenumerate(cosine) if n > 0.01]
    # print("all_positive : ", all_positive )
    # import ipdb; ipdb.set_trace()
    main_data =[]
    for row_data in all_positive:
        for k, v in row_data.items():
            question = sentences[k + 1]
            data = FAQ.objects.get(question=str(question))
            ts = time.time()
            if data.link:
                link = data.link
            else:
                link = ""

            if data.rank:
                rank= data.rank
            else:
                rank=0

            main_data.append({"question_id": data.id,"faqid":str(ts)[-5:], "type":"link", "link":link, "ans_seq": len(main_data)+1 , "value":data.answer,"retio":round(float(v*100),2), "rank":str(rank)})

    main_data.sort(key=lambda x:x["retio"], reverse = True)

    # print("main_data",main_data[1])
    # max = cosine.max()
    # print("FAQ thresh",max)
    responce_dict ={}
    faq_list=[]
    # if (max > 0.60):
    #         new_max = max - 0.20
    #         response_index = np.where(cosine >= new_max)[0][0]  # list contain the similar elements near to max
    #         # print("index  :", response_index )
    #
    #         # if response_index==0:
    #         #     question = sentences[response_index+1]
    #         # else:
    #         question=sentences[response_index+1]
    #         # print("list :",sentences)
    #         # print("index + 1 :", response_index+1)
    #         data = FAQ.objects.get(question=str(question))
    #         # if data.question != "":
    #         #     responce_dict["question"]=data.question
    #         #     responce_dict["que_seq"] = len(responce_dict)
    #         if data.answer != "":
    #             responce_dict["ans"] = data.answer
    #             responce_dict["ans_seq"] = 1
    #         if data.audio != "":
    #             responce_dict["audio"]=data.audio
    #             responce_dict["audio_seq"] = len(responce_dict)
    #         if data.video != "":
    #             responce_dict["video"]=data.video
    #             responce_dict["video_seq"] = len(responce_dict)
    #         if data.image != "":
    #             responce_dict["img"]=data.image
    #             responce_dict["img_seq"] = len(responce_dict)
    #         if data.link != "":
    #             responce_dict["link"]=data.link
    #             responce_dict["link_seq"] = len(responce_dict)

            # faq_list.append(responce_dict)
            # print(faq_list)

    return main_data



if __name__ == '__main__':

    while 1:
        sentence = input("FAQ Engine  : ")
        faq_obj=Faq_Engine()
        #faq_obj.faq_engine1(sentence)
        a=faq_obj.faq_engine1(sentence)
        print(a)
