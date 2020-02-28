import re

class CompanyNameExtractor:
    def __init__(self):
        pass

    def company_code_extract(self,input):
        data=[]
        d =[]
        txt1 = []
        data_dict ={}
        month_list = ["January", "February", 'March', 'April', 'May', 'June', 'July', 'August',
                      'September', 'October', 'November', 'December',"JANUARY", "FEBRUARY", 'MARCH',
                      'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST','SEPTEMBER', 'OCTOBER', 'NOVEMBER',
                      'DECEMBER', 'Jan', 'Feb', 'Mar', 'Apr',
                      'Aug', 'Sep', 'Oct','Nov', 'Dec', 'may', 'june', 'july', 'jan', 'feb', 'mar',
                      'apr', 'aug', 'sep', 'oct','nov', 'dec',"january", "february", 'march',
                      'april', 'may', 'june', 'july', 'august','september', 'october','november',
                      'december']
        try:
            match1 = re.findall(r'[\w\.-]+-[\w\.-]+', input)
            match_sp_char = re.findall(r'[\w\.-]+[$#]+[\w\.-]+', input)
            # print("match_sp_char",match_sp_char)
            number1 = re.findall(r'[\w\.-]+\d[\w\.-]+', input)
            number2 = re.findall(r'[\w\.-]+\d+', input)
            NumRegex = re.findall(r'\d+',input)
            # print("NumRegex :",NumRegex)
            print("number2 : ",number2)
            if match1 or number1 or match_sp_char or NumRegex or number2:
                if len(match1)>=1 or len(number1)>=1 or len(match_sp_char)>=1 or len(NumRegex)>=1 or len(NumRegex)>=1 :
                    data += match1
                    data += number1
                    data += match_sp_char
                    data += number2
                    if len(data)==0 :
                        data+=NumRegex
                        print("data",data)

                if data:
                    for i in data:
                        # print("data",data)
                        try :
                            k = re.findall(r'[a-zA-z]+', i)
                            # print(k)
                            if k:
                                 data_dict[k[0]] = i
                            # print("text2 : ",data_dict, )
                        except Exception as e:
                            print("Exaption in data loop")
            # print(data_dict)
            if data_dict:
                for k, v in data_dict.items():
                    if k not in month_list:
                        d = v.upper()
            elif len(data_dict)==0 and len(data)>=1 :
                    d = data[0]
            elif len(data_dict)==0 and len(data)==0:
                    d =[]

            print("it is compny code extector ",d)
        except Exception as e:
            print("Exception is in company next py", e)

        return d

if __name__ == '__main__':
    while True:
         user_input=input("Enter Company Name: ")
         obj=CompanyNameExtractor()
         print(obj.company_code_extract(user_input))
