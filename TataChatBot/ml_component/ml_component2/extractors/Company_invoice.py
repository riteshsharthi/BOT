import re


# # = "Hello, world."
# string1="KX- 001"
#
# m_obj = re.search(r"(KX-).(o..)", string1)
# if m_obj:
#     print( "We matched '" + m_obj.group(1) +\
#           "' and '" + m_obj.group(2) + "'")
#
#



# Python program to illustrate
# Matching regex objects
import re

def invoice(invoice_number):

        NumRegex = re.compile(r'\d\d\d')
        nu = NumRegex.search(invoice_number)
        return 'Your Invoice Number is: ' + nu.group()



if __name__ == '__main__':
    user_input=input("Enter the Invoice Number:  ")
    print(invoice(user_input))
