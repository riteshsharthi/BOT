from dateutil.parser import parse
from datetime import date

def date_extractor(input):
    # import pdb
    # pdb.set_trace()
    #input=input("Enter the Details : ")
    data=parse(input, fuzzy=True)
    print("Month: ",data.month)
    #print("Year: ",date.year)
    d=dict({'month':data.month, 'year':data.year  })
    print(d)


if __name__ == '__main__':
    user_input=input("Enter Date Information: ")
    date_extractor(user_input)




#print("Booking Date & Time is: ",date)


#print(date.dype)


