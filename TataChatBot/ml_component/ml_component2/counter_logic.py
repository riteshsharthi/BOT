import os
import pymongo
import redis
import json
import random
import re
from time import sleep
from copy import deepcopy
import traceback
import requests
from datetime import datetime
from .tensorflow_classifie.trainer import TFTrainer
from .extractors.text_processor import PreProcessing
from .aiml_set.aimlpro import Alicechat

from .initial_classifirer.log_reg_clf_multilab import LogisticClassifier
from .cancel_classifirer.log_reg_clf_multilab import LogisticClassifierCancelTask
from .repeat_classifier.log_reg_clf_multilab import LogisticClassifierRepeatTask
from .base_class import Operations
# from .faq_engine_file import Faq_Engine
from faq_component.views import Faq_Engine
# from ml_component.ml_component2.faq_engine_updated_for_G import Faq_Engine
from dashboard.models import ChatHistory

from .faq_funcation import FAQ_Extractor
# from FAQ.models import *
import pdb

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base_path_json = os.path.join(base_dir, 'ml_component2/')
from .date_wise_log import logger

base_path = os.path.join(base_dir, 'ml_component2/tensorflow_classifie')
file_path =str(os.path.join(base_path, 'tf_data'))

TTL = 60 * 60


class CounterLogic(object):
    def __init__(self):
        self.obj_initial_classifirer = LogisticClassifier()
        self.obj_cancel_task_classifirer = LogisticClassifierCancelTask()
        self.obj_repeat_classifier = LogisticClassifierRepeatTask()
        self.aiml_obj = Alicechat()
        self.faq_obj = Faq_Engine()
        # self.faq_obj = Faq_Engine()
        self.faq_extractor = FAQ_Extractor()
        self.mongo_conn = pymongo.MongoClient()
        self.db = self.mongo_conn["TATA_ChatBot"]
        self.redis_obj = redis.StrictRedis(host='localhost', port=6379, db=1)
        self.operations_obj = Operations()

        with open(os.path.join(base_path_json, "user_context.json"), "r") as fp:
            self.context_json = json.load(fp)

        self.preprocessor = PreProcessing()
        self.trainer = TFTrainer()

    def config_changer(self):
        try:

            with open(os.path.join(base_path_json, "config_file.json"), "r") as fp:
                config_json = json.load(fp)
                for k, v in config_json.items():
                    if v == "yes":
                        config_json[k] = True
                    if v == "no":
                        config_json[k] = False
        except Exception as e:
            print("Exception in config_changer", e)
            logger.error("Exception in config_changer : {}".format(e))
        return (config_json)

    def chat_history(self, data_dict):
        # data_dict={
        #     "request_data":"",
        #     "responce_data":"",
        #     "task_name":"",
        #     "task_type":"",
        #     "request_user":"",
        #     "responce_user":""
        # }
        try:
            if len(ChatHistory.objects.all()) == 0:
                idss = 1
            else:
                idss = max(i.id for i in ChatHistory.objects.all()) + 1

            a = ChatHistory.objects.create(id=idss, request_data=data_dict["request_data"].strip(), responce_data=data_dict["responce_data"],
                                           task_name=data_dict["task_name"].strip(),task_type=data_dict["task_type"].strip(),
                                           request_user=data_dict["request_user"].strip(), responce_user=data_dict["responce_user"].strip())
            a.save()
        except Exception as e:
            print("Exception in chat_history", e)
            logger.error("Exception in chat_history : {}".format(e))

    def flatten_complex_dict(self, dd):
        result_dict = {}
        for k, v in dd.items():
            if isinstance(v, dict):
                result_dict[k] = v
            elif isinstance(v, list):
                for i in v:
                    for kk, vv in i.items():
                        result_dict[kk] = vv
            else:
                result_dict[k] = v
        return result_dict

    def responce_data1(self, f_dict):
        for k, v in f_dict.items():
            if k == "message":
                resp = "{0} ".format(v)
            else:
                resp = "Sorry data not found for this id. Please try again"
        return resp

    def call_rest_api(self, data, url):
       
        logger.info("____Action url_______{} {}".format(data,  url ))
        # f_resp = ""
        f_resp = []
        context_data["chat_req"]["chat_attributes"]["action_url"]=url
        del data['action_url']
        try:
            responce_data = requests.post(url=url, json=data, timeout=10)
            if responce_data.status_code == 200:
                # get_data = responce_data.json()
                f_resp = responce_data.json()
                if not f_resp:
                    f_resp = ["Sorry data not found for this id. Please try again"]
                    
                print(f_resp, "_____FINAL_RSULT_____N")

                    
        except Exception as e:
            print("Exception in call_rest_api", e)
            logger.error("Exception in call_rest_api : {}".format(e))

        return f_resp

    def flatten_dict(self, dd, prefix=''):
        return {k if prefix else k: v
                for kk, vv in dd.items()
                for k, v in self.flatten_dict(vv, kk).items()
                } if isinstance(dd, dict) else {prefix: dd}

    def call_pre_action_url(self, url, pre_text, context_data):
     
        data = deepcopy(context_data["chat_req"]["chat_attributes"]["entities_extracted"])
        data.update({"username": context_data["identifier"]["user_name"]})

        resp = []
        try:
            if pre_text:
                resp.append(pre_text)
            print( "__________PRE ACTION URL_________________")
            responce_data = requests.post(url=url, json=data, timeout=10)
            logger.info("__________PRE ACTION URL_________ {}".format(url,data ))
            # resp.append(responce_data.json())
            if responce_data.status_code == 200:

                resp.extend(responce_data.json())

        except Exception as e:
            print("Exception in call_rest_api", e)

        return resp

    def post_action_func(self, task_data, context_data, reply_text_list, processed_uttarance, button):
        reply_text_list, context_data, button = self.task_completed([], context_data,
                                                            reply_text_list,
                                                            "clear_previous_data", button)
        post_action_task = task_data[0].get("post_action", "")

        if post_action_task:
            context_data["chat_req"]["chat_attributes"]["task"] = post_action_task
            temp_response_text, context_data, temp_button = self.get_intent_questions(post_action_task, context_data,
                                                                         processed_uttarance)
            reply_text_list.extend(temp_response_text)
            button.extend(temp_button)

        return reply_text_list, context_data, button

    def get_interview_questions(self, each_question, context_data):
        interview_found = False
        interview_url = each_question.get("interview_url", "")
        if interview_url:
            topic = interview_url.strip().split("@")[-1].replace('/','')
            interview_topic = {"interview_topic":topic}
            url = interview_url.strip().split("@")[-2]
            try:

                interview_data = requests.post(url, json = interview_topic)
                if interview_data.status_code == 200:
                    interview_details = interview_data.json()
                    context_data["chat_req"]["interview_details"] = interview_details
                    interview_found = True
            except Exception as e:
                print("Exception in call_rest_api", e)
        return context_data, interview_found

    def recommended(self, each_question, key_to_call):

       

        button = []
        recommende_data = ""
        
        if key_to_call == "entity_id":
            primary_id = each_question["_id"]
            recommende_data = self.db["dashboard_recommunded_data"].find({"entity_id": str(primary_id)})
        elif key_to_call == "task_id" and each_question.count():
            primary_id = each_question[0]["_id"]
            recommende_data= self.db["dashboard_recommunded_data"].find({"task_id": str(primary_id)})

        if recommende_data and recommende_data.count():
            for each in recommende_data:
                button.append(each) 
    
        return button

    def get_intent_questions(self, task_name, context_data, processed_uttarance):

        button = []
        reply_text_list = []
        task_data = self.db["dashboard_intenttotask"].find({"Intent_Name": task_name})
        try:
            normal_flow = True
            repeat_question = False

            if context_data["chat_req"]["interview_details"]:
                normal_flow = False
                user_answer = context_data["chat_req"]["uttarance"]

                classified_label = self.obj_repeat_classifier.test(processed_uttarance)
                label = "".join(list(classified_label["prediction"].keys()))
                print(classified_label, label)

                if label == "proceeding_task.text":
                    asked_seq = context_data["chat_req"]["chat_attributes"]["current_asked_question"]
                    context_data["chat_req"]["chat_attributes"]["asked_sequence_question"][asked_seq][
                        "answer"] = user_answer
                    in_entities = deepcopy(
                        context_data["chat_req"]["chat_attributes"]["asked_sequence_question"][asked_seq])

                    del in_entities["count"]
                    del context_data["chat_req"]["interview_details"][int(asked_seq.replace("_interview", ""))]

                    if "interview_details" not in context_data["chat_req"]["chat_attributes"]["entities_extracted"]:
                        context_data["chat_req"]["chat_attributes"]["entities_extracted"]["interview_details"] = []

                    context_data["chat_req"]["chat_attributes"]["entities_extracted"]["interview_details"].append(
                        in_entities)
                    if not context_data["chat_req"]["interview_details"]:
                        normal_flow = True
                else:
                    repeat_question = True

            if normal_flow and task_data.count() > 0:
                task_id = task_data[0]["_id"]
                all_questions = self.db["dashboard_tasktoentity"].find({"Task_Id": task_id}).sort([("Entity_Sequence", 1)])
                temp_all_questions = deepcopy(all_questions)
                multi_answering = self.config_changer()["multi_answering"]
                # multi_answering = True

                if multi_answering and context_data["chat_req"]["=-0chat_attributes"]["task"] not in [
                    self.config_changer()["failure_tasks"], self.config_changer()["start_task"], "cancel_task"]:

                    multi_extractor = {}
                    for each_q in temp_all_questions:
                        entity_id = each_q["Entity_Id"]
                        entity_name = each_q["Entity_Name"]
                        qseq = str(each_q["Entity_Sequence"])
                        try:
                            extracted_value, context_data, free_text_case, func_name = self.val_extractor(each_q, entity_id,
                                                                                                          processed_uttarance,
                                                                                                          context_data)

                            if free_text_case == "free_text":
                                continue

                            if extracted_value:
                                if func_name and func_name not in multi_extractor:
                                    multi_extractor[func_name] = []

                                multi_extractor[func_name].append((extracted_value, entity_name, qseq, each_q))

                        except Exception as e1:
                            print("get_intent_questions e1", e1)

                    for func_name, values in multi_extractor.items():
                        if len(values) < 2:
                            context_data["chat_req"]["chat_attributes"]["entities_extracted"][values[0][1]] = \
                                values[0][0]
                            context_data["chat_req"]["chat_attributes"]["asked_sequence_question"][values[0][2]] = \
                                values[0][2]
                            context_data["chat_req"]["chat_attributes"]["asked_sequence_question"][values[0][2]] = {
                                "count": 1}
              
                for ind, each_question in enumerate(all_questions):
                   

                    print("------------------")

                    seq = str(each_question["Entity_Sequence"])
                    not_asked_question_flag = seq not in context_data["chat_req"]["chat_attributes"][
                        "asked_sequence_question"]
                    extracted_value_flag = each_question["Entity_Name"] not in \
                                           context_data["chat_req"]["chat_attributes"]["entities_extracted"]
                    
                    if not_asked_question_flag or extracted_value_flag:
                        context_data["chat_req"]["chat_attributes"]["current_asked_question"] = seq

                        if not_asked_question_flag:
                        

                            context_data, interview_found = self.get_interview_questions(each_question, context_data)

                            if interview_found:
                                context_data["chat_req"]["chat_attributes"]["entities_extracted"][
                                    each_question["Entity_Name"]] = {}

                            context_data["chat_req"]["chat_attributes"]["asked_sequence_question"][seq] = each_question
                            reply_text = [each_question["Entity_Question"]]

                            button = self.recommended(each_question, "entity_id")
                            if each_question["pre_action_url"]:
                                action_url_text_list = self.call_pre_action_url(each_question["pre_action_url"],
                                                                                each_question["pre_text"], context_data)
                                reply_text = action_url_text_list + reply_text

                            reply_text_list.extend(reply_text)

                            context_data["chat_req"]["chat_attributes"]["asked_sequence_question"][seq]["count"] = 1
                        else:
                            if context_data["chat_req"]["chat_attributes"]["asked_sequence_question"][seq]["count"] > 2:
                                failuretask = self.config_changer()["failure_tasks"]
                                # deletion of the previous extracted data
                                reply_text_list, context_data, button = self.task_completed(task_data, context_data,
                                                                                    reply_text_list, "failure", button)
                                context_data["chat_req"]["chat_attributes"]["task"] = failuretask
                                temp_response_text, context_data, button = self.get_intent_questions(failuretask, context_data,
                                                                                             processed_uttarance)
                                reply_text_list.extend(temp_response_text)
                                break
                            else:

                                if not [q for q in each_question["Entity_alternet_qustion"] if q.strip()]:
                                    reply_text = [each_question["Entity_Question"]]
                                    # reply_text_list.append(reply_text)
                                else:
                                    reply_text = [random.choice(each_question["Entity_alternet_qustion"])]
                                    # reply_text_list.append(reply_text)
                                if each_question["pre_action_url"]:
                                    action_url_text_list = self.call_pre_action_url(each_question["pre_action_url"],
                                                                                    each_question["pre_text"],
                                                                                    context_data)
                                    reply_text = action_url_text_list + reply_text

                                context_data["chat_req"]["chat_attributes"]["asked_sequence_question"][seq][
                                    "count"] += 1
                                reply_text_list.extend(reply_text)
                        ######################################POST ACTION Start

                        if not context_data["chat_req"]["interview_details"] and not each_question["Entity_Name"] or (
                                all_questions.count() == ind + 1 and task_name in ["cancel_task"]):
                            reply_text_list, context_data, button = self.task_completed(task_data, context_data,
                                                                                reply_text_list, "blank_entity", button)
                            if task_data[0].get("post_action", ""):
                                reply_text_list, context_data, button = self.post_action_func(task_data, context_data,
                                                                                      reply_text_list,
                                                                                      processed_uttarance, button)
                        ######################################POST ACTION End
                        break
                else:
                    if context_data["chat_req"]["chat_attributes"]["task"] == "failuretask":
                        reply_text_list, context_data, button = self.task_completed(task_data, context_data, reply_text_list,
                                                                            "failure", button)

                    else:
                        reply_text_list, context_data, button = self.task_completed(task_data, context_data, reply_text_list,
                                                                            "completed", button)
                        if task_data[0].get("post_action", ""):
                            reply_text_list, context_data, button = self.post_action_func(task_data, context_data, [],
                                                                                  processed_uttarance, button)


            elif normal_flow:
                context_data["chat_req"]["chat_attributes"] = deepcopy(self.context_json["chat_req"]["chat_attributes"])

            for iind, each_interview in enumerate(context_data["chat_req"]["interview_details"]):
                seq = str(iind) + "_interview"

                if repeat_question and seq in context_data["chat_req"]["chat_attributes"]["current_asked_question"]:
                    count = context_data["chat_req"]["chat_attributes"]["asked_sequence_question"][seq]["count"]

                    if len(each_interview["question"]) < count:
                        count = len(each_interview["question"]) - 1

                    reply_text_list.append(each_interview["question"][count:count+1])
                    context_data["chat_req"]["chat_attributes"]["asked_sequence_question"][seq]["count"] +=1
                    
                elif task_data and not task_data[0].get("post_action", ""):
                    each_interview = deepcopy(each_interview)
                    reply_text_list.append(each_interview["question"][0])
                    
                    context_data["chat_req"]["chat_attributes"]["current_asked_question"] = seq
                    context_data["chat_req"]["chat_attributes"]["asked_sequence_question"][seq] = each_interview
                    context_data["chat_req"]["chat_attributes"]["asked_sequence_question"][seq]["count"] = 1

                    break
                else:
                    break

        except Exception as e:
            logger.error('get_intent_questions has Exception  error message :{}'.format(e))
            print("Exception in get_intent_questions ", e, traceback.format_exc())
        return reply_text_list, context_data, button


    def task_completed(self, task_data, context_data, reply_text_list, type_of_action, button):


        print("in task completed===============")
        data_to_hit = {}
        print(bot_req['user_id'], "%%%%%%%%%%%")

        deep_task = deepcopy(context_data["chat_req"]["chat_attributes"]["task"])

        all_extracted_entities = deepcopy(context_data["chat_req"]["chat_attributes"]["entities_extracted"])
        data_to_hit = all_extracted_entities
        context_data["chat_req"]["chat_attributes"]["live_user"] = str(True)
        context_data["chat_req"]["chat_attributes"]["asked_sequence_question"] = {}
        context_data["chat_req"]["chat_attributes"]["current_asked_question"] = ""
        context_data["chat_req"]["chat_attributes"]["task"] = ""
        context_data["chat_req"]["uttarance"] = ""
        context_data["chat_req"]["chat_attributes"]["entities_extracted"] = {}
        context_data["chat_req"]["chat_attributes"] = deepcopy(self.context_json["chat_req"]["chat_attributes"])
        print("no question for asking")
       


        if type_of_action == "completed" and task_data[0]["Action_Url"]:
            
            logger.info( "--------completed-------- {}".format("completed"))
            
          
            # api call with data
            action_url = task_data[0]["Action_Url"]
            data_to_hit["action_url"] = action_url
            context_data["chat_req"]["chat_attributes"]["action_url"]=action_url
            print("data for complite task url",action_url )
            print(json.dumps(data_to_hit, indent=3))

            try:
                recodOFtask = self.db["dashboard_intenttotask"].find({"Intent_Name": str(deep_task)})
                # print(recodOFtask)
                trigg = []
                for i in recodOFtask:
                    trigg.append(i)

                triggerName = trigg[0]["Task_Name"]
                data_to_hit["triggerName"] = str(triggerName)
                data_to_hit["username"] = context_data["identifier"]["user_name"]
            except Exception as e:
                logger.error('completed triggerName has Exception  error message{} :'.format(e))
                print("trigg @@@@", e)

            # reply_text = requests.post(url=url_data, json=data_k)
       
            
            reply_text = self.call_rest_api(self.flatten_dict(data_to_hit), action_url)
            button = self.recommended(task_data, "task_id")

            clean_hit_data = data_to_hit
            del clean_hit_data['action_url']
            # context_data["chat_req"]["time_zone"] = clean_hit_data
            self.viewbot_save(bot_req, deep_task, clean_hit_data)
            print('reply text from rest api ---->', reply_text)
            # reply_text_list.append(reply_text)
            reply_text_list.extend(reply_text)
            previous_task_confirmation = self.config_changer()["switch_task_confirmation"]
            # previous_task_confirmation = True

            if context_data["previous_contexts"] and previous_task_confirmation:
                context_data["chat_req"]["chat_attributes"]["current_asked_question"] = "previous_task_confirmation"
                reply_text_list.append("Do you want to proceed with previous query?")

        return reply_text_list, context_data, button

    def val_extractor(self, task2entity_detail, entity_id, processed_uttarance, context_data):
        import pdb
        extracted_value = ""
        regex_pattern = ""
        tobe_extracted = []
        free_text_case = ""
        match_data = False
        json_data = []
        if entity_id:
            tobe_extracted = self.db["dashboard_entity"].find({"_id": entity_id})
            # print(tobe_extracted[0],
            #       "tobe_extractedtobe_extractedtobe_extractedtobe_extractedtobe_extractedtobe_extractedtobe_extractedtobe_extracted")
        if tobe_extracted:
            free_text_case = tobe_extracted[0]["Entity_Type"]
            regex_pattern = tobe_extracted[0]["Entity_Regex"]

            if regex_pattern.startswith("func-"):
                func_name = regex_pattern.split("-")[1]
                print(func_name, "-----")
                logger.info("---------EXTRACTOR NAME-------- {} {}".format(func_name,processed_uttarance))
                func_index = dir(self.operations_obj).index(func_name)
                if func_index:
                    if free_text_case == "free_text":
                        processed_uttarance = context_data["chat_req"]["uttarance"]

                    extracted_value, context_data = getattr(self.operations_obj, dir(self.operations_obj)[func_index])(
                        processed_uttarance, context_data)
            elif regex_pattern.startswith("trained-") or regex_pattern.startswith("dynamic-"): 
                
                
                if regex_pattern.startswith("trained-"): 
                    match_data = True
                    with open(os.path.join(base_path_json, "train_folder", task2entity_detail["value_collection_name"]), "r") as fp:
                        json_data = json.load(fp)

                elif regex_pattern.startswith("dynamic-"):
                        match_data = True
                        url = task2entity_detail["collection_url"]
                        try:
                            response_data = requests.post(url=url, json={}, timeout=10)
                            if response_data.status_code == 200:
                                json_data = response_data.json()
                                print(json_data, "_______________FINAL_RSULT_____N")
                                
                        except Exception as e:
                            logger.error('val_extractor  __FINAL_RSULT_____N function regex_pattern.startswith("dynamic-")  has Exception  error message {} :'.format(e))
                            print("Exception in call_rest_api", e)

                
            elif regex_pattern.startswith("dynamic-"):
                pass
            elif regex_pattern.strip():
                print("In Else block")
                extracted_value = re.search(processed_uttarance, processed_uttarance, flags=re.IGNORECASE)
                if extracted_value:
                    extracted_value = extracted_value.group()

            if task2entity_detail.get("validation_url", ""):
                url = task2entity_detail["validation_url"]
                match_data = True
                try:
                    response_data = requests.post(url=url, json={}, timeout=10)
                    if response_data.status_code == 200:
                        json_data = response_data.json()
                        print(json_data, "__FINAL_RSULT_____N")
                        
                except Exception as e:
                    logger.error('val_extractor  __FINAL_RSULT_____N function  has Exception  error message {} :'.format(e))
                    print("Exception in call_rest_api", e)

            if match_data and json_data:
             
                uttarance = context_data["chat_req"]["uttarance"]
                for each_pattern in json_data:
                    extracted_value = re.search(str(each_pattern), uttarance, flags=re.IGNORECASE)
                    if extracted_value:
                        extracted_value = extracted_value.group()
                        break

      

        return extracted_value, context_data, free_text_case, regex_pattern

    def ambiguity_resolver_func(self, response_text_list, context_data, intent):
        # diff = intent[0][1]-intent[1][1]
        _temp_list = []
        for ind, eintent in enumerate([intent[0][0].strip(), intent[1][0]].strip()):
            for qdata in self.db["recommend_variation"].find({"tag": eintent}):
                _temp_list.append(str(ind + 1) + ": " + random.choice(qdata["patterns"]))
                context_data["chat_req"]["ambiguity_resolver"][str(ind + 1)] = eintent

        if _temp_list:
            _call_else_block = False
            response_text_list.append(
                " Please select 1 or 2\n\n<br>" + "\n<br>".join(_temp_list))
        return response_text_list, context_data

    def store_in_previous_contexts_switchcase(self, switch_task, intent, context_data):
        if (switch_task or intent[0][0].strip() == "cancel_task") \
                and context_data["chat_req"]["chat_attributes"]["task"] \
                and context_data["chat_req"]["chat_attributes"]["task"] != intent[0][0].strip() \
                and context_data["chat_req"]["chat_attributes"]["task"] not in self.config_changer().values():

            chat_attributes = deepcopy(context_data["chat_req"]["chat_attributes"])
            for k in chat_attributes["asked_sequence_question"].keys():
                chat_attributes["asked_sequence_question"][k]["count"] = 0

            context_data["previous_contexts"].append(chat_attributes)
            context_data["chat_req"]["chat_attributes"] = deepcopy(self.context_json["chat_req"]["chat_attributes"])

        return context_data

    def restore_previous_task(self, processed_uttarance, context_data, response_text_list):
        if processed_uttarance in ["yes", "y"] and context_data["previous_contexts"]:
            context_data["chat_req"]["chat_attributes"] = deepcopy(
                context_data["previous_contexts"][-1])
            del context_data["previous_contexts"][-1]
            if context_data["chat_req"]["chat_attributes"]["task"] != self.config_changer()["failure_tasks"]:
                response_text_list.append(
                    "Now you are in {}".format(context_data["chat_req"]["chat_attributes"]["task"]))

        else:
            _call_else_block = False
            response_text_list.append("Thanks for visiting.")

        return context_data, response_text_list

    def result_map_process(self, entity_id, extracted_value, context_data, response_text_list):
       
        result_map = self.db["dashboard_resultmap"].find({"entityId": entity_id})
        for each_map in result_map:
            try:
                if extracted_value.lower() == each_map["keyof"].lower():
                    if each_map["redirectTo"] == "#previous_task" or each_map["redirectTo"] == "cancel_task":
                        if each_map["redirectTo"] == "#previous_task":
                            each_map["redirectTo"] = ""
                            context_data["chat_req"]["chat_attributes"] = deepcopy(
                                context_data["previous_contexts"][-1])
                        del context_data["previous_contexts"][-1]

                    elif context_data["chat_req"]["chat_attributes"]["task"] != each_map["redirectTo"]:

                        response_text_list, context_data, button = self.task_completed([], context_data,
                                                                               response_text_list,
                                                                               "clear_previous_data", [])
                    if each_map["redirectTo"]:
                        context_data["chat_req"]["chat_attributes"]["task"] = each_map["redirectTo"]
                        logger.info("----result_map_process-----------... {}".format(each_map["redirectTo"] ))
                    break
            except Exception as e:
                logger.error('result_map_process function  has Exception  error message {} :'.format(e))
                print("result_map_process", e)
        return response_text_list, context_data

    def multi_intent(self, pridicted_intent_list,context_data):
        with open(os.path.join(file_path ,"training_data.json") ) as json_data :
            intents = json.load(json_data)

        intents_list = intents["intents"]
        selected_intents_list=[]
        for i in pridicted_intent_list:
            for j in intents_list:
                if i[0]==j["tag"]:
                    del j["patterns"]
                    selected_intents_list.append(j)
        with open(base_path_json+"/intent_data.json", "w") as intent_data :
            json.dump(selected_intents_list, intent_data, indent=4)

        try:
            new_peidict_list =[ [i[0], str(float(i[1]))]for i in pridicted_intent_list ]
            with open(base_path_json+"/first_intent.json", "w") as intent_data2 :
                json.dump(new_peidict_list ,intent_data2, indent=4 )
        except Exception as e:
            logger.error('multi_intent function  has Exception  error message {} :'.format(e))
            print("Exx---",e)

        context_data["selected_intent_list"] = deepcopy(selected_intents_list)
        return selected_intents_list

    def doller_recommdetion(self, selected_intents_list, val):
        # import ipdb
        # ipdb.set_trace()
        daller_data_list={}
        val1 = val
        try:
            key_set = [k for k, v in selected_intents_list[1].items()]
        except Exception as e:
            logger.error('doller_recommdetion function key_set has Exception  error message :'.format(e))
            print("key_set Exception",e)
            key_set = [k for k, v in selected_intents_list[0].items()]

        # print("---------------------",val)
        # print("key_set", key_set)

        if val=="":
            count = 0
            val =key_set[0]
        else:
            new_selected_list =[]
            for data in selected_intents_list:
                for k, v in data.items():
                    if str(v) == str(val):
                        new_selected_list.append(data)
                        val1 = k
                        # print("--------", k ,v)

            # print("length of new list",len(new_selected_list))
            selected_intents_list=new_selected_list
            with open(base_path_json + "/intent_data.json", "w") as intent_data:
                json.dump(selected_intents_list, intent_data, indent=4)
            # print("selected_intents_list",len(selected_intents_list))

            count = key_set.index(val1) + 1
            if count>=len(key_set):
                count = -1
            else:
                count = key_set.index(val1) + 1
            val = key_set[count]
        # print("selected_intents_list", selected_intents_list)
        daller_data_list[val]= list(set([i[val] for i in selected_intents_list ]))

        try:
            # import ipdb
            # ipdb.set_trace()
            print("daller_data_list in single value : ",daller_data_list )
            print("selected_intents_list in single value : ", selected_intents_list)
            daller_data_list1 = daller_data_list
            for dk, dv in daller_data_list1.items():
                if len(dv)<=1 and dk != "tag" :
                    count = key_set.index(dk) + 1
                    # print("count @@",count)
                    # if len(key_set)<=count:
                    val = key_set[int(count)]
                    daller_data_list = {}
                    daller_data_list[val] = list(set([i[val] for i in selected_intents_list]))
                    # print("@@@@ single value",dv)
        except Exception as e:
            logger.error('doller_recommdetion function has Exception  error message :'.format(e))
            print("daller_data_list Exception",e)
        # print("daller_data_list ",daller_data_list)
        return daller_data_list

    def dollerbutton(self, doller_dict, context_data):
        reply_text=[]
        button = []

        try:
            for k, v in doller_dict.items():
                print("k value", k, v)
                if k == "tag":
                    # print("---------Task is found now----------------")
                    # print("value*************",v[0])
                    context_data["chat_req"]["chat_attributes"]["intent"] = v[0]
                    context_data["chat_req"]["chat_attributes"]["task"] = v[0]
                    context_data["chat_req"]["chat_attributes"]["processed_uttarance"] = v[0]
                    temp_response_text, context_data, button = self.get_intent_questions( v[0],  context_data,  v[0])
                    # print("temp_response_text : ",temp_response_text)
                    reply_text = [{"type": "text",
                                   "sequence": "1",
                                   "value": temp_response_text[0]
                                   }]

                    # print("$$$$$ Context: ", json.dumps(context_data, indent=4))
                else:
                    reply_text=[{"type": "text",
                                "stop_key": k,
                                "sequence": "1",
                                "value": "Okey which {0} is it.".format(k)
                            }]
                    for i in v:
                          button.append({   "title": str(i),
                                            "task": "$redirect-{0}".format(str(i)),
                                            "link": "",
                                            "utterance": ""
                                        })
            context_data["chat_res"]["reply_text"]=reply_text
            context_data["chat_res"]["additional_param"]["button"]=button
        except Exception as e:
            logger.error('dollerbutton function has Exception  error message :'.format(e))
            print("###################FFFFF",e)
        # print("------question_tag------",reply_text,button)
        return context_data




    def main(self, user_uttarance , counter_dict, default_task=False):
        # import ipdb
        # ipdb.set_trace()
        # self.dollerbutton({},dollerbutton)
        print("===== user_uttarance =====  :",user_uttarance)

        logger.info("============================================================================================================================================")
        logger.info("*****************USER HIT******************** {}".format(counter_dict))
        logger.info("*****************USER Uttarance ******************** : {}".format(user_uttarance))

        global bot_req
        bot_req = counter_dict

        user_name = counter_dict["username"]
        # print(user_uttarance, "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,", counter_dict, user_name)

        # print("multi_intents------------------------", context_data["selected_intent_list"])
        switch_task = self.config_changer()["switch_task"]
        start_task = self.config_changer()["start_task"]
        # switch_task= True
        user_id = str(counter_dict['session_key'])
        context_data = self.redis_data(user_id, str(user_name))

        print("srart----")
        context_data["chat_req"]["chat_attributes"]["entities_extracted"]["username"] = str(user_name)
        context_data["chat_req"]["chat_attributes"]["live_user"] = str(True)
        print("srart----")
        # print("Userss Context: ", json.dumps(context_data, indent=4))
        response_text_list = []
        button = []
        response_text = ""
        recommended_task = False

        context_data["chat_req"]["chat_type"] = ""
        context_data["chat_req"]["message_id"] = ""
        context_data["chat_req"]["time_zone"] = ""
        # print("multi_intents------------------------", context_data["chat_res"])
        user_uttarance1=""
        try:
            if user_uttarance.startswith("$redirect-"):
                recommended_task = True
                context_data["chat_req"]["chat_attributes"] = deepcopy(self.context_json["chat_req"]["chat_attributes"])
                # import ipdb
                # ipdb.set_trace()
                with open(base_path_json+"/intent_data.json", "r") as json_data:
                    multi_intents = json.load(json_data)
                intent = user_uttarance.split("-")[1]
                user_uttarance1=intent
                daller_data_list = self.doller_recommdetion(multi_intents, intent)
                replay_text, button = self.dollerbutton(daller_data_list, context_data)
                # if context_data["chat_res"]["reply_text"][0]["stop_key"]=="name":
                #     for i in multi_intents:
                #         for k, v in  i.items():
                #             if k=="name":
                #                 task = i["tag"]
                #     context_data["chat_req"]["chat_attributes"]["task"] = task
                #     context_data["chat_req"]["chat_attributes"]["processed_uttarance"] = intent
                # else:
                #     daller_data_list, recommandetion, val = self.doller_recommdetion(multi_intents, intent)
                #     context_data = self.dollerbutton(daller_data_list, context_data)
                #
                #     return context_data
                # print("multi_intents------------------------", context_data["chat_res"]["data_proceed"])
                # print("multi_intents------------------------", multi_intents)
                # print('--------------------------------$$$$$$$$SS------------------------------')
                # context_data["chat_req"]["chat_attributes"] = deepcopy(self.context_json["chat_req"]["chat_attributes"])
                # intent = [(user_uttarance.split("-")[-1],)]
                # context_data["chat_req"]["chat_attributes"]["processed_uttarance"] = intent

                # if "?" in user_uttarance:
                #     splited_uttrence = user_uttarance.split("?")
                #     user_uttarance = splited_uttrence[0]
                #     intent = [(user_uttarance.split("-")[-1],)]
                #     table_id = splited_uttrence[1].split("=")[1]
                #     context_data["chat_req"]["chat_attributes"]["processed_uttarance"] = user_uttarance
                #
                #     context_data["chat_req"]["chat_attributes"]["entities_extracted"]["planId"] = table_id
                # user_uttarance = ""

            if user_uttarance.startswith("#redirect-"):
                recommended_task = True
                context_data["chat_req"]["chat_attributes"] = deepcopy(self.context_json["chat_req"]["chat_attributes"])
                intent = [(user_uttarance.split("-")[-1],)]
                user_uttarance1 = intent
                context_data["chat_req"]["chat_attributes"]["processed_uttarance"] = intent
                if "?" in user_uttarance:
                    splited_uttrence = user_uttarance.split("?")
                    user_uttarance = splited_uttrence[0]
                    intent = [(user_uttarance.split("-")[-1],)]
                    table_id = splited_uttrence[1].split("=")[1]
                    context_data["chat_req"]["chat_attributes"]["processed_uttarance"] = user_uttarance
                    context_data["chat_req"]["chat_attributes"]["entities_extracted"]["planId"] = table_id 
                user_uttarance = ""
            # import ipdb; ipdb.set_trace()
            if user_uttarance:
                processed_uttarance = self.preprocessor.text_processer(user_uttarance)
                context_data["chat_req"]["uttarance"] = user_uttarance
                context_data["chat_req"]["chat_attributes"]["processed_uttarance"] = processed_uttarance

                classified_label = self.obj_initial_classifirer.test(processed_uttarance)
                label = "".join(list(classified_label["prediction"].keys()))
                print(classified_label, label)
                if label == "general.text" and (classified_label["prediction"][label] > 54) and not \
                context_data["chat_req"]["interview_details"]:
                    print("-------in general------------")
                    logger.info("---- switched--in general-----------... {}".format("general"))
                    
                    response_text = self.aiml_obj.normal_chat(processed_uttarance)
                    if not response_text:
                        response_text = self.unpredictable_query()
                    response_text_list.append(response_text)

                if label == "subjective.text" or not response_text:
                    print("-------in subjective------------")
                    logger.info("---- switched--IN---in subjective-----------... {}".format("switched"))

                    ###### Controller FAQ Vs Intent #####
                    max_intent_score = self.trainer.tester_for_controller(processed_uttarance)
                    max_faq_value = self.faq_obj.max_cosine_value(processed_uttarance)
                    print("Intent Classifier Score-->", max_intent_score)
                    print("FAQ Classifier Score-->", max_faq_value)

                    # if user_uttarance:
                    word_count = processed_uttarance.split(" ")

                    if len(word_count)<=1:
                        response_text = self.unpredictable_query()
                        response_text_list.append(response_text)
                    elif (max_faq_value >= 0.60) and max_faq_value > max_intent_score:
                        print("Go to faq ", max_intent_score)
                        print("and Score is-->", max_faq_value)

                        faq_list = self.faq_obj.faq_engine1(user_uttarance)

                        print("FAQ list-->",faq_list)

                        if faq_list:
                            # for data_list in faq_list:

                            extracted_ans = self.faq_extractor.faq_extractor_function(faq_list)
                            print("extracted_ans @@@@@", extracted_ans)
                            if extracted_ans:
                                context_data["chat_req"]["chat_attributes"]["task"] = "FAQ"
                                context_data["chat_req"]["chat_attributes"]["intent"] = "FAQ"
                                # context_data["chat_req"]["chat_attributes"]["entity"] = "free_text"

                            response_text_list.extend(extracted_ans)
                        else:
                            response_text = self.unpredictable_query()
                            response_text_list.append(response_text)


                    else:
                        logger.info("---- NO DATA FOUND FROM FAQ -----------... {}".format(""))
                        logger.info("----so  NOW IN TASK ENGINE-----------... {}".format("switched"))

                        # import ipdb
                        # ipdb.set_trace()
                        
                        _call_else_block = True

                        intent = []

                        cancel_classifier = self.obj_cancel_task_classifirer.test(processed_uttarance)
                        cancel_label = "".join(list(cancel_classifier["prediction"].keys()))
                        if cancel_label == "cancel_task.text" and (cancel_classifier["prediction"][cancel_label] > 34):
                            intent = [("cancel_task",)]

                        if not context_data["chat_req"]["chat_attributes"]["task"] or switch_task or intent:

                            if not intent and context_data["chat_req"]["ambiguity_resolver"]:
                                if processed_uttarance in context_data["chat_req"]["ambiguity_resolver"]:
                                    intent = [(context_data["chat_req"]["ambiguity_resolver"][processed_uttarance],)]
                                    context_data["chat_req"]["ambiguity_resolver"] = {}

                            if not intent:
                                intent = self.trainer.tester(processed_uttarance)
                                if len(intent)>=2:
                                    print("@$@$@$ Intent :", intent)
                                    pickup_list =[]
                                    inttent_got = True
                                    for iii in intent:
                                        if iii[1]>=0.95:
                                            pickup_list.append(iii)
                                            if len(pickup_list)==1:
                                                inttent_got = False
                                                print("data get intent : ", iii)
                                                context_data["chat_req"]["chat_attributes"]["intent"] = iii[0]
                                                context_data["chat_req"]["chat_attributes"]["task"] = iii[0]
                                                context_data["chat_req"]["chat_attributes"]["processed_uttarance"] = iii[0]
                                                temp_response_text, context_data, button = self.get_intent_questions(iii[0], context_data, iii[0])
                                                print("temp_response_text : ", temp_response_text)
                                                reply_text = [{"type": "text",
                                                               "sequence": "1",
                                                               "value": temp_response_text[0]
                                                               }]
                                                context_data["chat_res"]["reply_text"] = reply_text

                                            else:
                                                inttent_got = True
                                    if inttent_got:
                                             multi_intents = self.multi_intent(intent, context_data)
                                             # print("@@@@@",multi_intents)
                                             daller_data_list= self.doller_recommdetion(multi_intents, "")
                                             replay_text, button= self.dollerbutton(daller_data_list, context_data)


                                prev_task = context_data["chat_req"]["chat_attributes"]["task"]
                                if intent and ((prev_task and prev_task in self.config_changer()["start_task"]) or  not switch_task):
                                    context_data["chat_req"]["chat_attributes"] = deepcopy(self.context_json["chat_req"]["chat_attributes"])


                            holding_previous_task = self.config_changer()["holding_previous_task"]
                            print("---------------------========", intent)

                            if intent:
                                if len(intent) > 1 and intent[0][1] - intent[1][1] > 0.0:
                                    response_text_list, context_data = self.ambiguity_resolver_func(response_text_list,
                                                                                                    context_data,
                                                                                                    intent)

                                if len(context_data["previous_contexts"]) <= holding_previous_task:

                                    context_data = self.store_in_previous_contexts_switchcase(switch_task, intent,
                                                                                              context_data)

                                    if not context_data["chat_req"]["ambiguity_resolver"] and (
                                            not context_data["chat_req"]["chat_attributes"]["task"] or
                                            context_data["chat_req"]["chat_attributes"]["task"] != intent[0][0].strip()):
                                        _call_else_block = False
                                        context_data["chat_req"]["chat_attributes"]["task"] = intent[0][0].strip()
                                        print("get_intent_questions $$$$",intent[0][0])
                                        temp_reply_text_list, context_data, button = self.get_intent_questions(intent[0][0].strip(),
                                                                                                       context_data,
                                                                                                       processed_uttarance)
                                        response_text_list.extend(temp_reply_text_list)

                            elif not switch_task:
                                pass
                            elif context_data["chat_req"]["chat_attributes"][
                                "current_asked_question"] == "previous_task_confirmation":

                                context_data, response_text_list = self.restore_previous_task(processed_uttarance,
                                                                                              context_data,
                                                                                              response_text_list)

                        if _call_else_block:

                            if context_data["chat_req"]["chat_attributes"]["current_asked_question"]:
                                current_sequence = context_data["chat_req"]["chat_attributes"]["current_asked_question"]
                                if str(current_sequence) in context_data["chat_req"]["chat_attributes"][
                                    "asked_sequence_question"]:
                                    
                                    tobe_processed =context_data["chat_req"]["chat_attributes"]["asked_sequence_question"][str(current_sequence)]
                                    entity_id = tobe_processed.get("Entity_Id", "")
                                    entity_name = tobe_processed.get("Entity_Name", "")

                                    extracted_value, context_data, free_text_case, _ = self.val_extractor(tobe_processed, entity_id,
                                                                                                          processed_uttarance,
                                                                                                          context_data)
                                    if extracted_value:
                                      
                                        if tobe_processed["task_redirect"].lower() in ["yes"]:
                                            response_text_list, context_data = self.result_map_process(entity_id,
                                                                                                       extracted_value,
                                                                                                       context_data,
                                                                                                       response_text_list)

                                        context_data["chat_req"]["chat_attributes"]["entities_extracted"][
                                            entity_name] = extracted_value

                            temp_response_text, context_data, button = self.get_intent_questions(
                                context_data["chat_req"]["chat_attributes"]["task"],
                                context_data,
                                processed_uttarance)
                            response_text_list.extend(temp_response_text)

                            if not response_text_list:
                                response_text = self.unpredictable_query()
                                response_text_list.append(response_text)
            elif default_task or recommended_task:
            
                if default_task:
                    intent = [(self.config_changer()["start_task"],)]

                context_data["chat_req"]["chat_attributes"]["task"] = intent[0][0].strip()
                temp_reply_text_list, context_data, button = self.get_intent_questions(intent[0][0].strip(), context_data,  "")
                response_text_list.extend(temp_reply_text_list)

            # context_data["chat_res"]["reply_text"] = response_text_list
            context_data["chat_res"]["reply_text"] = []
            for ind, each_responce in enumerate(response_text_list):
                if isinstance(each_responce, dict):
                    each_responce["sequence"] = str(ind+1)
                    context_data["chat_res"]["reply_text"].append(each_responce)
                if isinstance(each_responce, str):
                    context_data["chat_res"]["reply_text"].append({
                        "type": "text",
                        "sequence": str(ind+1),
                        "value": each_responce})
                    
            context_data["chat_res"]["additional_param"]["button"] = button
            # print("last -----------",context_data["chat_res"]["data_proceed"])

            print("Users Context to store: ", json.dumps(context_data, indent=4))
            self.redis_obj.setex(user_id, TTL, json.dumps(context_data))

        except Exception as e:
            print("Exception in Main function",e)
            logger.error("Exception in Main function : {}".format(e))
        print("Userss Context: ", json.dumps(context_data, indent=4))
        logger.info("*****************Final Replay context_data ******************** : \n {}".format(json.dumps(context_data, indent=4)))
        try:
            history_data_dict={
                "request_data":"",
                "responce_data":"",
                "task_name":"",
                "task_type":"",
                "request_user":"",
                "responce_user":""
            }
            if user_uttarance:
                if context_data["chat_res"]["additional_param"]["button"]:
                    history_data_dict["task_type"]="recommendation"
                    history_data_dict["task_name"] = "recommendation"
                else:
                    if context_data["chat_req"]["chat_attributes"]["task"] == "FAQ":
                        history_data_dict["task_type"]="FAQ"
                        history_data_dict["task_name"] = "FAQ"
                        history_data_dict["responce_data"] = [{i["sequence"]:i["value"]} for i in
                                                              context_data["chat_res"]["reply_text"]]
                    else:
                        history_data_dict["task_type"] = "Task"
                        history_data_dict["task_name"] = context_data["chat_req"]["chat_attributes"]["task"]
                        history_data_dict["responce_data"] = [i["value"] for i in
                                                              context_data["chat_res"]["reply_text"]]
                history_data_dict["request_data"]=str(user_uttarance1)

                history_data_dict["request_user"] = context_data["identifier"]["user_name"].capitalize()
                history_data_dict["responce_user"] = "chatbot".capitalize()
                self.chat_history(history_data_dict)

        except Exception as e:
            print("Exception in while chat history Save", e)
            logger.error("Exception inwhile chat history Save : {}".format(e))

        return context_data

    def unpredictable_query(self):
        resp_text = ""
        try:
            list_prper_data = ["Sorry, I did not understand that..",
                               "I did not understand, Please try in different way.",
                               "Hey I am not sure about that ...please try different way.",
                               "Hey buddy...! please try with different keywords"]
            resp_text = random.choice(list_prper_data)
        except Exception as e:
            print("Exception in unpredictable_query: ", traceback.format_exc(), e)
        return resp_text

    def redis_data(self, user_id, user_name):
        try:
            if self.redis_obj.exists(user_id):
                redis_data = json.loads(self.redis_obj.get(user_id).decode("utf8"))
            else:
                redis_data = deepcopy(self.context_json)
                redis_data["identifier"]["user_id"] = user_id
                redis_data["identifier"]["user_name"] = user_name
                self.redis_obj.setex(user_id, TTL, json.dumps(redis_data))
        except:
            print("Exception in redis_data: ", traceback.format_exc())
        return redis_data


if __name__ == '__main__':
    obj = CounterLogic()
    c = 1
    while True:
        print("\n", "-=" * 60)
        q = input("\nQUESTION " + str(c) + ": ")
        context_data = obj.main(q, 11100021)
        print("-=" * 60)
        print("QUESTION " + str(c) + "--> ", q)
        for e in context_data["chat_res"]["reply_text"]:
            print("ANSWER-->     ", e)
            if len(context_data["chat_res"]["reply_text"]) > 1:
                sleep(1)
        c += 1





