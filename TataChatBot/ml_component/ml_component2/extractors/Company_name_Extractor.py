
import re

def company_name(text):
    for word in text.split():
          if word.startswith("KX-") or word.startswith("kx-") or word.startswith("Kx-")or word.startswith("kX-"):
            #print ("Company name is: ",word)
                NumRegex=re.compile(r'\d\d\d')
                nu=NumRegex.search(word)
                print("Your Company name is: "+nu.group())
          


          #   flag=1
          #   pass
          # else:
          #     print("Not valid")
          #     break
            #whole_string=()
            #whole_string='-'.join(word)
            #print(type(word))
            #print(whole_string)



if __name__ == '__main__':
    #text = "this is one #tag and this KX-001 is ?another tag"
    text=input("Enter the comapny name: (eg: KX-001) - ")
    company_name(text)






#tag
#?another9