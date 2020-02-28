import json
import re


class PreProcessing(object):

    def __init__(self):
        pass

    def text_processer(self, uttarance):
        # uttarance = "Book  - ()my ticket"
        uttarance = uttarance.rstrip()

        # uttarance = uttarance.lower()

        punctuations = '''!()[]{};'",<>?%^&*~'''

        no_punct = ""
        for char in uttarance:
            if char not in punctuations:
                no_punct = no_punct + char

        # display the unpunctuated string
        processed_uttarance = re.sub(' +', ' ', no_punct)

        return processed_uttarance


# if __name__ == '__main__':
#     obj = PreProcessing()
#     obj.text_processer()
