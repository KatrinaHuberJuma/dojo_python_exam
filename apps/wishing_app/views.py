from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Wish, User

# Create your views here.
def index(request):
    return render(request, 'wishing_app/index.html')


def success(request):
    if "first_name" in request.session:
        context = {
            'my_pending_wishes': [wish for wish in Wish.objects.filter(wished_for_by=request.session['id']) if wish.granted==False],
            'all_ganted_wishes': Wish.objects.filter(granted=True),
        }
        return render(request, "wishing_app/success.html", context)
    return redirect('/')



def login(request):
    errors = {}
    if request.method == "POST":
        possible_user = User.objects.filter(email=request.POST["email"])
        try:
            this_user = possible_user[0]
            if request.POST["password"] == this_user.password:
                request.session['first_name'] = this_user.first_name
                request.session['id'] = this_user.id
                request.session['last_name'] = this_user.last_name
                return redirect("/success")
            errors['password_oopsie_error']= "You seem to have forgotten your password. Too bad for you, we for sure don't save your plaintext password so get a new email and come back."
        except:
            errors['email_oopsie_error']=  "No user exists with this email, go ahead and register!"
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
    return redirect("/")

def reg(request):
    if request.method == "POST":
        # pass the post data to the method we wrote and save the response in a variable called errors
        errors = User.objects.basic_validator(request.POST) 
        if request.POST["password"] != request.POST["confirm_password"]:
            errors['pw_confrimation_fail'] = "Password does not match confirmation password"     
        # check if the errors dictionary has anything in it
        if len(errors) > 0:
            # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                messages.error(request, value)
            # redirect the user back to the form to fix the errors
            return redirect('/')
        else:
            password = request.POST["confirm_password"]
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            email = request.POST["email"]
            new_user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=password)
            request.session['first_name'] = new_user.first_name
            request.session['last_name'] = new_user.last_name
            request.session['id'] = new_user.id
    return redirect("/success")


def logout(request):
    request.session.clear()
    return redirect('/')

def new_wish(request):
    return render(request, "wishing_app/new_wish.html")

def add_wish(request):
    if request.method == "GET":
        return redirect("/")
    if request.method == "POST":# pass the post data to the method we wrote and save the response in a variable called errors
        errors = Wish.objects.basic_validator(request.POST)
        if len(errors) > 0:
            # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                messages.error(request, value)
            # redirect the user back to the form to fix the errors
            return redirect('/new')
        title = request.POST["wish_title"]
        description = request.POST["wish_description"]
        user = User.objects.get(id=request.session['id'])
        new_wish = Wish.objects.create(title=title, description=description, wished_for_by=user)
        new_wish.fans.add(User.objects.get(id=request.session['id']))
        print(new_wish.title)
        return redirect("/success")

def edit(request, wish_id):
    context = {
        'wish': Wish.objects.get(id=wish_id),
    }
    return render(request, 'wishing_app/edit_wish.html', context)


def update(request, wish_id):
    if request.method == "POST":
        # pass the post data to the method we wrote and save the response in a variable called errors
        errors = Wish.objects.basic_validator(request.POST)
        # check if the errors dictionary has anything in it
        if len(errors) > 0:
            # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                messages.error(request, value)
            # redirect the user back to the form to fix the errors
            return redirect('/wishes/' + str(wish_id) + '/edit') #wishes/(?P<wish_id>\d+)/edit
        else:
            this_wish = Wish.objects.get(id=wish_id)
            this_wish.title = request.POST["wish_title"]
            this_wish.description = request.POST["wish_description"]
            this_wish.save()
            return redirect("/success")
    return redirect("/wishes/" + wish_id +"/edit")


def grant(request, wish_id):
    this_wish = Wish.objects.get(id=wish_id)
    this_wish.granted = True
    this_wish.save()
    return redirect("/success")

def destroy(request, wish_id):
    dying_wish = Wish.objects.get(id=wish_id)
    dying_wish.delete()
    return redirect("/success")



# <td><a href="/wishes/{{wish.id}}/like">Like/unlike</a></td>
def toggle_like(request, wish_id): #this is not quite working
    wish = Wish.objects.get(id=wish_id)
    # wish_fans = wish.fans.all()
    session_user = User.objects.get(id=request.session['id'])
    if session_user not in wish.fans.all():
        wish.fans.add(session_user)
        return redirect("/success")
    wish.fans.remove(session_user)
    return redirect("/success")
