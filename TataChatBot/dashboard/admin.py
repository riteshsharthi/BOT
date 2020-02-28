
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Entity)
admin.site.register(IntentToTask)
admin.site.register(TaskToEntity)
admin.site.register(ResultMap)
admin.site.register(FAQ)
admin.site.register(ChatHistory)
admin.site.register(NodesModule)
# admin.site.register(ParentalNode)