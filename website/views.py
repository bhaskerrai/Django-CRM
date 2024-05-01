from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecord
from .models import Record

# Create your views here.
def home(request):
    records = Record.objects.all()

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Login Successful")
            return redirect("home")
    
        else:
            messages.error(request, "Login Failed! Please try again")
            return redirect("home")

    else:
        return render(request, "home.html", {"records": records})

def logout_user(request):
    logout(request)
    messages.success(request, "You have successfully logged out!")
    return redirect("home")

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()

            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(request, username=username, password=password)

            login(request, user)
            messages.success(request, "You have successfully registered!")
            return redirect("home")

    else:
        form = SignUpForm()
        return render(request, "register.html", {"form": form})
        
    return render(request, "register.html", {"form": form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)

        return render(request, "record.html", {"customer_record": customer_record})
    
    else:
        messages.success(request, "You must be logged in!")
        return redirect("home")

def delete_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        record.delete()
        messages.success(request, "Record Deleted!")
        return redirect("home")
    
    else:
        messages.success(request, "You must be logged in!")
        return redirect("home")
    
def add_record(request):
    form = AddRecord(request.POST or None)

    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added Successfully!")
                return redirect("home")

        return render(request, "add_record.html", {"form": form})

    else:
        messages.success(request, "You must be logged in to add record!")
        return redirect("home")

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecord(request.POST or None, instance= current_record)

        if form.is_valid():
            form.save()
            messages.success(request, "Record Updated Successfully!")
            return redirect("home")

        return render(request, "update_record.html", {"form": form})

    else:
        messages.success(request, "You must be logged in to update record!")
        return redirect("home")
    
