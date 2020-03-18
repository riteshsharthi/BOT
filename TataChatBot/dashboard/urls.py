from django.urls import path
from . import views


urlpatterns = [
    ################################ entity ###############################
    path('entity/', views.Entity_Details, name='entity'),
    path('entitycreate/', views.Entity_Create, name='entityCreate'),
    path('entitydelete/<int:id>/', views.Entity_delete, name='entitydelete'),
    path('entityedit/<int:id>/', views.Entity_edit, name='entityedit'),
    path('entityedit1/', views.Entity_edit1, name='entityedit1'),

    ################################ IntentToTask ###############################
    path('intenttotask/', views.IntentToTask_Details, name='intenttotask'),
    path('intenttotaskcreate/', views.IntentToTask_Create, name='intenttotaskCreate'),
    path('intenttotaskdelete/<int:id>/', views.IntentToTask_delete, name='intenttotaskdelete'),
    path('intenttotaskedit/<int:id>/', views.IntentToTask_edit, name='intenttotaskedit'),
    path('intenttotaskedit1/', views.IntentToTask_edit1, name='intenttotaskedit1'),

    ################################ TaskToEntity ###############################
    path('tasktoentity/', views.TaskToEntity_Details, name='tasktoentity'),
    path('tasktoentitycreate/', views.TaskToEntity_Create, name='tasktoentityCreate'),
    path('tasktoentitydelete/<int:id>/', views.TaskToEntity_delete, name='tasktoentitydelete'),
    path('tasktoentityedit/<int:id>/', views.TaskToEntity_edit, name='tasktoentityedit'),
    path('tasktoentityedit1/', views.TaskToEntity_edit1, name='tasktoentityedit1'),

    ################################  FAQ Data ###############################
    path('faq/', views.faq_data, name='faq_data'),
    path('faqCreate/', views.faq_Create, name='faq_Create'),
    path('faqDelete/<int:id>/', views.faq_delete, name='faq_delete'),
    path('faq_pre/<int:id>', views.faq_edit_pre, name='faq_edit_pre'),
    path('faq_edit/', views.faq_edit, name='faq_edit'),

    path('node_index/', views.node_index, name='node_index'),
    path('node_create/', views.node_create, name='node_create'),
    path('node_delete/', views.node_delete, name='node_delete'),
    path('node_edit/', views.node_edit, name='node_edit'),

    path('faq_rank/', views.faq_rank_update, name='faq_rank_update'),

    path('xlsxfileUpload/', views.xlsxfile_upload, name='xlsxfileUpload'),

    ################################ Result Map ###############################
    path('resultmap/', views.result_map, name='result_map'),
    path('resultmapcreate/', views.result_map_create, name='result_map_create'),
    path('resultmapupdate/<int:id>/', views.result_map_update, name='result_map_update'),
    path('resultmapdelete/<int:id>/', views.result_map_delete, name='result_map_delete'),
    path('resultmapupdate1/',views.result_map_update1, name='result_map_update1'),

    ################################ Recommended ###############################
    path('recommundedview/', views.recommunded_data_view, name='recommundedview'),
    path('recommundedcreate/', views.recommunded_data_create, name='recommundedcreate'),
    path('recommundededit1/', views.recommunded_data_edit1, name='recommundededit1'),
    path('recommundeddelete/<int:id>/', views.recommunded_data_delete, name='recommundeddelete'),
    path('recommundededit/<int:id>/', views.recommunded_data_edit, name='recommundededit'),

    ################################ Chat History ###############################
    path('chathistory/', views.chat_history, name='chathistory'),


]
