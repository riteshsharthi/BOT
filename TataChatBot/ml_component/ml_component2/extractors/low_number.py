import re

class LowNumExtract:
    def __init__(self):
        pass

    def low_num_extract(self,input):
        data=[]
        try:
            NumRegex = re.findall(r'\d+',input)
            if NumRegex:
                for num in NumRegex:
                    data.append(int(num))

        except Exception as e:
            print("Exception is in low_num_extract", e)

        return min(data)

if __name__ == '__main__':
    while True:
         user_input=input("Enter Numbers: ")
         obj=LowNumExtract()
         print(obj.low_num_extract(user_input))
