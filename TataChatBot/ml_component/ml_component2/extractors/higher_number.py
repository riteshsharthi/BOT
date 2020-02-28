import re

class HigherNumExtract:
    def __init__(self):
        pass

    def higher_num_extract(self,input):
        data=[]
        try:
            NumRegex = re.findall(r'\d+',input)
            if NumRegex:
                for num in NumRegex:
                    data.append(int(num))

        except Exception as e:
            print("Exception is in higher_num_extract", e)

        return max(data)

if __name__ == '__main__':
    while True:
         user_input=input("Enter Numbers: ")
         obj=HigherNumExtract()
         print(obj.higher_num_extract(user_input))
