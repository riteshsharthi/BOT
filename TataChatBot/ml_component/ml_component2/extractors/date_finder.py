

from dateutil.parser import parse

def date_extractor(qry):
    date=parse(qry, fuzzy=True)
    d=dict({'month':date.month, 'year':date.year  })
    print(d)

if __name__ == '__main__':
    user_input=input("Enter Date Information: ")
    date_extractor(user_input)




#print("Booking Date & Time is: ",date)


#print(date.dype)








#ref: https://stackoverflow.com/questions/19994396/best-way-to-identify-and-extract-dates-from-text-python
