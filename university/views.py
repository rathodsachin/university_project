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
from .models import PaytmHistory

from django.http import HttpResponse
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from . import Checksum

from weasyprint import HTML, CSS
from django.template.loader import get_template
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import RequestContext






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

def payfees(request):
    if request.user.is_authenticated:        
        user_id=request.user.id
        students = Students.objects.get(userName_id=user_id) 
        fee= Fee.objects.filter(branch_id=students.branch.id)
        context = {'fee': fee}
        #json_data= {'fees': {b.fee_type: b.amount for b in fee}}   
        #import pdb;pdb.set_trace()
        #print(json_data)
        

    return render(request, 'payfees.html',context)

def payment(request):
    print(request.POST['fee_total'])
    MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
    MERCHANT_ID = settings.PAYTM_MERCHANT_ID    
    CALLBACK_URL = "http://localhost:8000/university/response/"
    website = "WEBSTAGING"
    # Generating unique temporary ids
    order_id = Checksum.__id_generator__()      
    import pdb;pdb.set_trace()
    bill_amount = 100
    if bill_amount:
        data_dict = {
                    'MID':MERCHANT_ID,
                    'ORDER_ID':order_id,
                    'TXN_AMOUNT': request.POST['fee_total'],
                    'CUST_ID':'harish@pickrr.com',
                    'INDUSTRY_TYPE_ID':'Retail',
                    'WEBSITE': website,
                    'CHANNEL_ID':'WEB',
                    'CALLBACK_URL':CALLBACK_URL,                                        
                }
        param_dict = data_dict
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, MERCHANT_KEY)    
        print(param_dict)
        return render(request,"payment.html",{'paytmdict':param_dict})
    return HttpResponse("Bill Amount Could not find. ?bill_amount=10")


@csrf_exempt
def response(request):
    if request.method == "POST":
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        data_dict = {}
        for key in request.POST:
            data_dict[key] = request.POST[key]
        verify = Checksum.verify_checksum(data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        if verify:
            PaytmHistory.objects.create(user=request.user, **data_dict)
            user_id=request.user.id
            students = Students.objects.get(userName_id=user_id)        
            data_dict.update({                    
                    'firstname':request.user.first_name,
                    'lastname':request.user.last_name,
                    'phone':students.phone,
                    'enrollment_number' : students.enrollment_number,                    
                    'institute' : students.institute,                    
                    'branch' : students.branch,
                })            
            return render(request,"response.html",{"paytm":data_dict})
        else:
            return HttpResponse("checksum verify failed")
    return HttpResponse(status=200)

def invoice(request):    
    user_id=request.user.id
    students = Students.objects.get(userName_id=user_id)
    data_dict = {}
    for key in request.POST:
        data_dict[key] = request.POST[key]    
    data_dict = {                    
                    'firstname':request.user.first_name,
                    'lastname':request.user.last_name,
                    'phone':students.phone,
                    'enrollment_number' : students.enrollment_number,                    
                    'institute' : students.institute,                    
                    'branch' : students.branch,
                    'ORDERID' : 'hhvAdy',
                    'TXNAMOUNT' : '100.00',     
                    'TXNID' : '70001158737', 
                    'STATUS' : 'TXN_SUCCESS', 
                    'TXNDATE' : '2018-11-28 13:03:28.0',
                    'GATEWAYNAME' : 'WALLET',
                }            
    return render(request,"invoice.html",{"paytm":data_dict})


def pdf_generation(request):
    user_id=request.user.id    
    paytmobj = PaytmHistory.objects.last()
    students = Students.objects.get(userName_id=user_id)
    data_dict = {                    
                    'firstname':request.user.first_name,
                    'lastname':request.user.last_name,
                    'phone':students.phone,
                    'enrollment_number' : students.enrollment_number,                    
                    'institute' : students.institute,                    
                    'branch' : students.branch,
                    'ORDERID' : paytmobj.ORDERID,
                    'TXNAMOUNT' : paytmobj.TXNAMOUNT,     
                    'TXNID' : paytmobj.TXNID, 
                    'STATUS' : paytmobj.STATUS, 
                    'TXNDATE' : paytmobj.TXNDATE,
                    'GATEWAYNAME' : paytmobj.GATEWAYNAME,
                }  

    html_string = render_to_string('response.html', {'paytm': data_dict}).encode(encoding="UTF-8")
    html = HTML(string=html_string,encoding='utf-8')
    result = html.write_pdf()

    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Fee_Receipt.pdf"'
    return response