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
import requests
#import os
class Faq_Engine():
  def __init__(self):
   pass
  def faq_engine1(self,test_set_sentence):
    # import pdb
    # pdb.set_trace()
    #csv_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'mydata2.csv')
    #print(csv_file_path)
    csv_file_path1 = os.path.join(os.path.dirname(os.path.dirname(__file__)))
    csv_file_path = csv_file_path1 + "/nlp_engine/" + 'mydata2.csv'
    # print("csv_file_path--->", csv_file_path)
    tfidf_vectorizer_pikle_path = "tfidf_vectorizer11.pickle"
    tfidf_matrix_train_pikle_path ="tfidf_matrix_train11.pickle"

    i = 0
    sentences = []

    # enter your test sentence
    test_set = (test_set_sentence, "")

    # 3ashan yzabt el indexes
    sentences.append(" No you.")
    sentences.append(" No you.")
    # import pdb
    # pdb.set_trace()

    try:
        ##--------------to use------------------#
        f = open(tfidf_vectorizer_pikle_path, 'rb')
        tfidf_vectorizer = pickle.load(f)
        f.close()

        f = open(tfidf_matrix_train_pikle_path, 'rb')
        tfidf_matrix_train = pickle.load(f)
        f.close()
        # ----------------------------------------#
    except:
        # ---------------to train------------------#
        start = timeit.default_timer()

        # enter jabberwakky sentence
        with open(csv_file_path, "r") as sentences_file:
            reader = csv.reader(sentences_file, delimiter=',')
            # reader.next()
            # reader.next()
            for row in reader:
                # if i==stop_at_sentence:
                #    break
                sentences.append(row[0])
                i += 1

        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix_train = tfidf_vectorizer.fit_transform(sentences)  # finds the tfidf score with normalization
        # tfidf_matrix_test =tfidf_vectorizer.transform(test_set)
        stop = timeit.default_timer()
        print ("training time took was : ")
        print (stop - start)

        f = open(tfidf_vectorizer_pikle_path, 'wb')
        pickle.dump(tfidf_vectorizer, f)
        f.close()

        f = open(tfidf_matrix_train_pikle_path, 'wb')
        pickle.dump(tfidf_matrix_train, f)
        f.close()
        # -----------------------------------------#

    tfidf_matrix_test = tfidf_vectorizer.transform(test_set)

    cosine = cosine_similarity(tfidf_matrix_test, tfidf_matrix_train)
    print(cosine)

    cosine = np.delete(cosine, 0)
    max = cosine.max()
    response_index = 0

    ############AAA#######
    if (max<=0.90):
        #print("hi")
        a=""
        #print("- Not in FAQ")
        return a

    else:

        if (max < 0.53):
            new_max = max - 0.20
            list = np.where(cosine >= new_max)  # list contain the similar elements near to max
            print("Total list------->",list)
            #print(type(list))
            # print("list:", str(list))
            print("list[0]:", list[0][0])  # list [0][1] <--- 1st block [0] is for row    #list  [0][0]  <--- 2nd block [1] is for element index
            #for i in list:
            #print(i[1])
            # i+=1
            #print("number of Similar responses with difference of 0.01 from max = " + str(list[0].size))
            #response_index = random.choice(list[0])
            # response_index=list[0]
            #response_index1 = list[0][0]
            #print("response index-->", response_index1)
            #response_index2 = list[0][1]
            #print("response Index2- ", response_index2)
            # response_index=(list)
        else:
            # # print ("not sure")
            # print ("max is = " + str(max))
            response_index = np.where(cosine == max)[0][0]  # no offset at all +3
            #print("response_index-->",response_index)


    j = 0
    k=0

    with open(csv_file_path, "r") as sentences_file:
        reader = csv.reader(sentences_file, delimiter=',')
        for row in reader:
            j += 1  # we begin with 1 not 0 &    j is initialized by 0
            k += 1
            try:
                if j == response_index :
                 #a=row[0], row[1], response_index1
                 a = row[0],row[1],row[2],row[3],row[4],row[5]
                 #print("1st if")
                 # response_data={"response_text":a}
                 # json_response=json.dump(response_data)
                 #print(json_response)
                 #print("- ",a)
                 return a
                if j==list[0][0]:
                #         #print("response_index2",response_index2)
                #         #print("2st if")
                #         #b = row[0], row[1], response_index2
                        x =  row[0],row[1],row[2],row[3],row[4],row[5]
                if k == list[0][1]:
                        b =row[0],row[1],row[2],row[3],row[4],row[5]
                #         # response_data = {"response_text": b}
                #         # json_response = json.dump(response_data)
                #         # print(json_response)
                #         print("-a ", a)
                #         print("-b ",b)
                        print("------->",x)
                        print("------->",b)

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

# _____TF-IDF libraries_____
#
#
#
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.feature_extraction.text import TfidfVectorizer
# import numpy as np
#
# # _____helper Libraries_____
# import pickle
# import csv
# import timeit
# import random
#
#
# import os
# class Faq_Engine():
#     def __init__(self):
#         pass
#     def faq_engine1(self,test_set_sentence):
#         csv_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mydata.csv')
#         #csv_file_path = "FAQ/mydata.csv"
#         tfidf_vectorizer_pikle_path = "tfidf_vectorizer1.pickle"
#         tfidf_matrix_train_pikle_path = "tfidf_matrix_train1.pickle"
#
#         i = 0
#         sentences = []
#
#         # enter your test sentence
#         test_set = (test_set_sentence, "")
#
#         # 3ashan yzabt el indexes
#         sentences.append(" No you.")
#         sentences.append(" No you.")
#
#         try:
#             ##--------------to use------------------#
#             f = open(tfidf_vectorizer_pikle_path, 'rb')
#             tfidf_vectorizer = pickle.load(f)
#             f.close()
#
#             f = open(tfidf_matrix_train_pikle_path, 'rb')
#             tfidf_matrix_train = pickle.load(f)
#             f.close()
#             # ----------------------------------------#
#         except:
#             # ---------------to train------------------#
#             start = timeit.default_timer()
#
#             # enter jabberwakky sentence
#             with open(csv_file_path, "r") as sentences_file:
#                 reader = csv.reader(sentences_file, delimiter=',')
#                 # reader.next()
#                 # reader.next()
#                 for row in reader:
#                     # if i==stop_at_sentence:
#                     #    break
#                     sentences.append(row[0])
#                     i += 1
#
#             tfidf_vectorizer = TfidfVectorizer()
#             tfidf_matrix_train = tfidf_vectorizer.fit_transform(sentences)  # finds the tfidf score with normalization
#             # tfidf_matrix_test =tfidf_vectorizer.transform(test_set)
#             stop = timeit.default_timer()
#             # print ("training time took was : ")
#             # print (stop - start)
#
#             f = open(tfidf_vectorizer_pikle_path, 'wb')
#             pickle.dump(tfidf_vectorizer, f)
#             f.close()
#
#             f = open(tfidf_matrix_train_pikle_path, 'wb')
#             pickle.dump(tfidf_matrix_train, f)
#             f.close()
#             # -----------------------------------------#
#
#         tfidf_matrix_test = tfidf_vectorizer.transform(test_set)
#
#         cosine = cosine_similarity(tfidf_matrix_test, tfidf_matrix_train)
#         # print(cosine)
#
#         cosine = np.delete(cosine, 0)
#         max = cosine.max()
#         response_index = 0
#
#         ############AAA#######
#         if (max <= 0.20):
#          print("- Not in FAQ")
#
#         else:
#
#            if (max < 0.49):
#                 new_max = max - 0.01
#                 list = np.where(cosine >= new_max)  # list contain the similar elements near to max
#                 # print(type(list))
#                 # print("list:", str(list))
#                 # print("list[0]:", list[0][0])  # list [0][1] <--- 1st block [0] is for row    #list  [0][0]  <--- 2nd block [1] is for element index
#                 # for i in list:
#                 #     print(i[1])
#                 # i+=1
#                 # print("number of Similar responses with difference of 0.01 from max = " + str(list[0].size))
#                 # response_index = random.choice(list[0])
#                 # response_index=list[0]
#                 # response_index1 = list[0][0]
#                 # print("response index-->", response_index1)
#                 # response_index2 = list[0][1]
#                 # print("response Index2- ", response_index2)
#                 # response_index=(list)
#            else:
#               #print ("not sure")
#               #print ("max is = " + str(max))
#               response_index = np.where(cosine == max)[0][0]  # no offset at all +3
#
#         j = 0
#         k = 0
#
#         with open(csv_file_path, "r") as sentences_file:
#              reader = csv.reader(sentences_file, delimiter=',')
#              for row in reader:
#                  j += 1  # we begin with 1 not 0 &    j is initialized by 0
#                  k += 1
#                  try:
#                      if j == response_index or j == list[0][0]:
#                        #a=row[0], row[1], response_index1
#                        a = row[1],row[2]
#                        # print("1st if")
#                        print("- ", a)
#
#                      if k == list[0][1]:
#                        # print("response_index2",response_index2)
#                        # print("2st if")
#                        # b = row[0], row[1], response_index2
#                        b = row[1],row[2]
#                        print("- ", b)
#                  except Exception as e:
#                               e
#
#
# #
# if __name__ == '__main__':
#
#     while 1:
#         sentence = input("FAQ Engine  : ")
#         faq_obj=Faq_Engine()
#         #faq_obj.faq_engine1(sentence)
#         a=faq_obj.faq_engine1(sentence)
#         print(a)
#








# # _____TF-IDF libraries_____
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.feature_extraction.text import TfidfVectorizer
# import numpy as np
# import os
# import json
# # _____helper Libraries_____
# import pickle
# import csv
# import timeit
# import random
# import requests
# #import os
# class Faq_Engine():
#   def __init__(self):
#    pass
#   def faq_engine1(self,test_set_sentence):
#
#     csv_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'mydata.csv')
#     tfidf_vectorizer_pikle_path = "tfidf_vectorizer1.pickle"
#     tfidf_matrix_train_pikle_path ="tfidf_matrix_train1.pickle"
#
#     i = 0
#     sentences = []
#
#     # enter your test sentence
#     test_set = (test_set_sentence, "")
#
#     # 3ashan yzabt el indexes
#     sentences.append(" No you.")
#     sentences.append(" No you.")
#
#     try:
#         ##--------------to use------------------#
#         f = open(tfidf_vectorizer_pikle_path, 'rb')
#         tfidf_vectorizer = pickle.load(f)
#         f.close()
#
#         f = open(tfidf_matrix_train_pikle_path, 'rb')
#         tfidf_matrix_train = pickle.load(f)
#         f.close()
#         # ----------------------------------------#
#     except:
#         # ---------------to train------------------#
#         start = timeit.default_timer()
#
#         # enter jabberwakky sentence
#         with open(csv_file_path, "r") as sentences_file:
#             reader = csv.reader(sentences_file, delimiter=',')
#             # reader.next()
#             # reader.next()
#             for row in reader:
#                 # if i==stop_at_sentence:
#                 #    break
#                 sentences.append(row[0])
#                 i += 1
#
#         tfidf_vectorizer = TfidfVectorizer()
#         tfidf_matrix_train = tfidf_vectorizer.fit_transform(sentences)  # finds the tfidf score with normalization
#         # tfidf_matrix_test =tfidf_vectorizer.transform(test_set)
#         stop = timeit.default_timer()
#         print ("training time took was : ")
#         print (stop - start)
#
#         f = open(tfidf_vectorizer_pikle_path, 'wb')
#         pickle.dump(tfidf_vectorizer, f)
#         f.close()
#
#         f = open(tfidf_matrix_train_pikle_path, 'wb')
#         pickle.dump(tfidf_matrix_train, f)
#         f.close()
#         # -----------------------------------------#
#
#     tfidf_matrix_test = tfidf_vectorizer.transform(test_set)
#
#     cosine = cosine_similarity(tfidf_matrix_test, tfidf_matrix_train)
#     #print(cosine)
#
#     cosine = np.delete(cosine, 0)
#     max = cosine.max()
#     response_index = 0
#
#     ############AAA#######
#     if (max<=0.20):
#         a=""
#         #print("- Not in FAQ")
#         return a
#
#     else:
#
#         if (max < 0.49):
#             new_max = max - 0.01
#             list = np.where(cosine >= new_max)  # list contain the similar elements near to max
#             #print(type(list))
#             # print("list:", str(list))
#             # print("list[0]:", list[0][0])  # list [0][1] <--- 1st block [0] is for row    #list  [0][0]  <--- 2nd block [1] is for element index
#             # for i in list:
#             #     print(i[1])
#             # i+=1
#             #print("number of Similar responses with difference of 0.01 from max = " + str(list[0].size))
#             #response_index = random.choice(list[0])
#             # response_index=list[0]
#             #response_index1 = list[0][0]
#             #print("response index-->", response_index1)
#             #response_index2 = list[0][1]
#             #print("response Index2- ", response_index2)
#             # response_index=(list)
#         else:
#             # # print ("not sure")
#             # print ("max is = " + str(max))
#             response_index = np.where(cosine == max)[0][0]  # no offset at all +3
#
#
#     j = 0
#     k=0
#
#     with open(csv_file_path, "r") as sentences_file:
#         reader = csv.reader(sentences_file, delimiter=',')
#         for row in reader:
#             j += 1  # we begin with 1 not 0 &    j is initialized by 0
#             k += 1
#             try:
#                 if j == response_index or j==list[0][0]:
#                  #a=row[0], row[1], response_index1
#                  a = row[1],row[2]
#                  #print("1st if")
#                  # response_data={"response_text":a}
#                  # json_response=json.dump(response_data)
#                  #print(json_response)
#                  #print("- ",a)
#                  return a
#
#                 if k==list[0][1]:
#                         #print("response_index2",response_index2)
#                         #print("2st if")
#                         #b = row[0], row[1], response_index2
#                         b = row[1],row[2]
#                         # response_data = {"response_text": b}
#                         # json_response = json.dump(response_data)
#                         # print(json_response)
#                         #print("- ",b)
#                         return b
#
#             except Exception as e:
#                              e
#
#
# #
# if __name__ == '__main__':
#
#     while 1:
#         sentence = input("FAQ Engine  : ")
#         faq_obj=Faq_Engine()
#         #faq_obj.faq_engine1(sentence)
#         a=faq_obj.faq_engine1(sentence)
#         print(a)




























# # _____TF-IDF libraries_____
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.feature_extraction.text import TfidfVectorizer
# import numpy as np
# import os
# import json
# # _____helper Libraries_____
# import pickle
# import csv
# import timeit
# import random
# import requests
# #import os
# class Faq_Engine():
#   def __init__(self):
#    pass
#   def faq_engine1(self,test_set_sentence):
#
#     csv_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'mydata2.csv')
#     tfidf_vectorizer_pikle_path = "tfidf_vectorizer11.pickle"
#     tfidf_matrix_train_pikle_path ="tfidf_matrix_train11.pickle"
#
#     i = 0
#     sentences = []
#
#     # enter your test sentence
#     test_set = (test_set_sentence, "")
#
#     # 3ashan yzabt el indexes
#     sentences.append(" No you.")
#     sentences.append(" No you.")
#     # import pdb
#     # pdb.set_trace()
#
#     try:
#         ##--------------to use------------------#
#         f = open(tfidf_vectorizer_pikle_path, 'rb')
#         tfidf_vectorizer = pickle.load(f)
#         f.close()
#
#         f = open(tfidf_matrix_train_pikle_path, 'rb')
#         tfidf_matrix_train = pickle.load(f)
#         f.close()
#         # ----------------------------------------#
#     except:
#         # ---------------to train------------------#
#         start = timeit.default_timer()
#
#         # enter jabberwakky sentence
#         with open(csv_file_path, "r") as sentences_file:
#             reader = csv.reader(sentences_file, delimiter=',')
#             # reader.next()
#             # reader.next()
#             for row in reader:
#                 # if i==stop_at_sentence:
#                 #    break
#                 sentences.append(row[0])
#                 i += 1
#
#         tfidf_vectorizer = TfidfVectorizer()
#         tfidf_matrix_train = tfidf_vectorizer.fit_transform(sentences)  # finds the tfidf score with normalization
#         # tfidf_matrix_test =tfidf_vectorizer.transform(test_set)
#         stop = timeit.default_timer()
#         print ("training time took was : ")
#         print (stop - start)
#
#         f = open(tfidf_vectorizer_pikle_path, 'wb')
#         pickle.dump(tfidf_vectorizer, f)
#         f.close()
#
#         f = open(tfidf_matrix_train_pikle_path, 'wb')
#         pickle.dump(tfidf_matrix_train, f)
#         f.close()
#         # -----------------------------------------#
#
#     tfidf_matrix_test = tfidf_vectorizer.transform(test_set)
#
#     cosine = cosine_similarity(tfidf_matrix_test, tfidf_matrix_train)
#     #print(cosine)
#
#     cosine = np.delete(cosine, 0)
#     max = cosine.max()
#     response_index = 0
#
#     ############AAA#######
#     if (max<=0.20):
#         #print("hi")
#         a=""
#         #print("- Not in FAQ")
#         return a
#
#     else:
#
#         if (max < 0.49):
#             new_max = max - 0.01
#             list = np.where(cosine >= new_max)  # list contain the similar elements near to max
#             print("Total list------->",list)
#             #print(type(list))
#             # print("list:", str(list))
#             # print("list[0]:", list[0][0])  # list [0][1] <--- 1st block [0] is for row    #list  [0][0]  <--- 2nd block [1] is for element index
#             #for i in list:
#             #print(i[1])
#             # i+=1
#             #print("number of Similar responses with difference of 0.01 from max = " + str(list[0].size))
#             #response_index = random.choice(list[0])
#             # response_index=list[0]
#             #response_index1 = list[0][0]
#             #print("response index-->", response_index1)
#             #response_index2 = list[0][1]
#             #print("response Index2- ", response_index2)
#             # response_index=(list)
#         else:
#             # # print ("not sure")
#             # print ("max is = " + str(max))
#             response_index = np.where(cosine == max)[0][0]  # no offset at all +3
#             #print("response_index-->",response_index)
#
#
#     j = 0
#     k=0
#
#     with open(csv_file_path, "r") as sentences_file:
#         reader = csv.reader(sentences_file, delimiter=',')
#         for row in reader:
#             j += 1  # we begin with 1 not 0 &    j is initialized by 0
#             k += 1
#             try:
#                 if j == response_index :
#                  #a=row[0], row[1], response_index1
#                  a = row[1],row[2],row[3],row[4],row[5]
#                  #print("1st if")
#                  # response_data={"response_text":a}
#                  # json_response=json.dump(response_data)
#                  #print(json_response)
#                  #print("- ",a)
#                  return a
#                 if j==list[0][0]:
#                 #         #print("response_index2",response_index2)
#                 #         #print("2st if")
#                 #         #b = row[0], row[1], response_index2
#                         x = row[1],row[2],row[3],row[4],row[5]
#                 if k == list[0][1]:
#                         b = row[1],row[2],row[3],row[4],row[5]
#                 #         # response_data = {"response_text": b}
#                 #         # json_response = json.dump(response_data)
#                 #         # print(json_response)
#                 #         print("-a ", a)
#                 #         print("-b ",b)
#                         #print("------->",x)
#                         #print("------->",b)
#
#                         return x,b
#
#             except Exception as e:
#                              e
#
#
#
# if __name__ == '__main__':
#
#     while 1:
#         sentence = input("FAQ Engine  : ")
#         faq_obj=Faq_Engine()
#         #faq_obj.faq_engine1(sentence)
#         a=faq_obj.faq_engine1(sentence)
#         print(a)
#
# # _____TF-IDF libraries_____
# #
# #
# #
# # from sklearn.feature_extraction.text import CountVectorizer
# # from sklearn.metrics.pairwise import cosine_similarity
# # from sklearn.feature_extraction.text import TfidfVectorizer
# # import numpy as np
# #
# # # _____helper Libraries_____
# # import pickle
# # import csv
# # import timeit
# # import random
# #
# #
# # import os
# # class Faq_Engine():
# #     def __init__(self):
# #         pass
# #     def faq_engine1(self,test_set_sentence):
# #         csv_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mydata.csv')
# #         #csv_file_path = "FAQ/mydata.csv"
# #         tfidf_vectorizer_pikle_path = "tfidf_vectorizer1.pickle"
# #         tfidf_matrix_train_pikle_path = "tfidf_matrix_train1.pickle"
# #
# #         i = 0
# #         sentences = []
# #
# #         # enter your test sentence
# #         test_set = (test_set_sentence, "")
# #
# #         # 3ashan yzabt el indexes
# #         sentences.append(" No you.")
# #         sentences.append(" No you.")
# #
# #         try:
# #             ##--------------to use------------------#
# #             f = open(tfidf_vectorizer_pikle_path, 'rb')
# #             tfidf_vectorizer = pickle.load(f)
# #             f.close()
# #
# #             f = open(tfidf_matrix_train_pikle_path, 'rb')
# #             tfidf_matrix_train = pickle.load(f)
# #             f.close()
# #             # ----------------------------------------#
# #         except:
# #             # ---------------to train------------------#
# #             start = timeit.default_timer()
# #
# #             # enter jabberwakky sentence
# #             with open(csv_file_path, "r") as sentences_file:
# #                 reader = csv.reader(sentences_file, delimiter=',')
# #                 # reader.next()
# #                 # reader.next()
# #                 for row in reader:
# #                     # if i==stop_at_sentence:
# #                     #    break
# #                     sentences.append(row[0])
# #                     i += 1
# #
# #             tfidf_vectorizer = TfidfVectorizer()
# #             tfidf_matrix_train = tfidf_vectorizer.fit_transform(sentences)  # finds the tfidf score with normalization
# #             # tfidf_matrix_test =tfidf_vectorizer.transform(test_set)
# #             stop = timeit.default_timer()
# #             # print ("training time took was : ")
# #             # print (stop - start)
# #
# #             f = open(tfidf_vectorizer_pikle_path, 'wb')
# #             pickle.dump(tfidf_vectorizer, f)
# #             f.close()
# #
# #             f = open(tfidf_matrix_train_pikle_path, 'wb')
# #             pickle.dump(tfidf_matrix_train, f)
# #             f.close()
# #             # -----------------------------------------#
# #
# #         tfidf_matrix_test = tfidf_vectorizer.transform(test_set)
# #
# #         cosine = cosine_similarity(tfidf_matrix_test, tfidf_matrix_train)
# #         # print(cosine)
# #
# #         cosine = np.delete(cosine, 0)
# #         max = cosine.max()
# #         response_index = 0
# #
# #         ############AAA#######
# #         if (max <= 0.20):
# #          print("- Not in FAQ")
# #
# #         else:
# #
# #            if (max < 0.49):
# #                 new_max = max - 0.01
# #                 list = np.where(cosine >= new_max)  # list contain the similar elements near to max
# #                 # print(type(list))
# #                 # print("list:", str(list))
# #                 # print("list[0]:", list[0][0])  # list [0][1] <--- 1st block [0] is for row    #list  [0][0]  <--- 2nd block [1] is for element index
# #                 # for i in list:
# #                 #     print(i[1])
# #                 # i+=1
# #                 # print("number of Similar responses with difference of 0.01 from max = " + str(list[0].size))
# #                 # response_index = random.choice(list[0])
# #                 # response_index=list[0]
# #                 # response_index1 = list[0][0]
# #                 # print("response index-->", response_index1)
# #                 # response_index2 = list[0][1]
# #                 # print("response Index2- ", response_index2)
# #                 # response_index=(list)
# #            else:
# #               #print ("not sure")
# #               #print ("max is = " + str(max))
# #               response_index = np.where(cosine == max)[0][0]  # no offset at all +3
# #
# #         j = 0
# #         k = 0
# #
# #         with open(csv_file_path, "r") as sentences_file:
# #              reader = csv.reader(sentences_file, delimiter=',')
# #              for row in reader:
# #                  j += 1  # we begin with 1 not 0 &    j is initialized by 0
# #                  k += 1
# #                  try:
# #                      if j == response_index or j == list[0][0]:
# #                        #a=row[0], row[1], response_index1
# #                        a = row[1],row[2]
# #                        # print("1st if")
# #                        print("- ", a)
# #
# #                      if k == list[0][1]:
# #                        # print("response_index2",response_index2)
# #                        # print("2st if")
# #                        # b = row[0], row[1], response_index2
# #                        b = row[1],row[2]
# #                        print("- ", b)
# #                  except Exception as e:
# #                               e
# #
# #
# # #
# # if __name__ == '__main__':
# #
# #     while 1:
# #         sentence = input("FAQ Engine  : ")
# #         faq_obj=Faq_Engine()
# #         #faq_obj.faq_engine1(sentence)
# #         a=faq_obj.faq_engine1(sentence)
# #         print(a)
# #
#
#
#
#
#
#
#
#
# # # _____TF-IDF libraries_____
# # from sklearn.feature_extraction.text import CountVectorizer
# # from sklearn.metrics.pairwise import cosine_similarity
# # from sklearn.feature_extraction.text import TfidfVectorizer
# # import numpy as np
# # import os
# # import json
# # # _____helper Libraries_____
# # import pickle
# # import csv
# # import timeit
# # import random
# # import requests
# # #import os
# # class Faq_Engine():
# #   def __init__(self):
# #    pass
# #   def faq_engine1(self,test_set_sentence):
# #
# #     csv_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'mydata.csv')
# #     tfidf_vectorizer_pikle_path = "tfidf_vectorizer1.pickle"
# #     tfidf_matrix_train_pikle_path ="tfidf_matrix_train1.pickle"
# #
# #     i = 0
# #     sentences = []
# #
# #     # enter your test sentence
# #     test_set = (test_set_sentence, "")
# #
# #     # 3ashan yzabt el indexes
# #     sentences.append(" No you.")
# #     sentences.append(" No you.")
# #
# #     try:
# #         ##--------------to use------------------#
# #         f = open(tfidf_vectorizer_pikle_path, 'rb')
# #         tfidf_vectorizer = pickle.load(f)
# #         f.close()
# #
# #         f = open(tfidf_matrix_train_pikle_path, 'rb')
# #         tfidf_matrix_train = pickle.load(f)
# #         f.close()
# #         # ----------------------------------------#
# #     except:
# #         # ---------------to train------------------#
# #         start = timeit.default_timer()
# #
# #         # enter jabberwakky sentence
# #         with open(csv_file_path, "r") as sentences_file:
# #             reader = csv.reader(sentences_file, delimiter=',')
# #             # reader.next()
# #             # reader.next()
# #             for row in reader:
# #                 # if i==stop_at_sentence:
# #                 #    break
# #                 sentences.append(row[0])
# #                 i += 1
# #
# #         tfidf_vectorizer = TfidfVectorizer()
# #         tfidf_matrix_train = tfidf_vectorizer.fit_transform(sentences)  # finds the tfidf score with normalization
# #         # tfidf_matrix_test =tfidf_vectorizer.transform(test_set)
# #         stop = timeit.default_timer()
# #         print ("training time took was : ")
# #         print (stop - start)
# #
# #         f = open(tfidf_vectorizer_pikle_path, 'wb')
# #         pickle.dump(tfidf_vectorizer, f)
# #         f.close()
# #
# #         f = open(tfidf_matrix_train_pikle_path, 'wb')
# #         pickle.dump(tfidf_matrix_train, f)
# #         f.close()
# #         # -----------------------------------------#
# #
# #     tfidf_matrix_test = tfidf_vectorizer.transform(test_set)
# #
# #     cosine = cosine_similarity(tfidf_matrix_test, tfidf_matrix_train)
# #     #print(cosine)
# #
# #     cosine = np.delete(cosine, 0)
# #     max = cosine.max()
# #     response_index = 0
# #
# #     ############AAA#######
# #     if (max<=0.20):
# #         a=""
# #         #print("- Not in FAQ")
# #         return a
# #
# #     else:
# #
# #         if (max < 0.49):
# #             new_max = max - 0.01
# #             list = np.where(cosine >= new_max)  # list contain the similar elements near to max
# #             #print(type(list))
# #             # print("list:", str(list))
# #             # print("list[0]:", list[0][0])  # list [0][1] <--- 1st block [0] is for row    #list  [0][0]  <--- 2nd block [1] is for element index
# #             # for i in list:
# #             #     print(i[1])
# #             # i+=1
# #             #print("number of Similar responses with difference of 0.01 from max = " + str(list[0].size))
# #             #response_index = random.choice(list[0])
# #             # response_index=list[0]
# #             #response_index1 = list[0][0]
# #             #print("response index-->", response_index1)
# #             #response_index2 = list[0][1]
# #             #print("response Index2- ", response_index2)
# #             # response_index=(list)
# #         else:
# #             # # print ("not sure")
# #             # print ("max is = " + str(max))
# #             response_index = np.where(cosine == max)[0][0]  # no offset at all +3
# #
# #
# #     j = 0
# #     k=0
# #
# #     with open(csv_file_path, "r") as sentences_file:
# #         reader = csv.reader(sentences_file, delimiter=',')
# #         for row in reader:
# #             j += 1  # we begin with 1 not 0 &    j is initialized by 0
# #             k += 1
# #             try:
# #                 if j == response_index or j==list[0][0]:
# #                  #a=row[0], row[1], response_index1
# #                  a = row[1],row[2]
# #                  #print("1st if")
# #                  # response_data={"response_text":a}
# #                  # json_response=json.dump(response_data)
# #                  #print(json_response)
# #                  #print("- ",a)
# #                  return a
# #
# #                 if k==list[0][1]:
# #                         #print("response_index2",response_index2)
# #                         #print("2st if")
# #                         #b = row[0], row[1], response_index2
# #                         b = row[1],row[2]
# #                         # response_data = {"response_text": b}
# #                         # json_response = json.dump(response_data)
# #                         # print(json_response)
# #                         #print("- ",b)
# #                         return b
# #
# #             except Exception as e:
# #                              e
# #
# #
# # #
# # if __name__ == '__main__':
# #
# #     while 1:
# #         sentence = input("FAQ Engine  : ")
# #         faq_obj=Faq_Engine()
# #         #faq_obj.faq_engine1(sentence)
# #         a=faq_obj.faq_engine1(sentence)
# #         print(a)