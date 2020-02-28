import aiml
import os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base_path_xml = os.path.join(base_dir, 'aiml_set' ,'aiml')
print(base_path_xml)
class Alicechat(object):
    
    def __init__(self):
        self.mybot = aiml.Kernel()
        self.mybot.setBotPredicate("name", "Casual")
        for each_path in os.listdir(base_path_xml):
            aiml_path = os.path.join(base_path_xml,each_path)
            if aiml_path.endswith(".aiml"):
                self.mybot.learn(aiml_path)
        

    def normal_chat(self,query):
        
        reply_text = ""
        print("In AIML", query)
        try:
            reply_text = self.mybot.respond(query)
        except Exception as e:
            print ("error", e)
            
        return reply_text


if __name__ == '__main__':
    obj=Alicechat()
    while True:
        query = input("Enter your query:")
        d = obj.normal_chat(query)
        print(d)
    #obj.normal_chat("Vishal")