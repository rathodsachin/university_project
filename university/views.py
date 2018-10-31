from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import SignUpForm

# Create your views here.




def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():            
            # u = User.objects.create_user(                                                                                    
            #             username = request.POST['user_name'],
            #             password = request.POST['password1'],
            #     )
            # u.save()
            
            form.save()
            username = form.cleaned_data.get('user_name')            
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


