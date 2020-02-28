from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    context_dict = { }
    return render(request,'index.html',context_dict)


@login_required
def chat(request):
    context_dict = { }
    return render(request,'chatbot/bot.html',context_dict)