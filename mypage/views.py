from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'mypage/home.html')


def contact(request):
    return render(request, 'mypage/basic.html',  {'content': ['Slik skriver du til meg','andbre@stud.ntnu.no']})