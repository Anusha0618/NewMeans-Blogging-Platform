from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

    )
from django.shortcuts import render, redirect

from blog.forms.auth import UserLoginForm, UserRegisterForm

def login_view(request):
    print(request.user.is_authenticated)
    next = request.GET.get('next')
    title = "Login"
    alternate ="SignUp"
    alternate_url = '/register/'
    quote = "Not Registered Yet?"
    d1 = "Hey, good to see you again!"
    d2 = "login to get going"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect("/blogs/")
    return render(request, "auth_form.html", {"form":form, "title": title,"alternate":alternate,"alternate_url":alternate_url,"quote":quote,"d1":d1,"d2":d2})


def register_view(request):
    print(request.user.is_authenticated)
    next = request.GET.get('next')
    title = "Register"
    alternate = "Login"
    alternate_url = '/login/'
    quote = "Already Registered?"
    d1="NewMeans"
    d2="Create an account!"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect("/blogs/")

    context = {
        "form": form,
        "title": title,
        "alternate": alternate,
        "alternate_url": alternate_url,
        "quote":quote,
        "d1": d1,
        "d2": d2
    }
    return render(request, "auth_form.html", context)


def logout_view(request):
    logout(request)
    return redirect("/blogs/")