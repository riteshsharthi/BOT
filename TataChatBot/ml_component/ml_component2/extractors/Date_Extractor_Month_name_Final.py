from dateutil.parser import parse
import re
import datetime
class DateMonthYear:
    def __init__(self):
           pass
           #self.input = input

    def date_extractor(self,input):
        wordList = re.sub("[^\w]", " ", input).split()
        # match_month = re.findall(r'[\w\.-]', input)
        match_space = re.findall(r'[a-zA-Z]+\s+\d{4}', input)
        match_sp_char = re.findall(r'[\w\.-]+[/:|]+[\w\.-]+', input)

        # match_with_special = re.findall(r'\d{2}-+\d{4}', input)

        match = re.findall(r'[\w\.-]+-[\w\.-]+', input)
        # print(match)
        number = re.findall(r'[\w\.-]+\d[\w\.-]+', input)
        month_list = ["January", "February", 'March', 'April', 'May', 'June', 'July', 'August',
                      'September', 'October', 'November', 'December', "january", "february",
                      'march', 'april', 'may', 'june', 'july', 'august','september', 'october',
                      'november', 'december','Jan', 'Feb', 'Mar', 'Apr', 'Aug', 'Sep', 'Oct',
                      'Nov', 'Dec', 'may', 'june', 'july', 'jan', 'feb', 'mar', 'apr', 'aug',
                      'sep', 'oct','nov', 'dec']
        d ={}

        data =[]
        data_dict ={}
        if input:
            txt =[]
            if len(match_space) >= 1:
                if match_space:
                    a = match_space[0].split(" ")
                    data_dict[a[0]] ="{0}{1}".format(a[0],a[1])
                    # print("a",data_dict)

            # elif len(match_with_special)>1:
            #     if match_with_special:
            #         a =match_with_special
            #         print("match_with_special : ", match_with_special)
            elif len(match)>=1 or len(number)>=1 or len(wordList)>=1 or len(match_sp_char)>=1  :
                    data += match
                    data += number
                    data += wordList
                    data += match_sp_char
                    data = set(data)
                    data = list(data)
                    if data:
                        for i in data:
                            txt.append(re.findall(r'[a-zA-z]+', i))
                            try :
                                k = re.findall(r'[a-zA-z]+', i)
                                data_dict[k[0]] = i
                                # print("text2 : ",data_dict, )
                            except Exception as e:
                                print("Exaption in data loop")




        if data_dict:
            for k,v in data_dict.items():
                if k in month_list:
                    # print(data[count - 1])
                    print("month list is working")

                    date = parse(v, fuzzy=True)
                    #d = dict({'month': date.month, 'year': date.year})
                    month=date.month
                    # print("month : ",date)
                    switcher={
                              1:'January',
                              2:'February',
                              3:'March',
                              4:'April',
                              5:'May',
                              6:'June',
                              7:'July',
                              8:'August',
                              9:'September',
                              10:'October',
                              11:'November',
                              12:'December',
                    }
                    month_name=switcher.get(month)

                    d.update( dict({'month': month_name, 'year': date.year}))

        return d




if __name__ == '__main__':
    obj = DateMonthYear()
    while True:
        user_input=input("Enter Date Information: ")
        print(obj.date_extractor(user_input))



