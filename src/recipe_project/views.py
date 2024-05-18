from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.contrib.auth import logout


def root_redirect(request):
    return redirect('recipes:welcome')

def logout_view(request):
    logout(request)
    return render(request, "success.html")


def login_view(request):
    error_message = None

    form = AuthenticationForm()

    if request.method == "POST":
        # read the data sent by the form via POST request
        form = AuthenticationForm(data=request.POST)

        # check if form is valid
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            # use Django authenticate function to validate the user
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("recipes:home")
        else:
            error_message = "ooops.. something went wrong"

    context = {"form": form, "error_message": error_message}

    return render(request, "auth/login.html", context)


def logout_view(request):
    logout(request)
    return render(request, "auth/success.html")
