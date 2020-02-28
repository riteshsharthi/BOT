from django.db import models
from mongoengine import Document, fields
# Create your models here.
class Entity(Document):
    id = fields.IntField(primary_key=True)
    Entity_Type = fields.StringField(required=True)
    Entity_Name = fields.StringField(required=True)
    Entity_Regex =fields.StringField(required=True)

    def __str__(self):
        return "{0}, {1}, {2}".format(self.Entity_Name ,self.Entity_Regex, self.Entity_Type)

class IntentToTask(Document):
    id = fields.IntField(primary_key=True)
    Intent_Name = fields.StringField(required=True)
    Task_Name = fields.StringField(required=True)
    Action_Url = fields.StringField(required=True)
    def __str__(self):
        return self.Intent_Name

class TaskToEntity(Document):
    id = fields.IntField(primary_key=True)
    Task_Id = fields.IntField(required=True)
    Entity_Id = fields.IntField(required=True)
    Entity_Name = fields.StringField(required=True)
    Entity_Question = fields.StringField(required=True)
    Entity_alternet_qustion= fields.ListField(required=False)
    Entity_Sequence = fields.IntField(required=True)
    task_redirect = fields.StringField(required=False)
    Session_key = fields.StringField(required=False)
    Datetime_chat = fields.StringField(required=False)
    user_chat = fields.StringField(required=False)

    def __unicode__(self):
        return self.Entity_Question

    class Meta:
        app_label = "model"
        db_table = "FAQ_TaskToEntity"
        ordering = ('created',)

class ExtractedUserData(Document):
    id = fields.IntField(primary_key=True)
    Task_Id = fields.IntField(required=True)
    Entity_Id = fields.IntField(required=True)
    Entity_Name = fields.StringField(required=True)
    Entity_Question = fields.StringField(required=True)
    Entity_Sequence = fields.IntField(required=True)
    Entity_Value = fields.StringField(required=False)
    Session_key = fields.StringField(required=False)
    Datetime_chat = fields.StringField(required=False)
    user_chat = fields.StringField(required=False)


    def __unicode__(self):
        return self.Entity_Question
class TaskToEntityUser(Document):
    id = fields.IntField(primary_key=True)
    Task_Id = fields.IntField(required=True)
    Entity_Id = fields.IntField(required=True)
    Entity_Name = fields.StringField(required=True)
    Entity_Question = fields.StringField(required=True)
    Entity_alternet_qustion= fields.ListField(required=False)
    Entity_Sequence = fields.IntField(required=True)
    Entity_Value = fields.StringField(required=False)
    Session_key = fields.StringField(required=False)
    Datetime_chat = fields.StringField(required=False)
    user_chat = fields.StringField(required=False)
    ssid = fields.IntField(required=False)

    def __unicode__(self):
        return self.Entity_Question

    class Meta:
        app_label = "model"
        db_table = "FAQ_TaskToEntity"
        ordering = ('created',)

class ConveUser(Document):
    id = fields.IntField(primary_key=True)
    Bot_Responce = fields.StringField(required=False)
    User_Request = fields.StringField(required=False)
    Session_key = fields.StringField(required=False)
    Sequence = fields.StringField(required=False)
    Datetime_Chat = fields.StringField(required=False)
    User_Id = fields.StringField(required=False)
    user_chat = fields.StringField(required=False)


    def __str__(self):
        return self.Bot_Responce

class FAQ(Document):
    id = fields.IntField(primary_key=True)
    question = fields.StringField(required=False)
    answer = fields.StringField(required=False)
    audio = fields.StringField(required=False)
    video = fields.StringField(required=False)
    image = fields.StringField(required=False)
    doc = fields.StringField(required=False)

    def __str__(self):
        return self.question

class ResultMap(Document):
    id = fields.IntField(primary_key=True)
    taskId = fields.IntField(required=True)
    entityId = fields.IntField(required=True)
    keyof = fields.StringField(required=True)
    redirectTo = fields.StringField(required=True)
    def __str__(self):
        return self.redirectTo