from django.shortcuts import render
from django.http import JsonResponse
import time
import redis
from django.contrib.auth.models import User
from faq_component.views import Faq_Engine
# from ml_component.ml_component2.faq_engine_updated_for_G import Faq_Engine
from ml_component.ml_component2.counter_logic import CounterLogic
from django.views.decorators.csrf import csrf_exempt
currentTime = int(time.strftime('%H'))
counter_logic=CounterLogic()
from .ChatHistoryLogs import logger
# Create your views here.

def greet(username):
    con_dict ={}
    if currentTime < 12:
         val = 'Hi {0}... Good morning, How can I help you.'.format(username)
    elif 15 >= currentTime > 12:
        val = 'Hi {0}... Good afternoon, How can I help you.'.format(username)
    elif currentTime > 15:
        val = 'Hi {0}... Good evening, How can I help you.'.format(username)
    else:
        val = 'Hi {0}... How may I help You'.format(username)

    con_dict["message"] = val
    return val

@csrf_exempt
def test(request):
    con_dict = {}
    engin = Faq_Engine()
    val=engin.faq_engine1("How to revive IPD bill")
    con_dict["Val"] = val
    return JsonResponse(con_dict)


def bot_start(request):
    # on launch bot first call
    con_dict = {}
    counter_dict = {}
    try:
        redis.StrictRedis(host='localhost', port=6379, db=1).flushdb()
        con_dict['username'] = str(request.user).capitalize()
        counter_dict['username'] = request.user
        counter_dict['user_id'] = User.objects.get(username=request.user).id
        counter_dict['session_key'] = str(request.session.session_key)
        context_data = counter_logic.main("", counter_dict, True)

        # con_dict['bot_responce'] = context_data["chat_res"]["reply_text"]
        con_dict['bot_responce'] = [greet(str(request.user).capitalize())]
        button = context_data["chat_res"]["additional_param"].get("button", [])
        if button:
            con_dict['recommend'] = button
        bot_launch_flag = True
        con_dict['username'] = str(request.user).capitalize()
    except Exception as e:
        print(" Exception in BOT Start :", e)
        logger.error(" Exception in BOT Start : {} ".format(e))
    try:
        history_dic = {
            "request_data": "chatbot Start",
            "responce_data": greet(str(request.user).capitalize()),
            "task_name": "Greating",
            "task_type": "Greating",
            "request_user": "ChatBot",
            "responce_user": "Chatbot"
        }
        logger.info("Chat history Info  from start bot: {}".format(history_dic))
    except Exception as e:
        logger.error("Exception in chat history save from start bot : {}".format(e))

    return render(request, 'polls/index.html', con_dict)


def chatbot(request):
    counter_dict = {}
    con_dict = {}
    context_data = {}
    replay_text = []
    user_details = {}
    # con_dict['a'] = greet(str(request.user).capitalize())
    # print(con_dict['a'])sliteeeeeeeeeeee
    con_dict['username'] = str(request.user).capitalize()
    counter_dict['username'] = request.user
    counter_dict['user_id'] = User.objects.get(username=request.user).id
    counter_dict['password'] = User.objects.get(username=request.user).id
    counter_dict['session_key'] = str(request.session.session_key)


    if request.method == "POST" and request.is_ajax():
        # import pdb
        # pdb.set_trace()

        utter = str(request.POST.get('answers'))
        agentreply = str(request.POST.get('agentreply'))

        user_id = int(request.user.id)
        session_id = str(request.session.session_key)
        user_name = str(request.user)
        button = []
        logger.info("Chat Bot Start Restart or Start By User : {}".format(str(request.user).capitalize()))
        try:
            if utter and user_id:
                context_data = counter_logic.main(utter, counter_dict)
                print("=-=-=-=-=-if utter and user_id:=-=-=-=-=-=")
        except Exception as e:
            print("obj_counter_logic.main", e)

        try:
            con_dict['user_uttarance'] = context_data['chat_req']['uttarance']
            button = context_data["chat_res"]["additional_param"].get("button", [])
            con_dict['bot_responce'] = context_data["chat_res"]["reply_text"]
            if button:
                con_dict['recommend'] = button

            print("***********************************************", con_dict['bot_responce'])
            replay_text += context_data["chat_res"]["reply_text"]
        except Exception as e:
            print("bot_responce in viewbot", e)
            logger.error(" Exception in viewbot : {}".format(e))

        try:
            history_dic = {
                "request_data":str(utter),
                "responce_data": [i["value"] for i in context_data["chat_res"]["reply_text"]],
                "task_name": context_data["chat_req"]["chat_attributes"]["task"],
                "task_type": context_data["chat_req"]["chat_attributes"]["task"],
                "request_user": str(request.user).capitalize(),
                "responce_user": "Chatbot"
            }
            logger.info("Chat history Info from chatbot : {}".format(history_dic))
        except Exception as e:
            print("Exception in chat history save from chatbot", e)
            logger.error("Exception in chat history save from chatbot: {}".format(e))

    return JsonResponse(con_dict)

