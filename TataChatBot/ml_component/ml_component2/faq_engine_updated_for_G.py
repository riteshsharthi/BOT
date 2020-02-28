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
  def max_cosine_value(self,test_set_sentence):
      # import pdb
      # pdb.set_trace()
      # csv_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'mydata2.csv')
      # print(csv_file_path)
      # csv_file_path1 = os.path.join(os.path.dirname(os.path.dirname(__file__)))
      # csv_file_path = csv_file_path1 + "/nlp_engine/" + 'mydata2.csv'
      import os
      json_file_path1 = os.path.join(os.path.dirname(os.path.dirname(__file__)))

      # print("csv_file_path--->", csv_file_path)

      # json_file_path="mydata2.json"
      # print("json_file_path--->", json_file_path)
      tfidf_vectorizer_pikle_path = json_file_path1 + "/nlp_engine/faq_data/" + "tfidf_vectorizer12.pickle"
      tfidf_matrix_train_pikle_path = json_file_path1 + "/nlp_engine/faq_data/" + "tfidf_matrix_train12.pickle"

      # i = 0
      sentences = []

      # enter your test sentence
      test_set = (test_set_sentence, " ")

      # 3ashan yzabt el indexes
      # sentences.append(" No you.")
      # sentences.append(" No you.")
      # import pdb
      # pdb.set_trace()

      try:

          json_file_path = json_file_path1 + "/nlp_engine/faq_data/" + 'mydata2.json'
          ##--------------to use------------------#
          f = open(tfidf_vectorizer_pikle_path, 'rb')
          tfidf_vectorizer = pickle.load(f)
          f.close()

          f = open(tfidf_matrix_train_pikle_path, 'rb')
          tfidf_matrix_train = pickle.load(f)
          f.close()
          # ----------------------------------------#
      except:
          ##--- Mongo to JSON Trainig----###
          import pymongo
          import subprocess
          import os
          myclient = pymongo.MongoClient("mongodb://localhost:27017/")
          client = pymongo.MongoClient('localhost', 27017)
          # mydb = client["bot"]
          # mycol = mydb["f_a_q"]
          # mydict = { "name": "John", "address": "Highway 37" }
          # x = mycol.find_one()
          # print(x)

          dirname = os.path.dirname(__file__)
          # print("dirname-->",dirname)

          os.chdir("C:\\Program Files\\MongoDB\\Server\\3.4\\bin\\")
          mogoexport = os.path.abspath("mongoexport.exe")
          subprocess.call(
              '''{0} -d hr_bot_new -c f_a_q --pretty --type=json -o "{1}\\faq_data\mydata2.json" --jsonArray'''.format(
                mogoexport, dirname))
          json_file_path = json_file_path1 + "/nlp_engine/faq_data/" + 'mydata2.json'
          # ---------------to train------------------#
          start = timeit.default_timer()

          # enter jabberwakky sentence
          with open(json_file_path, "r", encoding='utf-8') as sentences_file:
              json_array = json.load(sentences_file)

              for item in json_array:
                  # store_details = []
                  store_details = item['question']
                  # store_details['city'] = item['city']
                  sentences.append(store_details)

              # print("sentences--->",sentences)
              # print(type(sentences))

              # reader = csv.reader(sentences_file, delimiter=',')
              # reader.next()
              # reader.next()
              # for row in reader:
              #     # if i==stop_at_sentence:
              #     #    break
              #     sentences.append(row[0])
              #     i += 1

              ###################### tfidf SCORE#####################
              # tfidfvec = TfidfVectorizer(corpus, decode_error='ignore', stop_words=stops, ngram_range=(1, 5),
              #                            tokenizer=Stemmer.stemTokenize)

              # analyzer = 'word',
              # tokenizer = dummy_fun,
              # preprocessor = dummy_fun,
              # token_pattern = None
              #
              tfidf_vectorizer = TfidfVectorizer(stop_words='english',encoding='utf-8',decode_error='ignore',lowercase=True,analyzer='word',norm='l1',use_idf=False, smooth_idf=False, sublinear_tf=True)
              tfidf_matrix_train = tfidf_vectorizer.fit_transform(sentences)  # finds the tfidf score with normalization
              # tfidf_matrix_test =tfidf_vectorizer.transform(test_set)
              stop = timeit.default_timer()
              # print ("training time took was : ")
              # print (stop - start)

              f = open(tfidf_vectorizer_pikle_path, 'wb')
              pickle.dump(tfidf_vectorizer, f)
              f.close()

              f = open(tfidf_matrix_train_pikle_path, 'wb')
              pickle.dump(tfidf_matrix_train, f)
              f.close()
          # -----------------------------------------#
      # print("Sentences--->",sentences)
      # print("test_set",test_set)
      tfidf_matrix_test = tfidf_vectorizer.transform(test_set)

      # print("tfidf_matrix_train-->",tfidf_matrix_train)
      cosine = cosine_similarity(tfidf_matrix_train, tfidf_matrix_test)
      # print(cosine)
      # print(type(cosine))

      ###############################
      ############Sort###############

      max_cosine = cosine.max()
      #print("max_cosine value from new function--->", max_cosine)
      return max_cosine

################################################################
  def faq_engine1(self,test_set_sentence):
    # import pdb
    # pdb.set_trace()
    #csv_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'mydata2.csv')
    #print(csv_file_path)
    # csv_file_path1 = os.path.join(os.path.dirname(os.path.dirname(__file__)))
    # csv_file_path = csv_file_path1 + "/nlp_engine/" + 'mydata2.csv'
    import os
    json_file_path1 = os.path.join(os.path.dirname(os.path.dirname(__file__)))

    #print("csv_file_path--->", csv_file_path)

    #json_file_path="mydata2.json"
    # print("json_file_path--->", json_file_path)
    tfidf_vectorizer_pikle_path = json_file_path1 + "/nlp_engine/faq_data/"+"tfidf_vectorizer12.pickle"
    tfidf_matrix_train_pikle_path =json_file_path1 + "/nlp_engine/faq_data/"+"tfidf_matrix_train12.pickle"

    # i = 0
    sentences = []

    # enter your test sentence
    test_set = (test_set_sentence," ")

    # 3ashan yzabt el indexes
    # sentences.append(" No you.")
    # sentences.append(" No you.")
    # import pdb
    # pdb.set_trace()

    try:

        json_file_path = json_file_path1 + "/nlp_engine/faq_data/" + 'mydata2.json'
        ##--------------to use------------------#
        f = open(tfidf_vectorizer_pikle_path, 'rb')
        tfidf_vectorizer = pickle.load(f)
        f.close()

        f = open(tfidf_matrix_train_pikle_path, 'rb')
        tfidf_matrix_train = pickle.load(f)
        f.close()
        # ----------------------------------------#
    except:
        ##--- Mongo to JSON Trainig----###
        import pymongo
        import subprocess
        import os
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        client = pymongo.MongoClient('localhost', 27017)
        # mydb = client["bot"]
        # mycol = mydb["f_a_q"]
        # mydict = { "name": "John", "address": "Highway 37" }
        # x = mycol.find_one()
        # print(x)

        dirname = os.path.dirname(__file__)
        # print("dirname-->",dirname)

        os.chdir("C:\\Program Files\\MongoDB\\Server\\3.4\\bin\\")
        mogoexport = os.path.abspath("mongoexport.exe")
        subprocess.call(
           '''{0} -d hr_bot_new -c f_a_q --pretty --type=json --fields question,answer,audio,video,image,doc -o "{1}\\faq_data\\mydata2.json" --jsonArray'''.format(
               mogoexport, dirname))
        json_file_path = json_file_path1 + "/nlp_engine/faq_data/" + 'mydata2.json'
        # ---------------to train------------------#
        start = timeit.default_timer()

        # enter jabberwakky sentence
        with open(json_file_path, "r",encoding='utf-8') as sentences_file:
            json_array = json.load(sentences_file)

            for item in json_array:
                # store_details = []
                store_details = item['question']
                # store_details['city'] = item['city']
                sentences.append(store_details)

            # print("sentences--->",sentences)
            # print(type(sentences))


            # reader = csv.reader(sentences_file, delimiter=',')
            # reader.next()
            # reader.next()
            # for row in reader:
            #     # if i==stop_at_sentence:
            #     #    break
            #     sentences.append(row[0])
            #     i += 1

            tfidf_vectorizer = TfidfVectorizer(stop_words='english',encoding='utf-8')
            tfidf_matrix_train = tfidf_vectorizer.fit_transform(sentences)  # finds the tfidf score with normalization
            # tfidf_matrix_test =tfidf_vectorizer.transform(test_set)
            stop = timeit.default_timer()
            # print ("training time took was : ")
            # print (stop - start)

            f = open(tfidf_vectorizer_pikle_path, 'wb')
            pickle.dump(tfidf_vectorizer, f)
            f.close()

            f = open(tfidf_matrix_train_pikle_path, 'wb')
            pickle.dump(tfidf_matrix_train, f)
            f.close()
        # -----------------------------------------#
    # print("Sentences--->",sentences)
    # print("test_set",test_set)
    tfidf_matrix_test = tfidf_vectorizer.transform(test_set)

    # print("tfidf_matrix_train-->",tfidf_matrix_train)
    cosine = cosine_similarity(tfidf_matrix_train,tfidf_matrix_test)
    #print(cosine)
    # print(type(cosine))

    ###############################
    ############Sort###############


    max_cosine = cosine.max()
    #print("max_cosine--->",max_cosine)


    ###########################################
    ##########################################
    with open(json_file_path, "r", encoding='utf-8') as sentences_file1:
        json_array = json.load(sentences_file1)
        # print("JSON_ARRAY:--->", json_array)
        sentences_question = []
        sentences_ans = []
        sentences_audio = []
        sentences_video = []
        sentences_image = []
        sentences_doc = []
        question_seq=[]
        answer_seq=[]
        audio_seq=[]
        video_seq=[]
        image_seq=[]
        doc_seq=[]

        Botresponce = [{
            "type": "",
            "sequence": "",
            "value": ""
        }]



        for item in json_array:
            #print("items in json array:-->",item)
            store_question = item['question']
            question_seq1=item['question_seq']

            store_ans = item['answer']
            answer_seq1=item['answer_seq']

            store_audio = item['audio']
            audio_seq1=item['audio_seq']

            store_video = item['video']
            video_seq1=item['video_seq']

            store_image = item['image']
            image_seq1=item['image_seq']

            store_doc = item['doc']
            doc_seq1=item['doc_seq']

            #print("questions---->",store_question)
            sentences_question.append(store_question)
            question_seq.append(question_seq1)

            sentences_ans.append(store_ans)
            answer_seq.append(answer_seq1)

            sentences_audio.append(store_audio)
            audio_seq.append(audio_seq1)

            sentences_video.append(store_video)
            video_seq.append(video_seq1)

            sentences_image.append(store_image)
            image_seq.append(image_seq1)

            sentences_doc.append(store_doc)
            doc_seq.append(doc_seq1)
    ###########################################
    ###########################################

    # if(max_cosine<=0.60):
    #     #print("hi")
    #     a=""
    #     # b=""
    #     # c = ""
    #     # d = ""
    #     # e = ""
    #     # f = ""
    #     #print("- Not in FAQ")
    #     return a
    # else:
        if(max_cosine <=0.95):
            # print("max cosine inside if",max_cosine)
            # print("HI")
            new_max = max_cosine -0.10
            #Top-->3
            #########################
            #### SORTED #############

            ## current 2d array is --->cosine

            numrows=len(cosine)
            # print("numrows-->",numrows)

            id = [i for i in range(0, len(cosine))]

            New_matrix_cosine = np.insert(cosine, 0, id, axis=1)
            # print("New_matrix_cosine-->\n",New_matrix_cosine)

            # sorted_array = sorted(New_matrix_cosine, key=lambda New_matrix: New_matrix[1], reverse=True)
            sorted_array = sorted(New_matrix_cosine, key=lambda New_matrix_cosine: New_matrix_cosine[1], reverse=True)
            # print("New ---> sorted array--->", sorted_array)

            list_np = [row[0] for row in sorted_array]
            # print("1st Column type-->: ", type(list_np))

            list_np = [int(x) for x in list_np]
            #print("1st Column: ", list_np[:3])
            # sorted_cosine = sorted(cosine, key=lambda student: student[0], reverse=True)
            # list_np = np.sort(np.where(cosine >= new_max))  # list contain the similar elements near to max
            # list_np = sorted(np.where(cosine >= new_max),key=lambda sorted_cosine: sorted_cosine[0], reverse=True)

            # print("Sorted list np---->",list_np)
            # print("Total list------->", list_np) ###Tuple
            # print("Total list------->", list_np[0][0])
            # print("Total list------->", list_np[0][1])
            # print("Total list------->", list_np[0][2])
            # compaire MAX value with Cosine
            # print("Max Cosine--->",len(list_np[0]))

        else:
                response_text = np.where(cosine == max_cosine)[0][0]
                # print("response_text--->", response_text)
                # print("ALL Sentences Questions:---> ",sentences_question)
                response_list=[]
                response_list.append({"question":sentences_question[response_text],"ans":sentences_ans[response_text],"video":sentences_video[response_text],"audio":sentences_audio[response_text],"img":sentences_image[response_text],"doc":sentences_doc[response_text],
                                      "que_seq":question_seq[response_text],"ans_seq":answer_seq[response_text],"audio_seq":audio_seq[response_text],"video_seq":video_seq[response_text],"img_seq":image_seq[response_text],"doc_seq":doc_seq[response_text]})
                return response_list

        top_list = []

        # print("----->len(list_np)",len(list_np[0])) #list 1
        # for a in [(list_np[0])]:
        #     print("x-->",a)
        #     # a.ravel()
        #     print("aaaaa>-",a)
        for i in list_np[:3]:
            # print("i in a",i)

            top_list.append({"question":sentences_question[i],"ans": sentences_ans[i], "video":sentences_video[i],"audio": sentences_audio[i],"img": sentences_image[i],"doc":sentences_doc[i],
                             "que_seq":question_seq[i],"ans_seq": answer_seq[i],"audio_seq": audio_seq[i],"video_seq":video_seq[i],"img_seq": image_seq[i],"doc_seq": doc_seq[i]})
        return top_list



        # if list_np[0][0]:
        #     print("Inside list_np[0][0]",list_np[0][0])
        #     a=list_np[0][0]
        #     print("aaaaaaaaaaaaa->",a)
        #     x=sentences_question[a], sentences_ans[a],sentences_video[a],sentences_audio[a], sentences_image[a],sentences_doc[a]
        #         # return response_list1
        # if list_np[0][1] :
        #     print("Inside list_np[0][1]",list_np[0][1])
        #     a=list_np[0][1]
        #     print("aaaaaaaaaaaaa->",a)
        #     #response_list1 = []
        #     y=sentences_question[a],sentences_ans[a],sentences_video[a],sentences_audio[a],sentences_image[a],sentences_doc[a]
        #     return x, y


if __name__ == '__main__':

    while 1:
        sentence = input("FAQ Engine  : ")
        faq_obj=Faq_Engine()
        max_cosine_value=faq_obj.max_cosine_value(sentence)
        #faq_obj.faq_engine1(sentence)
        #questions,ans,audio,video,image,doc=faq_obj.faq_engine1(sentence)
        all= faq_obj.faq_engine1(sentence)
        # print("type of return value--->",type(a))
        # print(a,b,c,d)
        print(all)

