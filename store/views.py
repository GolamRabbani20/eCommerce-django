from django.shortcuts import render, redirect
from . models import Category, Customer, Order, Product, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q  #Q is for multiple query
import json
from Card.card import Card

from .forms import signupForm, updateUserprofileForm, updatepassowdForm, userInformationForm

# Create your views here.
def searchProduct(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        #Query the product from database Model  #name__icontaints used for handel case-sensitive-> Python/python/pYthon/....
        searched = Product.objects.filter(
            Q(name__icontains = searched) | Q(description__icontains=searched) | Q(price__icontains=searched) | Q(sale_price__icontains=searched)
        )

        #test for null
        if not searched:
            messages.warning(request, ('The product does not exist, Please try again!'))
            return render(request, 'store/search_product.html', {})
        else:
            return render(request, 'store/search_product.html', {'searched':searched})
    else:
        return render(request, 'store/search_product.html', {})
    
def updateUserinfo(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = userInformationForm(request.POST or None, instance=current_user)
        if form.is_valid():
            form.save()
            messages.success(request, ('You information has been updated successfully.'))
            return redirect('home')
        else:
            return render(request, 'store/update_userinfo.html', {'form':form})
    else:
        messages.warning('You must be logged in to update your information')
        return redirect('login')

def updatePassword(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = updatepassowdForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your Password updated successfully! Please login again.')
                logout(request)
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return redirect('update_password')
        else:
            form = updatepassowdForm(current_user)
            return render(request, 'store/update_password.html', {'form':form})
    else:
        messages.warning(request, ('You must be logged in to update your password!'))
        return redirect('home')

def updateUserprofile(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = updateUserprofileForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, ('Your profile has been updated successfully!'))
            return redirect('home')
        return render(request, 'store/update_user.html', {'user_form':user_form})
    else:
        messages.warning(request, ('You must be logged in to update your profile!'))
        return redirect('home')

def categoricalProduct(request, cat_name):
    try:
        category = Category.objects.get(name=cat_name)
        products = Product.objects.filter(category=category)
        return render(request, 'store/category.html', {'products':products, 'category':category})
    except:
        messages.warning(request, ("The category doe't exist...!"))
        return redirect('home')

def categorySummery(request):
    categories = Category.objects.all()
    return render(request, 'store/summery_category.html', {'categories':categories}) 

def viewProduct(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'store/viewproduct.html', {'product': product})

def Homepage(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products':products})

def aboutUs(request):
    return render(request, 'store/aboutus.html', {})

def loginUser(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You have been Logged in successfuly!'))

            #Do somthing for shopping cart stuff
            current_user = Profile.objects.get(user__id = request.user.id)
            #Get the saved-cart from database
            saved_cart = current_user.old_card
            if saved_cart:
               #Convert the database string to python dictonary using JSON
               converted_cart = json.loads(saved_cart)
               #Add the loaded cart-dictonary to our Session
               cart = Card(request)
               #Loop though the cart and add the items from the database
               for key, value in converted_cart.items():
                   cart.db_add(product_id=key, quantity=value)

            return redirect('home')
        
        else:
            messages.warning(request, ('There was an error! Please try again.'))
            return redirect('login_user')
    else:
        return render(request, 'store/login.html')

def logoutUser(request):
    logout(request)
    messages.success(request, ('You have been logged out!'))
    return redirect('home')

def signupUser(request):
    form = signupForm()
    if request.method == "POST":
        form = signupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #Login User
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('You have registered successfully!'))
            return redirect('update_userinfo')
        else:
            for error in list(form.errors.values()):
                    messages.error(request, error)
            return redirect('signup_user')
    else: 
        return render(request, 'store/signup.html', {'form': form})