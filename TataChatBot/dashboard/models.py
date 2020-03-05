# from django.db import models
from djongo import models
from django.contrib.auth.models import User

# Create your models here.
class Entity(models.Model):
    id = models.IntegerField(primary_key=True, db_column='_id')
    Entity_Type = models.CharField(max_length=100, default="")
    Entity_Name = models.CharField(max_length=100, default="")
    Entity_Regex =models.CharField(max_length=100, default="")

    objects = models.DjongoManager()

    def __str__(self):
        return "{0}, {1}, {2}".format(self.Entity_Name ,self.Entity_Regex, self.Entity_Type)

class IntentToTask(models.Model):
    id = models.IntegerField(primary_key=True, db_column='_id')
    Intent_Name = models.CharField(max_length=100, default="")
    Task_Name = models.CharField(max_length=100, default="")
    Action_Url = models.CharField(max_length=100, default="")
    post_action = models.CharField(max_length=100, default="")
    objects = models.DjongoManager()
    def __str__(self):
        return self.Intent_Name

class TaskToEntity(models.Model):
    id = models.IntegerField(primary_key=True, db_column='_id')
    Task_Id = models.IntegerField(default=0)
    Entity_Id = models.IntegerField(default=0)
    Entity_Name = models.CharField(max_length=100, default="")
    Entity_Question = models.CharField(max_length=250, default="")
    # Entity_alternet_qustion= models.ListField(max_length=300, default="")
    Entity_Sequence = models.IntegerField(default=0)
    task_redirect = models.CharField(max_length=100, default="")
    link = models.CharField(max_length=300, default="")
    pre_text = models.CharField(max_length=100, default="")
    pre_action_url = models.CharField(max_length=100, default="")
    # interview_url = models.CharField(max_length=100, default="")
    # value_collection_name = models.CharField(max_length=100, default="")
    # collection_url = models.CharField(max_length=100, default="")
    # validation_url = models.CharField(max_length=100, default="")
    objects = models.DjongoManager()
    def __str__(self):
        return self.Entity_Question

# class ParentalNode(models.Model):
#     node_name = models.CharField(max_length=70, default="")
#     node_value = models.CharField(max_length=70, default="")
#     node_level = models.IntegerField(default=1)
#     objects = models.DjongoManager()
#
#     def __str__(self):
#         return "Node Level "+str(self.node_level) + "  >>  " + str(self.node_name) + " ( " + str(self.node_value) + " ) "
#

class NodesModule(models.Model):
    id = models.IntegerField(primary_key=True, db_column='_id')
    node_name = models.CharField(max_length=70, default="")
    node_value = models.CharField(max_length=70, default="")
    node_level = models.IntegerField(default=1)
    parental_node_id = models.IntegerField(default=0)
    # parental_node_value = models.CharField(max_length=70, default="", blank=True)
    # parental_node_level = models.IntegerField(default=0)
    objects = models.DjongoManager()

    def __str__(self):
        return "Node Level "+str(self.node_level) + "  >>  " + str(self.node_name) + " ( " + str(self.node_value) + " ) "

class FAQ(models.Model):
    id = models.IntegerField(primary_key=True, db_column='_id')
    question = models.CharField(max_length=250, default="")
    answer = models.CharField(max_length=400, default="")
    audio = models.CharField(max_length=100, default="")
    video = models.CharField(max_length=100, default="")
    image = models.CharField(max_length=300, default="")
    doc = models.CharField(max_length=300, default="")
    rank =models.IntegerField(default=0)
    link = models.CharField(max_length=500, default="")
    nodes = models.CharField(max_length=500, default="")
    user_type = models.CharField(max_length=20, default="")
    create_by =models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    use_count=models.IntegerField(default=0)
    create_dt = models.DateTimeField(auto_now_add=True)
    objects = models.DjongoManager()
    def __str__(self):
        return self.question

class ResultMap(models.Model):
    id = models.IntegerField(primary_key=True, db_column='_id' )
    taskId = models.IntegerField(default=0)
    entityId = models.IntegerField(default=0)
    keyof = models.CharField(max_length=100, default="")
    redirectTo = models.CharField(max_length=100, default="")
    objects = models.DjongoManager()
    def __str__(self):
        return self.redirectTo

class recommunded_data(models.Model):
   id = models.IntegerField(primary_key=True, db_column='_id')
   entity_id = models.CharField(max_length=100, default="")
   task_id = models.CharField(max_length=100, default="")
   title = models.CharField(max_length=100, default="")
   task =models.CharField(max_length=100, default="")
   link = models.CharField(max_length=100, default="")
   utterance = models.CharField(max_length=100, default="")
   objects = models.DjongoManager()
   def __str__(self):
       return self.title

class ChatHistory(models.Model):
    id = models.IntegerField(primary_key=True, db_column='_id')
    request_data= models.CharField(max_length=300, default="")
    responce_data = models.CharField(max_length=500, default="")
    task_name = models.CharField(max_length=20, default="")
    task_type = models.CharField(max_length=20, default="")
    request_user=models.CharField(max_length=50, default="")
    responce_user = models.CharField(max_length=50, default="")
    create_dt=models.DateTimeField(auto_now_add=True)