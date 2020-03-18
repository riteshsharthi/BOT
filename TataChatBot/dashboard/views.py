from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404,  HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.core.files.storage import FileSystemStorage
import pandas as pd
import os
import json
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_json =os.path.join(base_dir, "faq_component/")
# Create your views here.

########## #this for Entity data Table and form ####################
@login_required(login_url='/accounts/login/')
def Entity_Details(request):
    dict_contaxt = {}
    entity_detail = Entity.objects.all()
    dict_contaxt['entity_detail'] = entity_detail
    return render(request, 'dashboard/entity.html', dict_contaxt )

@login_required(login_url='/accounts/login/')
def Entity_Create(request):
    dict_con = {}
    entity_detail = Entity.objects.all()
    # print(request)
    if request.method == 'POST':
        EntityType = request.POST['EType']
        EntityName = request.POST['EName']
        EntityRegex = request.POST['ERegex']
        if len(entity_detail)==0:
            idss = 1
        else:
            idss =max(i.id for i in entity_detail)+1
        a = Entity.objects.create(id=idss, Entity_Type=EntityType.strip(), Entity_Name=EntityName.strip(), Entity_Regex=EntityRegex.strip())
        a.save()
    entity_detail = Entity.objects.all()
    dict_con['entity_detail'] = entity_detail
    # return render(request, 'dashboard/entity.html', dict_con)
    return HttpResponseRedirect("/dashboard/entity/")

@login_required(login_url='/accounts/login/')
def Entity_delete(request, id):
    dict_con = {}

    if len(Entity.objects.all()) == 1:
        dict_con['last_one_data_error'] = "Sorry you can't Delete last Record. Becouse one data is mandatory "
    else:
        a = Entity.objects.filter(id=id).delete()
        dict_con['a'] = a
    entity_detail = Entity.objects.all()
    dict_con['entity_detail'] = entity_detail
    # return render(request, 'dashboard/entity.html', dict_con)
    return HttpResponseRedirect("/dashboard/entity/")

@login_required(login_url='/accounts/login/')
def Entity_edit(request,id):
    dict_con = {}
    entity_edit1 = Entity.objects.get(id=id)
    dict_con['entity_edit1'] = entity_edit1
    # return render(request, 'dashboard/entity.html', dict_con)
    return HttpResponseRedirect("/dashboard/entity/")

@login_required(login_url='/accounts/login/')
def Entity_edit1(request):
    dict_con = {}
    if request.method == 'POST':
        eid = int(request.POST['eid'])
        EntityType = request.POST['EType']
        EntityName = request.POST['EName']
        EntityRegex = request.POST['ERegex']
        print("#########", eid)
        edit_entity = Entity.objects.get(pk=str(eid))
        print("edit_entity",edit_entity)
        edit_entity.Entity_Type=EntityType
        edit_entity.Entity_Name=EntityName
        edit_entity.Entity_Regex=EntityRegex
        edit_entity.save()
        # .update_many(Entity_Type=EntityType, Entity_Name=EntityName,  Entity_Regex=EntityRegex)
    entity_detail = Entity.objects.all()
    dict_con['entity_detail'] = entity_detail
    # return render(request, 'dashboard/entity.html', dict_con)
    return HttpResponseRedirect("/dashboard/entity/")



########## #this for IntentToTask data Table  and form ####################

@login_required(login_url='/accounts/login/')
def IntentToTask_Details(request):
    dict_contaxt = {}
    intenttotask_detail = IntentToTask.objects.all()
    dict_contaxt['intenttotask_detail'] = intenttotask_detail
    return render(request, 'dashboard/intent.html', dict_contaxt )


@login_required(login_url='/accounts/login/')
def IntentToTask_Create(request):
    dict_con = {}
    intenttotask_detail = IntentToTask.objects.all()
    # print(request)
    if request.method == 'POST':
        IntentName = request.POST['IName']
        TaskName = request.POST['TName']
        ActionUrl = request.POST['AUrl']
        post_action = request.POST['post_action']

        if len(intenttotask_detail)==0:
            idss = 1
        else:
            idss =max(i.id for i in intenttotask_detail)+1
        a = IntentToTask.objects.create(id=idss, Intent_Name=IntentName, Task_Name=TaskName, Action_Url=ActionUrl,post_action=post_action)
        a.save()
    intenttotask_detail = IntentToTask.objects.all()
    dict_con['intenttotask_detail'] = intenttotask_detail
    # return render(request, 'dashboard/intent.html', dict_con)
    return HttpResponseRedirect("/dashboard/intenttotask/")

@login_required(login_url='/accounts/login/')
def IntentToTask_delete(request, id):
    dict_con = {}
    if len(Entity.objects.all()) == 1:
        dict_con['last_one_data_error'] = "Sorry you can't Delete last Record. Becouse one data is mandatory "
    else:
        a = Entity.objects.filter(id=id).delete()
        dict_con['a'] = a
    a = IntentToTask.objects.filter(id=id).delete()
    dict_con['a'] = a
    intenttotask_detail = IntentToTask.objects.all()
    dict_con['intenttotask_detail'] = intenttotask_detail
    # return render(request, 'dashboard/intent.html', dict_con)
    return HttpResponseRedirect("/dashboard/intenttotask/")

@login_required(login_url='/accounts/login/')
def IntentToTask_edit(request,id):
    dict_con = {}
    # entity_detail = Entity.objects.all()
    intenttotask_edit1 = IntentToTask.objects.get(id=id)
    # dict_con['entity_detail'] = entity_detail
    dict_con['intenttotask_edit1'] = intenttotask_edit1
    # print(request)

    # return render(request, 'dashboard/intent.html', dict_con)
    return HttpResponseRedirect("/dashboard/intenttotask/")

@login_required(login_url='/accounts/login/')
def IntentToTask_edit1(request):
    dict_con = {}
    intenttotask_detail = IntentToTask.objects.all()
    # entity_edit = Entity.objects.get(id)
    dict_con['intenttotask_detail'] = intenttotask_detail
    # dict_con['entity_edit'] = entity_edit
    # print(request)
    if request.method == 'POST':
        Iid = int(request.POST['Iid'])
        IntentName = request.POST['IName']
        TaskName = request.POST['TName']
        ActionUrl = request.POST['AUrl']
        post_action = request.POST['post_action']
        Intent_edit =IntentToTask.objects.get(id=Iid)
        Intent_edit.Intent_Name=IntentName
        Intent_edit.Task_Name=TaskName
        Intent_edit.Action_Url=ActionUrl
        Intent_edit.post_action=post_action
        Intent_edit.save()

    # return render(request, 'dashboard/intent.html', dict_con)
    return  HttpResponseRedirect("/dashboard/intenttotask/")


############################### TaskToEntity #########################################

@login_required(login_url='/accounts/login/')
def TaskToEntity_Details(request):
    dict_con = {}
    entity_detail = Entity.objects.all()
    tasktoentity_detail = TaskToEntity.objects.all()
    intenttotask_detail = IntentToTask.objects.all()
    dict_con['entity_detail'] = entity_detail
    dict_con['intenttotask_detail'] = intenttotask_detail
    dict_con['tasktoentity_detail'] = tasktoentity_detail

    return render(request, 'dashboard/task.html', dict_con )


@login_required(login_url='/accounts/login/')
def TaskToEntity_Create(request):
    dict_con = {}
    entity_detail = Entity.objects.all()
    tasktoentity_detail = TaskToEntity.objects.all()
    intenttotask_detail = IntentToTask.objects.all()
    dict_con['entity_detail'] = entity_detail
    dict_con['intenttotask_detail'] = intenttotask_detail
    dict_con['tasktoentity_detail'] = tasktoentity_detail
    # print(request)
    if request.method == 'POST':
        taskid = request.POST['Taskid']
        intentname = request.POST['IName']
        entityId = request.POST['EntityId']
        entityquestion = request.POST['Entityquestion']
        entitysequence = request.POST['Entitysequence']
        task_redirect = request.POST['taskredirect']
        pre_text = request.POST['pre_text']
        pre_action_url = request.POST['pre_action_url']
        # interview_url = request.POST['interview_url']
        # value_collection_name = request.POST['value_collection_name']
        # collection_url = request.POST['collection_url']
        # validation_url = request.POST['validation_url']
        Entity_alternet_qustion = (request.POST['AlternetQuestion']).split(',')
        if len(tasktoentity_detail)==0:
            idss = 1
        else:
            idss =max(i.id for i in tasktoentity_detail)+1

        a = TaskToEntity.objects.create(id=idss,Task_Id=taskid.strip() , Entity_Name=intentname.strip(), Entity_Id=entityId,
                                        Entity_Question=entityquestion.strip(), Entity_alternet_qustion=Entity_alternet_qustion,
                                        task_redirect=task_redirect.strip(), Entity_Sequence=entitysequence.strip(),
                                        pre_text=pre_text.strip(), pre_action_url=pre_action_url.strip()
                                        # interview_url=interview_url.strip(),
                                        # value_collection_name=value_collection_name.strip(),
                                        # collection_url=collection_url.strip(),
                                        # validation_url=validation_url.strip()
                                        )
        a.save()
    entity_detail = Entity.objects.all()
    tasktoentity_detail = TaskToEntity.objects.all()
    intenttotask_detail = IntentToTask.objects.all()
    dict_con['entity_detail'] = entity_detail
    dict_con['intenttotask_detail'] = intenttotask_detail
    dict_con['tasktoentity_detail'] = tasktoentity_detail

    # return render(request, 'dashboard/task.html', dict_con)
    return  HttpResponseRedirect("/dashboard/tasktoentity/")



def TaskToEntity_delete(request, id):
    dict_con = {}
    try:
        TaskToEntity.objects.get(id=id).delete()
    except Exception as e:
        print(" TaskToEntity_delete ",e)
    tasktoentity_detail = TaskToEntity.objects.all()
    dict_con['tasktoentity_detail'] = tasktoentity_detail
    return HttpResponseRedirect("/dashboard/tasktoentity/")


def TaskToEntity_edit(request,id):
    dict_con = {}
    entity_detail = Entity.objects.all()
    intenttotask_detail = IntentToTask.objects.all()
    tasktoentity_edit1 = TaskToEntity.objects.get(id=id)
    dict_con['entity_detail'] = entity_detail
    dict_con['intentname'] = intenttotask_detail
    dict_con['tasktoentity_edit1'] = tasktoentity_edit1
    # print(request)

    return HttpResponseRedirect("/dashboard/tasktoentity/")

@login_required(login_url='/accounts/login/')
def TaskToEntity_edit1(request):
    dict_con = {}
    entity_detail = Entity.objects.all()
    tasktoentity_detail = TaskToEntity.objects.all()
    intenttotask_detail = IntentToTask.objects.all()
    dict_con['entity_detail'] = entity_detail
    dict_con['intenttotask_detail'] = intenttotask_detail
    dict_con['tasktoentity_detail'] = tasktoentity_detail
    # entity_edit = Entity.objects.get(id)
    # dict_con['entity_edit'] = entity_edit
    # print(request)
    if request.method == 'POST':
        Iid = int(request.POST['Iid'])
        taskid = request.POST['Taskid']
        intentname = request.POST['IName']
        entityId = request.POST['EntityId']
        entityquestion = request.POST['Entityquestion']
        entitysequence = request.POST['Entitysequence']
        task_redirect = request.POST['taskredirect']
        pre_text = request.POST['pre_text']
        pre_action_url = request.POST['pre_action_url']
        # interview_url = request.POST['interview_url']
        # value_collection_name = request.POST['value_collection_name']
        # collection_url = request.POST['collection_url']
        # validation_url = request.POST['validation_url']
        Entity_alternet_qustion = (request.POST['AlternetQuestion']).split(',')
        Entity_alternet_qustion = [x for x in Entity_alternet_qustion if x]
        Task_edit = TaskToEntity.objects.get(id=Iid)
        Task_edit.Task_Id=taskid
        Task_edit.Entity_Name=intentname
        Task_edit.Entity_Id=entityId
        Task_edit.Entity_Question=entityquestion.strip()
        Task_edit.pre_text=pre_text.strip()
        Task_edit.Entity_Sequence=entitysequence.strip()
        Task_edit.pre_action_url=pre_action_url.strip()
        Task_edit.Entity_alternet_qustion=Entity_alternet_qustion
        Task_edit.task_redirect=task_redirect.strip()
        # Task_edit.interview_url=interview_url.strip()
        # Task_edit.value_collection_name=value_collection_name.strip()
        # Task_edit.collection_url=collection_url.strip()
        # Task_edit.validation_url=validation_url.strip()
        Task_edit.save()

    return HttpResponseRedirect("/dashboard/tasktoentity/")


########## #this for ResultMap data Table  and form ####################
@login_required(login_url='/accounts/login/')
def result_map(request):
    dict_con = {}
    ResultMap_all = ResultMap.objects.all()
    tasktoentity_detail = TaskToEntity.objects.all()
    entity_detail = Entity.objects.all()
    intenttotask_detail = IntentToTask.objects.all()
    dict_con['ResultMap_all'] = ResultMap_all
    dict_con['tasktoentity_detail'] = tasktoentity_detail
    dict_con['entity_detail'] = entity_detail
    dict_con['intenttotask_detail'] = intenttotask_detail
    return render(request, 'dashboard/resultmap.html', dict_con)

@login_required(login_url='/accounts/login/')
def result_map_create(request):
    dict_con = {}
    ResultMap_all = ResultMap.objects.all()
    dict_con['ResultMap_all'] = ResultMap_all
    entity_detail = Entity.objects.all()
    intenttotask_detail = IntentToTask.objects.all()
    dict_con['entity_detail'] = entity_detail
    dict_con['intenttotask_detail'] = intenttotask_detail

    # print(request)
    if request.method == 'POST':
        taskid = request.POST['TaskID']
        entityid = request.POST['EntityID']
        keyof = request.POST['Key']
        redirectto = request.POST['Redirectto']
        if len(ResultMap_all) == 0:
            idss = 1
        else:
            idss = max(i.id for i in ResultMap_all) + 1
        a = ResultMap.objects.create(id=idss, taskId=taskid, entityId=entityid,
                                     keyof=keyof, redirectTo=redirectto)
        a.save()

    ResultMap_all = ResultMap.objects.all()
    tasktoentity_detail = TaskToEntity.objects.all()
    dict_con['ResultMap_all'] = ResultMap_all
    dict_con['tasktoentity_detail'] = tasktoentity_detail

    # return render(request, 'dashboard/resultmap.html', dict_con)
    return HttpResponseRedirect("/dashboard/resultmap/")

@login_required(login_url='/accounts/login/')
def result_map_update(request, id):
    dict_con = {}
    ResultMap_edit = ResultMap.objects.get(id=id)
    dict_con['ResultMap_edit'] = ResultMap_edit

    return render(request, 'dashboard/resultmap.html', dict_con)
    # return HttpResponseRedirect("/dashboard/resultmap/")

@login_required(login_url='/accounts/login/')
def result_map_update1(request):
    dict_con = {}
    if request.method == 'POST':
        Rid = request.POST['eid']
        taskid = request.POST['TaskID']
        entityid = request.POST['EntityID']
        keyof = request.POST['Key']
        redirectto = request.POST['Redirectto']
        ResultMap.objects.get(id=Rid).update(taskId=taskid, entityId=entityid, keyof=keyof, redirectTo=redirectto)


    ResultMap_all = ResultMap.objects.all()
    dict_con['ResultMap_all'] = ResultMap_all
    entity_detail = Entity.objects.all()
    intenttotask_detail = IntentToTask.objects.all()
    dict_con['entity_detail'] = entity_detail
    dict_con['intenttotask_detail'] = intenttotask_detail
    # return render(request, 'dashboard/resultmap.html', dict_con)
    return HttpResponseRedirect("/dashboard/resultmap/")

@login_required(login_url='/accounts/login/')
def result_map_delete(request,id):
    dict_con = {}
    try:
        ResultMap.objects.get(id=id).delete()

    except Exception as e:
        print("this is ",id," id not found",e)

    ResultMap_all = ResultMap.objects.all()
    dict_con['ResultMap_all'] = ResultMap_all

    # return render(request, 'dashboard/resultmap.html', dict_con)
    return HttpResponseRedirect("/dashboard/resultmap/")

########## #this for ResultMap data Table  and form ####################
path = '/var/www/html/media'
from django.core import serializers

@login_required(login_url='/accounts/login/')
def faq_data(request):
    dict_con = {}
    faq_detail = FAQ.objects.all()[::-1]
    dict_con['username'] = request.user
    parental_node_data_detail = NodesModule.objects.all()
    post_list = serializers.serialize('json', parental_node_data_detail)
    dict_con['parental_node_data_detail'] = parental_node_data_detail
    dict_con['parental_node_data_detail_json'] = post_list
    paginator = Paginator(faq_detail, 4 )  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    dict_con['faq_detail'] = page_obj
    return render(request, 'dashboard/faq.html',dict_con)

@login_required(login_url='/accounts/login/')
def faq_rank_update(request):
    dict_con = {}
    if request.method == "POST" and request.is_ajax():
        # print("@@@@@@@@@@@@ @@@@@@@@@@@@@@@@@")
        ID_rank = str(request.POST.get('rankId'))
        # print("@@@@@@@@@@@@  ID_rank @@@@@@@@@@@@@@@@@")
        faq_detail = FAQ.objects.get(pk=ID_rank)
        old_rank = faq_detail.rank
        faq_detail.rank=old_rank+1
        faq_detail.save()
    return JsonResponse(dict_con)

def faq_Create(request):
    dict_con = {}
    faq_detail = FAQ.objects.all()
    nodes_module_data_detail = NodesModule.objects.all()
    dict_con['nodes_module_data_detail'] = nodes_module_data_detail
    upload_img = ""
    audio = ""
    video = ""
    doc = ""

    if request.method == 'POST' :
        print("###########",request.POST)
        # if request.FILES['faqimage'] or request.FILES['audio'] or request.FILES['video'] or request.FILES['doc']:
        question = request.POST['question']
        answer = request.POST['answer']
        link = request.POST.getlist('links')
        # print("link",json.dumps(link))
        nodes = {}
        try:
            if request.POST['node_id']:
                node_id = request.POST['node_id']

                node_data = NodesModule.objects.get(pk=node_id)
                idd = node_data.parental_node_id
                for level in range(node_data.node_level):
                    if id != 0:
                      node_data2 = NodesModule.objects.get(pk=idd)
                      nodes[node_data2.node_name] = node_data2.node_value
                      idd = node_data2.parental_node_id

                nodes = dict(reversed(list( nodes.items())))
                # nodes = dict(zip(action_ids, action_names)
        except Exception as node_ex:
            print("Exception in Node Post in FAQ", node_ex)
            dict_con['msg'] = "There is no Node data select Uploading Node .. ! "

        try:
                # import ipdb
                # ipdb.set_trace()
                if request.FILES['faqimage']:
                    upload_img = request.FILES['faqimage']
                    upload_img = upload_img.name
                else:
                    upload_img = ""
                if request.FILES['video']:
                   video = request.FILES['video']
                   video = video.name
                else:
                    video = ""
                if request.FILES['doc']:
                    doc = request.FILES['doc']
                    doc = doc.name
                else:
                    doc = ""
                if request.FILES['audio']:
                    audio = request.FILES['audio']
                    audio = audio.name
                else:
                    audio = ""
                fsi = FileSystemStorage(location= path+'/images')
                fsa = FileSystemStorage(location= path+'/audio')
                fsv = FileSystemStorage(location= path+'/video')
                fsd = FileSystemStorage(location= path+'/doc')
                # print("FAQ image Path " , fsi)
                filenamei = fsi.save(upload_img.name, upload_img)
                filenamea = fsa.save(audio.name, audio)
                filenamev = fsv.save(video.name, video)
                filenamed = fsd.save(doc.name, doc)
                uploaded_file_urli = fsi.url(filenamei)
                uploaded_file_urla = fsa.url(filenamea)
                uploaded_file_urlv = fsv.url(filenamev)
                uploaded_file_urld = fsd.url(filenamed)
        except Exception as e:
                print("Exception is in FAQ Data Uploading",e)
                dict_con['msg'] = "Exception is in FAQ Data Uploading .. ! "


        if len(faq_detail)==0:
                idss = 1
        else:
                idss =max(i.id for i in faq_detail)+1

        a = FAQ.objects.create(id=idss, question=question , answer=answer, audio=audio,
                                   video=video,image=upload_img, doc=doc ,
                               link=str(json.dumps(link)),nodes=str(json.dumps(nodes)))
        a.save()
    faq_detail = FAQ.objects.all()
    dict_con['faq_detail'] = faq_detail
    return  HttpResponseRedirect("/dashboard/faq/")


def faq_delete(request, id):
    dict_con = {}
    if len(FAQ.objects.all()) == 1:
        dict_con['last_one_data_error'] = "Sorry you can't Delete last Record. Becouse one data is mandatory"
    else:
        a = FAQ.objects.filter(id=id).delete()
        dict_con['a'] = a
    a = FAQ.objects.filter(id=id).delete()
    dict_con['a'] = a
    faq_detail = FAQ.objects.all()
    dict_con['faq_detail'] = faq_detail
    nodes_module_data_detail = NodesModule.objects.all()
    dict_con['nodes_module_data_detail'] = nodes_module_data_detail
    return  HttpResponseRedirect("/dashboard/faq/")


def faq_edit_pre(request, id):
    dict_con = {}
    faq_edit_detail = FAQ.objects.get(id=id)
    dict_con['faq_edit_detail'] = faq_edit_detail
    return render(request, 'dashboard/faq.html', dict_con)



def faq_edit(request):
    dict_con = {}
    faq_detail = FAQ.objects.all()
    dict_con['faq_detail'] = faq_detail
    nodes_module_data_detail = NodesModule.objects.all()
    dict_con['nodes_module_data_detail'] = nodes_module_data_detail
    # print(request)
    upload_img = ""
    audio = ""
    video = ""
    doc = ""

    if request.method == 'POST' :
        # if request.FILES['faqimage'] or request.FILES['audio'] or request.FILES['video'] or request.FILES['doc']:
            ids = request.POST['idss']
            question = request.POST['question']
            answer = request.POST['answer']
            link = request.POST['link']
            nodes = request.POST['nodes']
            try:

                upload_img = request.FILES['faqimage']
                audio = request.FILES['audio']
                video = request.FILES['video']
                doc = request.FILES['doc']

                fsi = FileSystemStorage(location= path+'/images')
                fsa = FileSystemStorage(location= path+'/audio')
                fsv = FileSystemStorage(location= path+'/video')
                fsd = FileSystemStorage(location= path+'/doc')
                filenamei = fsi.save(upload_img.name, upload_img)
                filenamea = fsa.save(audio.name, audio)
                filenamev = fsv.save(video.name, video)
                filenamed = fsd.save(doc.name, doc)
                uploaded_file_urli = fsi.url(filenamei)
                uploaded_file_urla = fsa.url(filenamea)
                uploaded_file_urlv = fsv.url(filenamev)
                uploaded_file_urld = fsd.url(filenamed)

                # print(uploaded_file_urli)
            except Exception as e:
                    print("FAQ EDIT Exception",e)
            if upload_img:
                upload_img = upload_img.name
            else:
                upload_img = ""

            if audio:
                audio = audio.name
            else:
                audio = ""

            if video:
                video = video.name
            else:
                video = ""

            if doc:
                doc = doc.name
            else:
                doc = ""

            edit_faq =FAQ.objects.get(id=ids)
            edit_faq.question = question
            edit_faq.answer = answer
            edit_faq.audio = audio
            edit_faq.video = video
            edit_faq.image = upload_img
            edit_faq.doc = doc
            edit_faq.link = link
            edit_faq.nodes = str(nodes)
            edit_faq.save()
    return  HttpResponseRedirect("/dashboard/faq/")



@login_required(login_url='/accounts/login/')
def xlsxfile_upload(request):
    dict_con = {}

    try:
        if request.method == 'POST':
            xlsxfile = request.FILES['xlsxfile']
            # with open(os.path.join(file_json,"hierarchy _query.json")) as datafile:
            #     Json_data = json.load(datafile)
                # Json_data =list(Json_data)
            # if not Json_data:
            Json_data = []
            dfs = pd.read_excel(xlsxfile)
            all_data_dict_xlsx = dfs.to_dict('index')
            old_data_length = len(Json_data)
            # print(dfs.to_dict('index')[0]["question"])
            # import ipdb; ipdb.set_trace()
            for k, v in all_data_dict_xlsx.items():
                if v["question"] and v["answer"] :
                    question=v["question"]
                    answer=v["answer"]
                    link=str([v["link"]])
                    faq_detail = FAQ.objects.all()
                    if len(faq_detail) == 0:
                        idss = 1
                    else:
                        idss = max(i.id for i in faq_detail) + 1

                    case_data = {}
                    print(Json_data)
                    if not Json_data:
                            Json_data = []

                    for k1, v1 in v.items():
                        if k1 not in ("question","answer","link"):
                            case_data[k1]=v1


                    # case_data["pk"]=idss
                    Json_data.append(case_data)
                    a = FAQ.objects.create(id=idss, question=question, answer=answer, link=link, nodes=str(case_data))
                    a.save()
                    # if len(old_data_length) < len(Json_data):
                    # with open(os.path.join(file_json, "hierarchy_query.json"), "w") as f:
                    #         json.dump(Json_data, f, indent=4)
                    dict_con['msg'] = "Data is successfully uploaded .."
                else:
                    dict_con['msg'] = "question and answer can't be empty.. !"
                    render(request, 'dashboard/faq.html', dict_con)

    except Exception as e:
        print("Exception is in FAQ XLSX Uploading : ", str(e))
        dict_con['msg'] = "Exception is in FAQ XLSX Uploading .. ! "
    # faq_detail = FAQ.objects.filter(create_by=request.user)
    faq_detail = FAQ.objects.all()
    dict_con['faq_detail'] = faq_detail
    return  HttpResponseRedirect("/dashboard/faq/")


@login_required(login_url='/accounts/login/')
def node_index(request):
    dict_con = {}
    nodes_module_data_detail = NodesModule.objects.all()
    dict_con['nodes_module_data_detail'] = nodes_module_data_detail
    faq_detail = FAQ.objects.all()
    dict_con['faq_detail'] = faq_detail
    return render(request, 'dashboard/faq.html', dict_con)

@login_required(login_url='/accounts/login/')
def node_create(request):
    dict_con = {}
    try:
        nodes_module_data_detail = NodesModule.objects.all()
        # parental_node_data_detail = ParentalNode.objects.all()
        if request.method == 'POST':
            print(request.POST)
            node_name = request.POST['node_name']
            node_value = request.POST['node_value']
            node_level = request.POST['node_level']
            if request.POST['parental_node_id']:
                parental_node_id = request.POST['parental_node_id']

            if len(nodes_module_data_detail) == 0:
                idss = 1

            else:
                idss = max(i.id for i in nodes_module_data_detail) + 1


            a = NodesModule.objects.create(id=idss, node_name=node_name, node_value=node_value, node_level=node_level,
                                           parental_node_id=parental_node_id)
            a.save()
    except Exception as e:
        print("Exception in Node creating :",str(e))


    faq_detail = FAQ.objects.all()
    dict_con['faq_detail'] = faq_detail
    # return render(request, 'dashboard/faq.html', dict_con)
    return HttpResponseRedirect("/dashboard/faq/")


@login_required(login_url='/accounts/login/')
def node_delete(request):
    dict_con = {}
    if request.method == "POST" and request.is_ajax():
        id = int(request.POST.get('id'))
        try:
            childNodes = NodesModule.objects.filter(parental_node_id=id)
            if len(childNodes) == 0:
                NodesModule.objects.get(id=id).delete()
                dict_con['msg'] = "The node is successfully delete !"
            else:
                dict_con['msg'] = "You can't delete this node because it has child nodes ! "
        except Exception as e:
            print("Exception in node delete", e)
            dict_con['msg'] = "You can't delete this node because it not exist ! "
    # faq_detail = FAQ.objects.all()
    # dict_con['faq_detail'] = faq_detail
    # dict_con['username'] = request.user
    parental_node_data_detail = NodesModule.objects.all()
    post_list = serializers.serialize('json', parental_node_data_detail)
    dict_con['parental_node_data_detail'] = post_list
    # dict_con['parental_node_data_detail_json'] = post_list
    return JsonResponse(dict_con)

@login_required(login_url='/accounts/login/')
def node_edit(request):
    dict_con = {}
    if request.method == "POST" :
        id = int(request.POST['id'])
        node_name = request.POST['node_name']
        node_value = request.POST['node_value']
        try:
            Node = NodesModule.objects.get(id=id)
            if Node:
                Node.node_name = node_name
                Node.node_value = node_value
                Node.save()
                dict_con['msg'] = "The node is successfully Edit !"

        except Exception as e:
            print("Exception in node Edit",e)
            dict_con['msg'] = "You can't Edit this node because it not exist ! "
    faq_detail = FAQ.objects.all()
    dict_con['username'] = request.user
    parental_node_data_detail = NodesModule.objects.all()
    post_list = serializers.serialize('json', parental_node_data_detail)
    dict_con['parental_node_data_detail'] = post_list
    dict_con['parental_node_data_detail_json'] = post_list
    paginator = Paginator(faq_detail, 4)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    dict_con['faq_detail'] = page_obj
    return render(request, 'dashboard/faq.html', dict_con)



###################################################  recommunded_data  ########################################################

@login_required(login_url='/accounts/login/')
def recommunded_data_view(request):
    dict_con = {}
    recommunded_data_detail = recommunded_data.objects.all()
    dict_con['recommunded_data_detail'] = recommunded_data_detail
    TaskToEntity_detail = TaskToEntity.objects.all()
    dict_con['TaskToEntity_detail'] = TaskToEntity_detail
    intenttotask_detail = IntentToTask.objects.all()
    dict_con['intenttotask_detail'] = intenttotask_detail
    return render(request, 'dashboard/recommunded_data.html', dict_con)

@login_required(login_url='/accounts/login/')
def recommunded_data_create(request):
    # import ipdb
    # ipdb.set_trace()
    dict_con = {}
    if request.method == 'POST':
        entity_id = request.POST['entity_id']
        task_id = request.POST['task_id']
        title = request.POST['title']
        task = request.POST['task']
        link = request.POST['link']
        utterance = request.POST['utterance']
        if len(recommunded_data.objects.all()) == 0:
            idss = 1
        else:
            idss = max(i.id for i in recommunded_data.objects.all()) + 1
        a = recommunded_data.objects.create(id=idss, entity_id=entity_id, title=title.strip(), task_id=task_id.strip(),
                                            task=task.strip(), link=link.strip(), utterance=utterance.strip())
        a.save()
    recommunded_data_detail = recommunded_data.objects.all()
    dict_con['recommunded_data_detail'] = recommunded_data_detail
    entity_detail = Entity.objects.all()
    dict_con['entity_detail'] = entity_detail
    recommunded_data_detail = recommunded_data.objects.all()
    dict_con['recommunded_data_detail'] = recommunded_data_detail
    TaskToEntity_detail = TaskToEntity.objects.all()
    dict_con['TaskToEntity_detail'] = TaskToEntity_detail
    intenttotask_detail = IntentToTask.objects.all()
    dict_con['intenttotask_detail'] = intenttotask_detail
    # return render(request, 'dashboard/recommunded_data.html', dict_con
    return HttpResponseRedirect("/dashboard/recommundedview/")

@login_required(login_url='/accounts/login/')
def recommunded_data_edit(request, id):
    dict_con = {}
    recommunded_data_edit = recommunded_data.objects.get(id=id)
    dict_con['recommunded_data_edit'] = recommunded_data_edit

    entity_detail = Entity.objects.all()
    recommunded_data_detail = recommunded_data.objects.all()
    TaskToEntity_detail = TaskToEntity.objects.all()
    intenttotask_detail = IntentToTask.objects.all()
    dict_con['TaskToEntity_detail'] = TaskToEntity_detail
    dict_con['intenttotask_detail'] = intenttotask_detail
    dict_con['entity_detail'] = entity_detail
    dict_con['recommunded_data_detail'] = recommunded_data_detail
    # return render(request, 'dashboard/recommunded_data.html', dict_con)
    return HttpResponseRedirect("/dashboard/recommundedview/")


@login_required(login_url='/accounts/login/')
def recommunded_data_delete(request, id):
    dict_con = {}
    recommunded_data.objects.get(id=id).delete()
    recommunded_data_detail = recommunded_data.objects.all()
    dict_con['recommunded_data_detail'] = recommunded_data_detail
    TaskToEntity_detail = TaskToEntity.objects.all()
    dict_con['TaskToEntity_detail'] = TaskToEntity_detail
    intenttotask_detail = IntentToTask.objects.all()
    dict_con['intenttotask_detail'] = intenttotask_detail
    # return render(request, 'dashboard/recommunded_data.html', dict_con)
    return HttpResponseRedirect("/dashboard/recommundedview/")

@login_required(login_url='/accounts/login/')
def recommunded_data_edit1(request):
    dict_con = {}
    if request.method == 'POST':
        eid = request.POST['eid']
        entity_id = request.POST['entity_id']
        task_id = request.POST['task_id']
        title = request.POST['title']
        task = request.POST['task']
        link = request.POST['link']
        utterance = request.POST['utterance']
        recommunded_data.objects.get(id=eid).update(entity_id=entity_id, title=title.strip(), task_id=task_id,
                                                    task=task.strip(), link=link.strip(), utterance=utterance.strip())

    entity_detail = Entity.objects.all()
    dict_con['entity_detail'] = entity_detail
    recommunded_data_detail = recommunded_data.objects.all()
    dict_con['recommunded_data_detail'] = recommunded_data_detail
    TaskToEntity_detail = TaskToEntity.objects.all()
    dict_con['TaskToEntity_detail'] = TaskToEntity_detail
    intenttotask_detail = IntentToTask.objects.all()
    dict_con['intenttotask_detail'] = intenttotask_detail
    # return render(request, 'dashboard/recommunded_data.html', dict_con)
    return HttpResponseRedirect("/dashboard/recommundedview/")

###################################################  Chat History  ########################################################

@login_required(login_url='/accounts/login/')
def chat_history(request):
    dict_con = {}
    chat_history_detail = ChatHistory.objects.all()[::-1]
    # dict_con['chat_history_detail'] = chat_history_detail[::-1]
    paginator = Paginator(chat_history_detail, 2)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    dict_con['chat_history_detail'] = page_obj
    return render(request, 'dashboard/chat_history.html', dict_con)