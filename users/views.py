from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, CreateView, UpdateView
from users.models import UserProfile
from .forms import  UserProfileForm, UserForm
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required, login_required
# Create your views here.






# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
# /* /                                    /*/
# /* /         REGISTER                  / */
# /* /                                    /*/
# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/

#register is not in database, because of this, we should create all of it
def register(request):
    # if request method== post ise deyip yapıyorduk, şimdi tek satırla yaptık
    #from django.contrib.auth.forms import UserCreationForm,UserChangeForm
    form = UserCreationForm(request.POST or None)
    #this form is created by us,  from .forms import UserProfileForm
    form_added = UserProfileForm(request.POST or None, request.FILES or None)

    if form.is_valid() and form_added.is_valid():
        form.save()
        # form_user.save()#bunu yani ikinci formu save ederken user i alması lazım ama save edince id elimizde kalmıyor
        #bu yüzden form_user.save() yerine aşağıdaki işlemleri yapıyoruz
        profile = form_added.save(commit=False) #database e henüz kaydetme bekle diyoruz, gelen veri şimdi dictionary e çevrldi, amacımız buydu
        profile.user = form.save()
        profile.save()
        profile=form_added
        # that creates a new user
        # after creation of the user, want to authenticate it. bu useri authenticate etmek için iki bilgiye ihtiyacım var:
        username = form.cleaned_data['username'] 
        password = form.cleaned_data['password1'] 
        # şimdi bu dataları aldık user değişkenine authenticate verelim
        # from django.contrib.auth import authenticate,login
        user = authenticate(username=username,password=password)  # usera authenticate verdik
        # want user to login right after registered, import login
        login(request, user)  # zorunda değiliz
        # user_infos = user.objects.get(id=id)
        # want to redirect to home page, import redirect
        #from django.shortcuts import render,redirect
        return redirect('home')
    context = {
        'form': form,
        'form_added': form_added
    }
    return render(request, 'registration/register.html', context)



# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
# /* /                                    /*/
# /* /         CBV - READ(GET)           / */
# /* /                                    /*/
# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/


class UserListRead(ListView):
    model = UserProfile
    context_object_name = 'userprofile'
    template_name = 'users/userlist.html'
    
    # default template name : # app/modelname_list.html
    # this fits our template name no need to use this time
    # template_name = "study_cbv/study_cbv.html"
    # context_object_name = 'students'  # default context name : object_list
    # paginate_by = 10
    # queryset = Student.objects.all() or filter
    # get_queryset method for more owerfull filtering ( we can put data into get_context_data method and send template )


def users_list_read(request):
    userprofile = UserProfile.objects.all()
    # student_list = get_object_or_404(Student)
    print("resim var mı------------ ", bool(UserProfile.profile_pic))

    context = {
        'userprofile': userprofile
    }
    return render(request, 'users/userlist.html', context)


# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
# /* /                                    /*/
# /* /         DETAIL                     /*/
# /* /                                    /*/
# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
def user_detail(request, id):
    userdata = UserProfile.objects.get(id=id)
    # print(student.profile_pic)
    print("User içindekiler ", id, bool(UserProfile.profile_pic))
    context = {
        'userdata': userdata,
    }
    return render(request, 'users/user_detail.html', context)

#from django.views.generic import TemplateView, ListView, DetailView,DeleteView,CreateView,UpdateView

class UserDetailView(DetailView):
    model = UserProfile
    context_object_name = 'userprofile'
    template_name = 'users/user_detail.html'
    pk_url_kwarg = 'id'


# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
# /* /                                    /*/
# /* /         LOGIN Override             /*/
# /* /                                    /*/
# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/

#from django.contrib import messages
#from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

def user_login(request):

    form = AuthenticationForm(request, data=request.POST)

    if form.is_valid():
        user = form.get_user()
        if user:
            messages.success(request, "Login successfull")
            login(request, user)
            return redirect('home')
    return render(request, 'users/user_login.html', {"form": form})

# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
# /* /                                    /*/
# /* /         PASSWORD CHANGE            /*/
# /* /                                    /*/
# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/

def password_change(request):
    if request.method == 'POST':
        # We will use user change form this time
        # Import it
        form = UserChangeForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('home')
    else:
        form = UserChangeForm()

    context = {
        'form': form
    }
    return render(request, "registration/password_change.html", context)


# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
# /* /                                    /*/
# /* /             LOGOUT                 /*/
# /* /                                    /*/
# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
def user_logout(request):
    messages.success(request, "You Logged out!")
    logout(request)
    return redirect('home')


# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
# /* /                                    /*/
# /* /         CRUD - DELETE(POST)        /*/
# /* /                                    /*/
# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
def user_delete(request, id):
    # student = get_object_or_404(Student, id=id)
    userdata = UserProfile.objects.get(id=id)
    print('userdata : -------', userdata)
    if request.method == "POST":
        userdata.delete()
        print("--------succesfully deleted----------")
        messages.success(request, "User Deleted!")
        return redirect("home")
    context = {
        'userdata': userdata,
    }
    return render(request, "todo/home.html", context)


# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
# /* /                                    /*/
# /* /         CRUD - UPDATE(POST)        /*/
# /* /                                    /*/
# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/


def profile(request):
    u_form = UserForm(request.POST or None, instance=request.user)
    p_form = UserProfileForm(request.POST or None, instance=request.user.userprofile, files=request.FILES)

    if u_form.is_valid() and p_form.is_valid():
        u_form.save()
        p_form.save()
        messages.success(request, "Your profile has been updated!")
        return redirect('home')

    context = {
        "u_form": u_form,
        "p_form": p_form
    }
    return render(request, "users/profile.html", context)


