import re

class LowerWordExtract:
    def __init__(self):
        pass

    def lower_word_extract(self,input):
        data={}
        d =[]
        key_list=[]
        output =""

        word_list = ["high","higher","highest","highly",
                     "High", "Higher", "Highest", "Highly",
                     "HIGHER" ,"HIGH" , "HIGHEST","HIGHLY",
                     "mid","middle","midst","medium",
                     "Mid", "Middle", "Midst", "Medium",
                     "MID","MIDDLE","MIDST","MEDIUM","LOW","Low","low"]
        word_dict = {1:"high", 2:"higher", 3:"highest",4:"highly",
                     5:"High", 6:"Higher", 7:"Highest", 8:"Highly",
                     9:"HIGHER", 10:"HIGH", 11:"HIGHEST", 12:"HIGHLY",
                     13:"mid", 14:"middle", 15:"midst", 16:"medium",
                     17:"Mid", 18:"Middle", 19:"Midst", 20:"Medium",
                     21:"MID", 22:"MIDDLE", 23:"MIDST", 24:"MEDIUM",
                     25:"LOW", 26:"Low", 27:"low"}
#some time low some time high
        # print(word_dict)
        txt_list=input.split(" ")

        try:
            if len(txt_list) >= 1:
                for word in txt_list:
                    # print("word",word)
                    if word in word_list:
                        d.append(word)
                # print("d -",d)
                if len(d) >= 1:
                    for k,v in word_dict.items():
                        # print(k, v)
                        for word2 in d:
                            if v == word2:
                                data[k]=v
                    if len(data) >= 1:
                        for k,v in data.items():
                            key_list.append(k)
                        # print(min(key_list))
                        output = data[max(key_list)]

                    word_high = word_list[:12]
                    word_mid = word_list[12:24]
                    word_low = word_list[24:]
                    if output in word_high:
                        output = "High"
                    elif output in word_mid:
                        output = "Middle"
                    elif output in word_low:
                        output = "Low"

        except Exception as e:
            print("Exception is in lower_word_extract py", e)

        return output

if __name__ == '__main__':
    while True:
         user_input=input("Enter Company Name: ")
         obj=LowerWordExtract()
         print(obj.lower_word_extract(user_input))
