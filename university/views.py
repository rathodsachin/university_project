from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import SignUpForm
from .models import Students
from .models import Institute
from .models import Branch
from .models import Fee



def home(request):
    return render(request, 'home.html')


def signup(request):    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        #import pdb;pdb.set_trace()
        print(form)
        if form.is_valid():          

            instid=request.POST.get('institute')            
            brchid=request.POST.get('branch')            
            
            inst=Institute.objects.get(id=instid)
            brch=Branch.objects.get(id=brchid)
                
            username = form.cleaned_data.get('user_name')            
            raw_password = form.cleaned_data.get('password1')

            user = User.objects.create_user(                                                                                    
                    username = username,
                    password = raw_password,
                    first_name = request.POST['first_name'],
                    last_name = request.POST['last_name'],
                    email = request.POST['email_address']
                )
            user.save()
            print(form)
            s=Students.objects.create(
                    userName=user,
                    user_name=username,
                    password1 = request.POST['password1'],                                        
                    phone = request.POST['phone'],
                    dob = request.POST['dob'],
                    enrollment_number = request.POST['enrollment_number'],
                    course = request.POST['course'],
                    branch = brch,
                    institute = inst,
                    
                )
            print(s)
            
            s.save()



            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def load_branch(request):    
    institute_id = request.GET.get('institute')
    print(institute_id)
    branch = Branch.objects.filter(institute_id=institute_id).order_by('name')
    json_data = {'branch': {b.id: b.name for b in branch}}
    return JsonResponse(json_data)    
