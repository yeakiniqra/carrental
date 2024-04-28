from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')
def ownersignup(request):
    if request.method == 'POST':
       
        username = request.POST.get('username')
        contact_no = request.POST.get('contact_no')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        
        if username and contact_no and email and password:
           
            new_owner = Owner(
                username=username,
                contact_no=contact_no,
                email=email,
                password=password
            )
            
            new_owner.save()
            
            
            request.session['owner_username'] = username
            request.session['owner_contact_no'] = contact_no
            request.session['owner_email'] = email
            request.session['owner_password'] = password
            
            
            return redirect('ownerlogin')  
        else:
            messages.error(request, 'All fields are required.')
            return redirect('ownersignup')  
    return render(request, 'ownersignup.html')
    
def owner_profile(request):
    owner_username = request.session.get('owner_username')
    owner_contact_no = request.session.get('owner_contact_no')
    owner_email = request.session.get('owner_email')
    owner_password = request.session.get('owner_password')
    
    if owner_username and owner_contact_no and owner_email:
        context = {
            'owner_username': owner_username,
            'owner_contact_no': owner_contact_no,
            'owner_email': owner_email,
            'owner_password': owner_password 
        }
        return render(request, 'ownerprofile.html', context)
    else:
        
        return HttpResponse('Please Log in first.')