import pymongo
import subprocess
import os
myclient=pymongo.MongoClient("mongodb://localhost:27017/")
client = pymongo.MongoClient('localhost', 27017)
mydb=client["bot"]
mycol=mydb["f_a_q"]
#mydict = { "name": "John", "address": "Highway 37" }
#x = mycol.find_one()
#print(x)

dirname=os.path.dirname(__file__)
#print("dirname-->",dirname)

os.chdir("C:\\Program Files\\MongoDB\\Server\\3.4\\bin\\")
mogoexport=os.path.abspath("mongoexport.exe")
subprocess.call('''{0} -d bot -c f_a_q --type=csv --fields question,answer,audio,video,image,doc -o "{1}\\mydata2.csv"'''.format(mogoexport,dirname))