from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.conf import settings
import cv2
import os
from django.core.mail import EmailMessage
from django.shortcuts import render

# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    return render (request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confirm password are not Same!!")
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            user = User.objects.get(username=username)
            mail=user.email
            capture_image_and_email(mail)
            return render (request,'login.html')
    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

def service(request):
    return render (request,'service.html')

def capture_image_and_email(eml):
        # Open the webcam
    cap = cv2.VideoCapture(0)

    # Read the current frame
    ret, frame = cap.read()

    # Release the webcam
    cap.release()

    # Save the captured image to a file
    image_path = os.path.join(settings.BASE_DIR, 'captured_image.jpg')
    cv2.imwrite(image_path, frame)

    # Compose the email message with the captured image as an attachment
    email = EmailMessage(
        'Captured Image of the intruder',
        'Please see the attached image',
        settings.EMAIL_HOST_USER,
        [eml],
    )
    email.attach_file(image_path)
    email.send()

    # Delete the temporary image file
    os.remove(image_path)

    return None
