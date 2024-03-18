from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')
def ownersignup(request):
    return render(request, 'ownersignup.html')
def ownerprofile(request):
    return render(request, 'ownerprofile.html')