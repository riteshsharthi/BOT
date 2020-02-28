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
from .faq_engine_updated_for_G import Faq_Engine
from exusers.models import MyUser

from .faq_funcation import FAQ_Extractor
from FAQ.models import *
import pdb

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base_path_json = os.path.join(base_dir, 'nlp_engine')
from .date_wise_log import logger



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
        self.db = self.mongo_conn["bot"]
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
        return (config_json)

    def viewbot_save(self, request, task, data):
        try:
            deep_task = task
            extrected_data = data
            print(extrected_data)
            intent = IntentToTask.objects.get(Intent_Name=deep_task)
            # print(intent)
            questions = TaskToEntity.objects.filter(Task_Id=intent.id)
            # print(questions)
            for question in questions:
                for x, y in extrected_data.items():
                    if x == question.Entity_Name:
                        if len(ExtractedUserData.objects.all()) == 0:
                            id = 1
                        else:
                            id = max(i.id for i in ExtractedUserData.objects.all()) + 1
                        a = ExtractedUserData.objects.create(id=id, Task_Id=question.id,
                                                             Entity_Name=x, Entity_Id=question.Entity_Id,
                                                             Entity_Question=question.Entity_Question,
                                                             user_chat=str(request['username']),
                                                             Entity_Sequence=question.Entity_Sequence,
                                                             Entity_Value=str(y),
                                                             Session_key=str(request['session_key']),
                                                             Datetime_chat=str(
                                                                 datetime.now().strftime("%A, %d. %B %Y %I:%M%p")))
                        a.save()
                        print("Okey save")

        except Exception as e:
            print("Exception in Extrected data save : ", e)

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
        logger.info( "____---------_____Action url_________------------___________ {} {}".format(data,  url ))
        f_resp = ""

        del data['action_url']
        try:
            responce_data = requests.post(url=url, json=data, timeout=10)
            if responce_data.status_code == 200:
                get_data = responce_data.json()
               

                print(get_data, "_______________FINAL_RSULT_____N")
                if "message" in get_data:
                    f_resp = get_data["message"]
                    logger.info(  "-------- FINAL MESSAGE -------- {}".format(f_resp))
                else:
                    f_resp = "Sorry data not found for this id. Please try again"
        except Exception as e:
            print("Exception in call_rest_api", e)
        # f_dict =self.flatten_complex_dict(get_data)
        # print(get_data)
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

            responce_data = requests.post(url=url, json=data, timeout=10)
            logger.info(  "__________PRE ACTION URL_________________ {}".format(url,data ))
            if responce_data.status_code == 200:
                get_data = responce_data.json()
                temp_resp = get_data.get("message", "")
                if temp_resp:
                    resp.append(temp_resp)

        except Exception as e:
            print("Exception in call_rest_api", e)

        return resp

    def post_action_func(self, task_data, context_data, reply_text_list, processed_uttarance, button):
        reply_text_list, context_data = self.task_completed([], context_data,
                                                            reply_text_list,
                                                            "clear_previous_data")
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

    def recommended(self, each_question):
        import pdb
        pdb.set_trace()
     
        button = []
        primary_id = each_question["_id"]
        recommende_data = self.db["recommunded_data"].find({"entity_id": str(primary_id)})
        if recommende_data.count():
            for each in recommende_data:
                button.append(each) 
        return button

    def get_intent_questions(self, task_name, context_data, processed_uttarance):
       
        
        button = []
        reply_text_list = []
        task_data = self.db["intent_to_task"].find({"Intent_Name": task_name})
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
                all_questions = self.db["task_to_entity"].find({"Task_Id": task_id}).sort([("Entity_Sequence", 1)])
                temp_all_questions = deepcopy(all_questions)
                multi_answering = self.config_changer()["multi_answering"]
                # multi_answering = True

                if multi_answering and context_data["chat_req"]["chat_attributes"]["task"] not in [
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

                            button = self.recommended(each_question)
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
                                reply_text_list, context_data = self.task_completed(task_data, context_data,
                                                                                    reply_text_list, "failure")
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
                            reply_text_list, context_data = self.task_completed(task_data, context_data,
                                                                                reply_text_list, "blank_entity")
                            if task_data[0].get("post_action", ""):
                                reply_text_list, context_data, button = self.post_action_func(task_data, context_data,
                                                                                      reply_text_list,
                                                                                      processed_uttarance, button)
                        ######################################POST ACTION End
                        break
                else:
                    if context_data["chat_req"]["chat_attributes"]["task"] == "failuretask":
                        reply_text_list, context_data = self.task_completed(task_data, context_data, reply_text_list,
                                                                            "failure")

                    else:
                        reply_text_list, context_data = self.task_completed(task_data, context_data, reply_text_list,
                                                                            "completed")
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
            print("Exception in get_intent_questions ", e)
        return reply_text_list, context_data, button

    def task_completed(self, task_data, context_data, reply_text_list, type_of_action):

        print("in task completed===============")
        data_to_hit = {}
        print(bot_req['user_id'], "%%%%%%%%%%%")

        deep_task = deepcopy(context_data["chat_req"]["chat_attributes"]["task"])

        all_extracted_entities = deepcopy(context_data["chat_req"]["chat_attributes"]["entities_extracted"])
        data_to_hit = all_extracted_entities

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

            print(json.dumps(data_to_hit, indent=3))

            try:
                recodOFtask = self.db["intent_to_task"].find({"Intent_Name": str(deep_task)})
                # print(recodOFtask)
                trigg = []
                for i in recodOFtask:
                    trigg.append(i)

                triggerName = trigg[0]["Task_Name"]
                data_to_hit["triggerName"] = str(triggerName)
            except Exception as e:
                print("trigg @@@@", e)

            # reply_text = requests.post(url=url_data, json=data_k)

            reply_text = self.call_rest_api(self.flatten_dict(data_to_hit), action_url)

            clean_hit_data = data_to_hit
            del clean_hit_data['action_url']
            # context_data["chat_req"]["time_zone"] = clean_hit_data
            self.viewbot_save(bot_req, deep_task, clean_hit_data)
            print('reply text from rest api ---->', reply_text)
            reply_text_list.append(reply_text)
            previous_task_confirmation = self.config_changer()["switch_task_confirmation"]
            # previous_task_confirmation = True

            if context_data["previous_contexts"] and previous_task_confirmation:
                context_data["chat_req"]["chat_attributes"]["current_asked_question"] = "previous_task_confirmation"
                reply_text_list.append("Do you want to proceed with previous query?")

        return reply_text_list, context_data

    def val_extractor(self, task2entity_detail, entity_id, processed_uttarance, context_data):
        import pdb
        extracted_value = ""
        regex_pattern = ""
        tobe_extracted = []
        free_text_case = ""
        match_data = False
        json_data = []
        if entity_id:
            tobe_extracted = self.db["entity"].find({"_id": entity_id})
            print(tobe_extracted[0],
                  "tobe_extractedtobe_extractedtobe_extractedtobe_extractedtobe_extractedtobe_extractedtobe_extractedtobe_extracted")
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
                        print(json_data, "_______________FINAL_RSULT_____N")
                        
                except Exception as e:
                    print("Exception in call_rest_api", e)

            if match_data and json_data:
             
                uttarance = context_data["chat_req"]["uttarance"]
                for each_pattern in json_data:
                    extracted_value = re.search(str(each_pattern), uttarance, flags=re.IGNORECASE)
                    if extracted_value:
                        extracted_value = extracted_value.group()
                        break

        # if extracted_value:
            

        return extracted_value, context_data, free_text_case, regex_pattern

    def ambiguity_resolver_func(self, response_text_list, context_data, intent):
        # diff = intent[0][1]-intent[1][1]
        _temp_list = []
        for ind, eintent in enumerate([intent[0][0], intent[1][0]]):
            for qdata in self.db["recommend_variation"].find({"tag": eintent}):
                _temp_list.append(str(ind + 1) + ": " + random.choice(qdata["patterns"]))
                context_data["chat_req"]["ambiguity_resolver"][str(ind + 1)] = eintent

        if _temp_list:
            _call_else_block = False
            response_text_list.append(
                " Please select 1 or 2\n\n<br>" + "\n<br>".join(_temp_list))
        return response_text_list, context_data

    def store_in_previous_contexts_switchcase(self, switch_task, intent, context_data):
        if (switch_task or intent[0][0] == "cancel_task") \
                and context_data["chat_req"]["chat_attributes"]["task"] \
                and context_data["chat_req"]["chat_attributes"]["task"] != intent[0][0] \
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
       
        result_map = self.db["result_map"].find({"entityId": entity_id})
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

                        response_text_list, context_data = self.task_completed([], context_data,
                                                                               response_text_list,
                                                                               "clear_previous_data")
                    if each_map["redirectTo"]:
                        context_data["chat_req"]["chat_attributes"]["task"] = each_map["redirectTo"]
                        logger.info("----result_map_process-----------... {}".format(each_map["redirectTo"] ))
                    break
            except Exception as e:
                print("result_map_process", e)
        return response_text_list, context_data

    def main(self, user_uttarance , counter_dict, default_task=False):
 
        logger.info(  "========================================================================= {}".format(""))
        logger.info(  "=============================================================================== {}".format(""))
        logger.info(  "*****************USER HIT******************** {} {}".format(user_uttarance , counter_dict))

        global bot_req
        bot_req = counter_dict

        user_name = counter_dict["username"]
        print(user_uttarance, "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,", counter_dict, user_name)

        # ye problem kregs mers nsm mst lensa priyanka

        switch_task = self.config_changer()["switch_task"]
        start_task = self.config_changer()["start_task"]
        # switch_task= True
        user_id = str(counter_dict['session_key'])
        context_data = self.redis_data(user_id, str(user_name))
        channel_id = MyUser.objects.get(username=counter_dict['username']).kapitaxid
        context_data["chat_req"]["chat_attributes"]["entities_extracted"]["username"] = channel_id

        print("Userss Context: ", json.dumps(context_data, indent=4))
        response_text_list = []
        button = []
        response_text = ""
        recommended_task = False

        context_data["chat_req"]["chat_type"] = ""
        context_data["chat_req"]["message_id"] = ""
        context_data["chat_req"]["time_zone"] = ""
        try:
            if user_uttarance.startswith("#redirect-"):
                recommended_task = True
                intent = [(user_uttarance.split("-")[-1],)]
                user_uttarance = ""

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
                    max_faq_value=self.faq_obj.max_cosine_value(processed_uttarance)
                    print("Intent Classifier Score-->", max_intent_score)
                    print("FAQ Classifier Score-->", max_faq_value)

                    if max_faq_value > max_intent_score:
                        print("Go to faq")
                        print("and Score is-->", max_faq_value)

                        faq_list = self.faq_obj.faq_engine1(user_uttarance)



                        if faq_list:
                            for data_list in faq_list:

                                extracted_ans = self.faq_extractor.faq_extractor_function(data_list)
                                print("extracted_ans @@@@@", extracted_ans)
                                response_text_list.append(extracted_ans)


                    else:
                        logger.info("---- NO DATA FOUND FROM FAQ -----------... {}".format(""))
                        logger.info("----so  NOW IN TASK ENGINE-----------... {}".format("switched"))
                  
                       
                        
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

                            # if not intent:
                            #     response_text = self.aiml_obj.normal_chat(processed_uttarance)

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
                                            context_data["chat_req"]["chat_attributes"]["task"] != intent[0][0]):
                                        _call_else_block = False
                                        context_data["chat_req"]["chat_attributes"]["task"] = intent[0][0]
                                        temp_reply_text_list, context_data, button = self.get_intent_questions(intent[0][0],
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

                context_data["chat_req"]["chat_attributes"]["task"] = intent[0][0]
                temp_reply_text_list, context_data, button = self.get_intent_questions(intent[0][0],
                                                                               context_data,
                                                                               "")
                response_text_list.extend(temp_reply_text_list)

            context_data["chat_res"]["reply_text"] = response_text_list
           
            context_data["chat_res"]["additional_param"]["button"] = button

            print("Users Context to store: ", json.dumps(context_data, indent=4))
            self.redis_obj.setex(user_id, TTL, json.dumps(context_data))

        except Exception as e:
            print(e)
        return context_data

    def unpredictable_query(self):
        resp_text = ""
        try:
            list_prper_data = ["Sorry, I did not understand that..",
                               "My robot brain is not sure about that one...Please try asking a different way.",
                               "Hey I am not sure about that ...please try different way.",
                               "Hey buddy...! please try with different keywords"]
            resp_text = random.choice(list_prper_data)
        except Exception as e:
            print("Exception in unpredictable_query: ", traceback.format_exc(), e)
        return resp_text

    def redis_data(self, user_id, user_name):
        # import pdb
        #
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







