from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse 
from .models import User, Destination , Session
from django.core.exceptions import ObjectDoesNotExist
import random
import time

# Create your views here.
def index(request):
    recent_destinations = Destination.objects.filter(share_publicly=True).order_by('-id')[:5]
    if request.user:
        return redirect('/destinations')
    return render(request, "destinationapp/index.html", {'destinations': recent_destinations})

def createAccount(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        User.objects.create(name=name, email=email, password_hash=password)
        return redirect('listDestinations')
    return render(request, 'destinationapp/createaccount.html')

def signIn(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            if user.password_hash == password:
                Session.objects.filter(user=user).delete()
                timestamp = str(int(time.time())) 
                random_number = str(random.randint(1000, 9999)) 
                token = timestamp + random_number  
                Session.objects.create(user=user, token=token)  
                response = redirect('listDestinations')
                response.set_cookie('session_token', token)   
                return response
            else:
                return HttpResponse('Invalid credentials', status=404)
        except ObjectDoesNotExist:
            return HttpResponse('User not found.', status=404)
    return render(request, "destinationapp/signin.html")

def listDestinations(request):
    user = request.user
    destinations = Destination.objects.filter(user=user)
    return render(request, 'destinationapp/destinations.html' ,{'destinations' : destinations})

def newDestination(request):
    return render(request, 'destinationapp/newdestinations.html')

def createDestination(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        review = request.POST.get('review')
        rating = request.POST.get('rating')
        share_publicly = request.POST.get('share_publicly') == 'on'
        user = request.user
        Destination.objects.create(name=name, review=review, rating=rating, share_publicly=share_publicly, user=user)
        return redirect('/destinations')
    return HttpResponse(status=405)
def logout(request):
    response = redirect('/')
    response.delete_cookie('session_token')  
    return response

def viewDestination(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id, user=request.user)
    return render(request, 'destinationapp/viewdestination.html', {'destination': destination})

def editDestination(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id, user=request.user)
    if request.method == 'POST':
        destination.name = request.POST.get('name')
        destination.review = request.POST.get('review')
        destination.rating = request.POST.get('rating')
        destination.share_publicly = request.POST.get('share_publicly') == 'on'
        destination.save()
        return redirect('listDestinations')
    return render(request, 'destinationapp/editdestinations.html', {'destination': destination})

def deleteDestination(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id, user=request.user)
    destination.delete()
    return redirect('listDestinations')

