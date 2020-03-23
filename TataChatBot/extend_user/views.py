from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Profile

# Create your views here.
def index(request):
    print(request.user.username)
    con_dict = {}
    user_data = Profile.objects.filter(user=request.user)
    print( Profile.objects.filter(user=request.user))
    con_dict['user_data'] = user_data
    return  render(request, 'extend_user/users.html', con_dict)

# def user_edit(request, id):
#
#     return HttpResponseRedirect('extend_user/index')