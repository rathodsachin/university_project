from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import Students
from .models import Institute
from .models import Branch
from .models import Fee
# Create your views here.




def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():          
            instname=form.cleaned_data.get('Institute')
            brchname=form.cleaned_data.get('Branch')
            
            import pdb;pdb.set_trace()
            inst=Institute.objects.get(name="Nirma University")
            print("Helollllollolol")
            id = inst.id
            inst.save()
            brch=Branch.objects.get_or_create(name="Institute of technology")
            brch.save()

            
            
            username = form.cleaned_data.get('user_name')            
            raw_password = form.cleaned_data.get('password1')

            user = User.objects.create_user(                                                                                    
                    username = request.POST['user_name'],
                    password = request.POST['password1'],
                )
            
            
            s=Students(
                    userName=user,
                    user_name=request.POST['user_name'],
                    password = request.POST['password1'],
                    first_name = request.POST['first_name'],
                    last_name = request.POST['last_name'],
                    phone = request.POST['phone'],
                    dob = request.POST['dob'],
                    enrollment_number = request.POST['enrollment_number'],
                    branch = brch,
                    institute = inst,
                    course = request.POST['course'],
                )
            print(s)
            user.save()
            s.save()



            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


