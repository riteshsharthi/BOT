import re
class Email_extrator(object):
    def __init__(self):
        pass
    def email_extractor(self,text):
            email =[]
            match = re.search(r'[\w\.-]+@[\w\.-]+', text)
            if match:
                email.append(match.group(0))
                if len(email) >= 1:
                    email = email[0]
            else:
                email
            return email



if __name__ == '__main__':
    email = Email_extrator()
    user_input=input("Enter Email information: ")
    print(email.email_extractor(user_input))



#Ref: https://stackoverflow.com/questions/17681670/extract-email-sub-strings-from-large-document