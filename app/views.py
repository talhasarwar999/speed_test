from django.shortcuts import render,redirect,HttpResponse
from django.core.mail import send_mail, BadHeaderError
from .models import *
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMultiAlternatives, send_mass_mail

# Create your views here.

def index(request):
    return render(request, "app/index.html")


def subscribe(request):
    if request.method == "POST":
        email = request.POST['email']
        content = Subscribe(email=email)
        content.save()
        messages.success(request, "Successfully Subscribed. For details please check your email.")
        try:
            send_mail(f'Thank you for Subscribing', f'Hi,\n\nThank you for subscribing to BT Business Official Partner.\n\nIf you have any questions please feel free to contact us, we are just an email away.\n\nThank You\n\nCustomers Service.\nBT Business Partner UK', email, ['support@marketingservicesonline.co.uk'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        try:
            send_mail(f'Thank you for Subscribing', f'Hi,\n\nThank you for subscribing to BT Business Official Partner.\n\nIf you have any questions please feel free to contact us, we are just an email away.\n\nThank You\n\nCustomers Service.\nBT Business Partner UK', 'support@marketingservicesonline.co.uk', [email])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect('index')
    return render(request, "index.html")


def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        if len(phone) < 10 or len(phone) > 20:
            messages.error(request,"Invalid Number: Phone Number Length must be miximum to 10 and minimum to 20")
            return redirect('index')
        content = Contact(name=name,email=email,phone=phone,message=message)
        content.save()
        messages.success(request, "Form submitted successfully. For details please check your email.")
        try:
            send_mail(f'Thank you for Contacting us',
                      f'Hi,\n\nThank you for contacting BT Business Official Partner.\n\nWe will be contacting you shortly.\n\nIf you have any questions please feel free to contact us, we are just an email away.\n\nThank You\n\nCustomers Service.\nBT Business Partner UK',
                      email, ['support@marketingservicesonline.co.uk'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        try:
            send_mail(f'Thank you for Contacting us',
                      f'Hi,\n\nThank you for contacting BT Business Official Partner.\n\nWe will be contacting you shortly.\n\nIf you have any questions please feel free to contact us, we are just an email away.\n\nThank You\n\nCustomers Service.\nBT Business Partner UK',
                      'support@marketingservicesonline.co.uk',
                      [email])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect('index')
    return render(request, "index.html")