#from .faq_engine_file import Faq_Engine
import socket
ipaddress= socket.gethostbyname(socket.gethostname())
# print(ipaddress)
class FAQ_Extractor():
    def __init__(self):
        pass
    def faq_extractor_function(self,faq_question,answer,audio,video,image,doc):

        all=faq_question, answer, audio, video, image, doc

        audio_data=""
        video_data=""
        imgae_data=""
        doc_data=""
        if audio:
                audio_data="""<audio controls><source src="http://{1}/media/audio/{0}" type="audio/mpeg"></audio>""".format(audio,ipaddress)
        if video:
                video_data="""<video width="300"  controls><source src="http://{1}/media/video/{0}" type="video/mp4"></video>""".format(video,ipaddress)
        if image:

                imgae_data=""" <a href="http://{1}/media/images/{0}" target="_blank">{0}</a>""".format(image, ipaddress)
        if doc:

                doc_data = """<a href="http://{1}/media/doc/{0}" target="_blank">{0}</a>""".format(doc, ipaddress)
        string =""
        for mdata in (faq_question,answer,video_data,audio_data,imgae_data,doc_data):
                if mdata:
                    tr ="""<tr><td>{0}</td></tr> <tr><td>&nbsp;&nbsp;&nbsp;</td></tr>""".format(mdata)
                    string += tr

        question_table=    """<table border="1" cellspacing="10">{0}</table>""".format(string)
        return question_table
