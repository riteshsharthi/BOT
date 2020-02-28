import re

class CityFinder(object):
    
        def __init__(self):
                pass

        def findcity(self, text):
                dict_people = {}
                lookup_dict = {"Pune": "Pune","poona": "Pune","Poona": "Pune", "pune":"Pune","Mumbai": "Mumbai","mumbai":"Mumbai","mumbai1":"Mumbai","mum":"Mumbai","bombay":"Mumbai","Bombay":"Mumbai"}
        
                # Make a regex for only letters.
                regex = re.compile('[^a-zA-Z]')
                city_list =[]
                textSplit = text.split()
                #print(len(textSplit))
                for i in range(0, len(textSplit)):
                    # Get rid of punctuation.
                    word = regex.sub('', textSplit[i]).lower()
                    if word in lookup_dict:
                        # Fetch the right letter from the lookup_dict.
                        letter = lookup_dict[word]
                        city_list.append(letter)
                if city_list:
                        dict_people["city"] = city_list
                return dict_people
#hi abhi
if __name__ == "__main__":
    val = CityFinder()
    # d = val.findcity()
    # print (d)