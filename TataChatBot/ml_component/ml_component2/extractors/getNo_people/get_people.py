from .word2number import w2n
import re


class GetPeople():
    def __init__(self):
        pass

    def no_people(self, text):
        # print (text , "=================================")
        person =""
        try:
            num = w2n.word_to_num(text)
            if not num:
                num = re.findall('\d+', text)
                if num:
                    num = num[0]

        except Exception as e:
            print("Exception in no_people", e)
        if num:
            person = num
        return person


if __name__ == '__main__':
    obj = GetPeople()
    print(obj.no_people("book ticket pelple "))