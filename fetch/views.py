from django.shortcuts import render,redirect
from .forms import EmployeeForm
from .models import EmployeeRefer,OTP
from django.contrib.auth.models import User
from django.contrib import messages
from fetchData import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from . tokens import generate_token
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
import random
from django.contrib import messages


# Create your views here.
def auth_login(request):
       if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        print(username)
        print(pass1)
        
        user = authenticate(username=username, password=pass1)
        print(user)
        print("True")
        
        if user is not None:
            print("True")
            fname = user.first_name
            #messages.success(request, "Logged In Sucessfully!!")
            return render(request, "fetch/employee_form.html",{"fname":fname})
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('/fetch/LogIn')
       return render(request,'fetch/login.html')
def home(request):
   return render(request,'fetch/index.html')
def fpass(request):
   if request.method == 'POST':
        email = request.POST['emailid']
        try:
            user = User.objects.get(email =email)
            print(user)
            # Generate OTP for the user
            otp = OTP.generate_otp(user)

            print(otp)
            send_mail(
            "Verification Code For the Password Reset",
            otp ,
            "pallavikurmala@gmail.com",
            [email],
            fail_silently=False,
            )     
            # You can send the OTP to the user via SMS, email, etc.
            # Redirect to success page or show a success message
            return render(request,'fetch/fpass.html')
        except User.DoesNotExist:
            # Handle case when user does not exist
            print("Doesnt Exits")
   return render(request,'fetch/fpass.html')
  

        
   
def lgout(request):
   logout(request)
   messages.success(request, "Logged Out Successfully!!")
   return redirect('/fetch/LogIn/')
def signup(request):
   if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        myuser = User.objects.create_user(username, email, pass1,is_superuser=True,is_staff =True)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.email =email
        myuser.password =pass1
        myuser.save()
        if User.objects.filter(username=username).exists():
            username_unique_error = True

        if User.objects.filter(email=email).exists():
            email_unique_error = True

        else :
            create_new_user = User.objects.create_user(username,pass1,email,is_superuser =True,is_staff=True)
            create_new_user.first_name = fname
            create_new_user.last_name = lname
            create_new_user.email =email
            create_new_user.password =pass1
            create_new_user.save()
            user = authenticate(username=username, password=pass1)
            auth_login(request, user)
            if create_new_user is not None:
                if create_new_user.is_active:
                    print("Registered")
                    return redirect('/fetch/LogIn')
                else:
                    print("The password is valid, but the account has been disabled!")
        
                    return redirect('/fetch/SignUp')
        
   return render(request, "fetch/signup.html")

    
def employee_list(request):
  context = { 'em' : EmployeeRefer.objects.all() }
  return render (request,"fetch/employee_list.html" ,context)

def employee_form(request,id=0):
    if request.method =="GET":
        if id == 0:
            form = EmployeeForm()
        else:
           employee =EmployeeRefer.objects.get(pk=id)
           form = EmployeeForm(instance=employee)
        return  render(request,"fetch/employee_form.html",{'form':form})
    else:
       if id ==0:
          form = EmployeeForm(request.POST)
       else:
          employee =EmployeeRefer.objects.get(pk=id)
          form =EmployeeForm(request.POST,instance =employee)
       if form.is_valid():
          form.save()
       return redirect('/fetch/list')

def employee_delete(request,id):
  employee =EmployeeRefer.objects.get(pk=id)
  employee.delete()

  return redirect ('/fetch/list')


def pupdate(request):
    """
    View function to validate an OTP entered by a user.
    """
    if request.method == 'POST':
        username = request.POST.get('username')

        otp = request.POST.get('otp')
        print(otp)
        try:
            user = User.objects.get(username=username)
            otp_instance = OTP.objects.get(user=user)
            print(otp_instance.otp)
            if otp_instance.otp == otp and otp_instance.is_valid():
                # OTP is valid, perform desired action
                # Redirect to success page or show a success message
                print(user.password)
                new_pass = request.POST.get('pass1')
                user.set_password(new_pass)

                
                print(user.password)
                user.save()

                print("Password Updated")
                messages.success(request, 'Password Successfully Updated')

                return redirect('/fetch/LogIn')
                
            else:
                messages.warning(request, 'Please Enter Correct OTP')
                # OTP is not valid, show error message
                return redirect('/fetch/pupdate')
        except User.DoesNotExist:
            # Handle case when user does not exist
            return render(request, 'error.html', {'error_message': 'User does not exist'})
        except OTP.DoesNotExist:
            # Handle case when OTP does not exist for the user
            return render(request, 'error.html', {'error_message': 'OTP does not exist'})
    return render(request,"fetch/pupdate.html")
def li (request):
    return render(request,"fetch/li.html")



from .models import PDFFile
from .forms import PDFFileForm

def uppdf(request):
    if request.method == 'POST':
        form = PDFFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/fetch/pdfview/') # Redirect to view PDF list
    else:
        form = PDFFileForm()
    return render(request, 'fetch/uppdf.html', {'form': form})

def pdfview(request):
    pdf = PDFFile.objects.all()
    return render(request, 'fetch/pdfview.html', {'pdf': pdf})

