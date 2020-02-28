import re
class Sub_company(object):
    def __init__(self):
        pass
    def company_name(self, text):
        a = text.split('-')
        # for word in text.split():
        #       if word.startswith("KXSUB-") or word.startswith("kxsub-") or word.startswith("KxSub-")or word.startswith("kXSUB-"):
        #         #print ("Company name is: ",word)
        #             NumRegex=re.compile(r'\d\d\d')
        #             nu=NumRegex.search(word)

        return a[1]

if __name__ == '__main__':
    #text = "this is one #tag and this KX-001 is ?another tag"
    # text=input("Enter the SubComapny comapny name: (eg: KXSUB-001) - ")
    (Sub_company.company_name())
