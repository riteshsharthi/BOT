#from .faq_engine_file import Faq_Engine
import socket
ipaddress= socket.gethostbyname(socket.gethostname())+"/media/"
print(ipaddress)
class FAQ_Extractor():
    def __init__(self):
        pass
    def faq_extractor_function(self,faq_list1):
        list1 = []

        if len(faq_list1)==1:
            print("In 1 ANS--->")
            # for faq_list in faq_list1:
            #     for k in faq_list.items():
            #         # for i in faq_list.items():
            #             if "question" in k and faq_list['question']:
            #                 type = 'text'
            #                 list1.append({
            #                     "type": type,
            #                     "sequence": faq_list['que_seq'],
            #                     "value": faq_list['question']
            #                 })
            #             if "ans" in k and faq_list['ans']:
            #                 type = 'text'
            #                 list1.append({
            #                     "type": type,
            #                     "sequence": faq_list['ans_seq'],
            #                     "value": faq_list['ans']
            #                 })
            #             if "video" in k and faq_list['video']:
            #                 type = 'video'
            #                 list1.append({
            #                     "type": type,
            #                     "sequence": faq_list['video_seq'],
            #                     "value": "http://"+str(ipaddress)+"video/"+str(faq_list['video'])
            #                 })
            #             if "audio" in k and faq_list['audio']:
            #                 type = 'audio'
            #                 list1.append({
            #                     "type": type,
            #                     "sequence": faq_list['audio_seq'],
            #                     "value": "http://"+str(ipaddress)+"audio/"+str(faq_list['audio'])
            #                 })
            #             if "img" in k and faq_list['img']:
            #                 type = 'img'
            #                 list1.append({
            #                     "type": type,
            #                     "sequence": faq_list['img_seq'],
            #                     "value": "http://"+str(ipaddress)+"img/"+str(faq_list['img'])
            #                 })
            #             if "link" in k and faq_list['link']:
            #                 type = 'link'
            #                 list1.append({
            #                     "type": type,
            #                     "sequence": faq_list['link_seq'],
            #                     "value": str(faq_list['link'])
            #                 })
            return faq_list1
                    # print("list1--->",list1)
                    # last_seq = list1[-1]['sequence']
                    # print("last_seq&&&-->", last_seq)
                    # break
        elif len(faq_list1)>1:
            # import ipdb;
            # ipdb.set_trace()
            print("In 3 ANS---> :: ",len(faq_list1))
            # print("All data for FAQ:====>\n",faq_list1)
            # for faq_data in faq_list1:
                # print("faq_list---->", faq_data)
                # print("typeeeeeeeeeeee ",type(faq_data))
                # if faq_list1[0]:
                #     # print("faq_list1[0]------------>",faq_list1[0])
                #     for k in faq_data.items():
                #             # print("List1---- in for loop:-->", list1)
                #             if "question" in k and faq_data['question']:
                #                 type = 'text'
                #                 list1.append({
                #                     "type": type,
                #                     "sequence": faq_data['que_seq'],
                #                     "value": faq_data['question']
                #                 })
                #             if "ans" in k and faq_data['ans']:
                #                 type = 'text'
                #                 list1.append({
                #                     "type": type,
                #                     "sequence": faq_data['ans_seq'],
                #                     "value": faq_data['ans']
                #                 })
                #             if "video" in k and faq_data['video']:
                #                 type = 'video'
                #                 list1.append({
                #                     "type": type,
                #                     "sequence": faq_data['video_seq'],
                #                     "value": faq_data['video']
                #                 })
                #             if "audio" in k and faq_data['audio']:
                #                 type = 'audio'
                #                 list1.append({
                #                     "type": type,
                #                     "sequence": faq_data['audio_seq'],
                #                     "value": faq_data['audio']
                #                 })
                #             if "img" in k and faq_data['img']:
                #                 type = 'img'
                #                 list1.append({
                #                     "type": type,
                #                     "sequence": faq_data['img_seq'],
                #                     "value": faq_list1['img']
                #                 })
                #             if "link" in k and faq_data['link']:
                #                 type = 'link'
                #                 list1.append({
                #                     "type": type,
                #                     "sequence": faq_data['link_seq'],
                #                     "value": faq_data['link']
                #                 })
                #
                #     last_seq=list1[-1]['sequence']

        return faq_list1

#
# if __name__ == '__main__':
#
#     while 1:
#         sentence = input("FAQ Engine  : ")
#         faq_obj=FAQ_Extractor()
#         #faq_obj.faq_engine1(sentence)
#         a=faq_obj.faq_extractor_function(sentence)
#         print(a)
