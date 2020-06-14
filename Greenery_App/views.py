from django.shortcuts import render, redirect
import bcrypt
from django.contrib import messages
from .models import *

def index(request):
    return render(request, 'index.html')

def register(request):
    print(request.POST)
    errors = User.objects.validator(request.POST)
    print(errors)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    hashed_password = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(first_name = request.POST['fname'], last_name = request.POST['lname'], email = request.POST['email'], password = hashed_password)
    print(new_user, "New user has been registered!")
    request.session['name'] = new_user.first_name
    request.session['id'] = new_user.id
    return redirect('/main')

def login(request):
    logged_user = User.objects.filter(email = request.POST['email'])
    if len(logged_user) > 0:
        logged_user = logged_user[0]
        if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.password.encode()):
            print(logged_user, "Logged user has been signed in!")
            request.session['name'] = logged_user.first_name
            request.session['id'] = logged_user.id
        return redirect('/main')
    return redirect('/')

def main(request):
    context = {
        'all_plants': Plant.objects.all()
    }
    return render(request, 'main.html', context)

def add_plant(request):
    if request.method == 'POST':
        errors = Plant.objects.validate_plant(request.POST)
        print(errors)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/main')
        new_plant = Plant.objects.create(plant_name = request.POST['plant_name'], description = request.POST['description'], poster = User.objects.get(id = request.session['plant_id']))
        print(new_plant, "New plant has been posted!")
        return redirect('/main')
    return redirect('/main')

def update_plant(request, plant_id):
    context = {
        'plant': Plant.objects.get(id = plant_id)
    }
    if request.method == 'POST':
        errors = Plant.objects.validate_update(request.POST)
        print(errors)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/plant/{str(plant_id)}')
        update_plant = Plant.objects.get(id = plant_id)
        update_plant.description = request.POST['description']
        update_plant.save()
        return redirect(f'/plant/{str(plant_id)}')
    return render(request, 'plant_profile.html', context)

def plant_profile(request, plant_id):
    context = {
        'plant_id': Plant.objects.get(id = plant_id),
    }
    return render(request, 'plant_profile.html', context)

def destroy_plant(request, plant_id):
    one_plant = Plant.objects.get(id = plant_id)
    if one_plant.poster.id == request.session['id']:
        one_plant.delete()
    return redirect('/main')

def logout(request):
    logout = request.session.clear()
    print(logout, "User has logged out.")
    return redirect('/')