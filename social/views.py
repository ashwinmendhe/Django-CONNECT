from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from social.models import MyProfile, MyPost, FollowUser, PostLike, PostComment
#from social.forms import CreateUserForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


#Create your views here.
# def home1(req):
#     return render(req, "index.html") 
@method_decorator(login_required, name="dispatch")
class AboutView(TemplateView):
    template_name = "social/about.html"
  
class HomeView(TemplateView):
    template_name = "social/home.html"
    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        #context["nameash"]= "abc"
        followedList = FollowUser.objects.filter(followed_by = self.request.user.myprofile)
        followedList2 = []
        
        for e in followedList:
            followedList2.append(e.profile)
        si = self.request.GET.get("si")
        if si == None:
             si = ""
        postList= MyPost.objects.filter(Q(uploaded_by__in = followedList2)).filter(Q(subject__icontains = si) | Q(msg__icontains = si)).order_by("-id");
        for p1 in postList:
            p1.liked = False
            ob = PostLike.objects.filter(post=p1, liked_by=self.request.user.myprofile)
            if ob:
                p1.liked = True
            ob = PostLike.objects.filter(post=p1)
            p1.likecount = ob.count()
        context["mypost_list"] = postList
        return context

    # def get_queryset(self):
    #     si = self.request.GET.get("si")
    #     if si == None:
    #         si = ""
    #     postList= MyPost.objects.filter(Q(uploaded_by__in = followedList2)).filter(Q(subject__icontains = si) | Q(msg__icontains = si)).order_by("-id");




    # def get_context_data(self, **kwargs):
    #     context = TemplateView.get_context_data(self, **kwargs)
    #     followedList = FollowUser.objects.filter(followed_by = self.request.user.myprofile)
    #     followedList2 = []
    #     for e in followedList:
    #         followedList2.append(e.profile)
    #     postList = MyPost.objects.filter(uploaded_by__in = followedList2).order_by("-id")
        
    #     for p1 in postList:
    #         p1.liked = False
    #         ob = PostLike.objects.filter(post = p1,liked_by=self.request.user.myprofile)
    #         if ob:
    #             p1.liked = True        
    #         obList = PostLike.objects.filter(post = p1)
    #         p1.likedno = obList.count()
    #     context["mypost_list"] = postList
    #     return context;




class ContactView(TemplateView):
    template_name = "social/contact.html"

# class LoginView(TemplateView):
#     template_name = "social/login.html"

# class RegisterView(TemplateView):
#     template_name = "social/register.html"
# def loginPage(request):
#     return render(request, "social/login.html") 

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home1')
    else:
        form = CreateUserForm()  
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            
            if form.is_valid():
                form.save()
            
                user = form.cleaned_data.get('first_name')
                messages.success(request,'Account was created for ' + user)
            
                return redirect('login')
        context = {'form':form}
        return render(request, 'social/register.html',context)



def loginPage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to="/social/home")
    else:
        if request.method == 'POST':
            username=request.POST.get('username')
            password=request.POST.get('password')

            user1 = authenticate(request, username=username, password=password)
            if user1 is not None:
                login(request, user1)
                return HttpResponseRedirect(redirect_to="/social/home")
            else:
                messages.info(request, 'Username or password incorrect')
                #return render(request, 'accounts/login.html')
        return render(request, 'social/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')

def follow(req, pk):
    user = MyProfile.objects.get(pk=pk)
    FollowUser.objects.create(profile=user, followed_by = req.user.myprofile)
    return HttpResponseRedirect(redirect_to="/social/myprofile")

def unfollow(req, pk):
    user = MyProfile.objects.get(pk=pk)
    FollowUser.objects.filter(profile=user, followed_by = req.user.myprofile).delete()
    return HttpResponseRedirect(redirect_to="/social/myprofile")

def like(req, pk):
    post = MyPost.objects.get(pk=pk)
    PostLike.objects.create(post=post, liked_by = req.user.myprofile)
    return HttpResponseRedirect(redirect_to="/social/home")

def unlike(req, pk):
    post = MyPost.objects.get(pk=pk)
    PostLike.objects.filter(post=post, liked_by = req.user.myprofile).delete()
    return HttpResponseRedirect(redirect_to="/social/home")


@method_decorator(login_required, name="dispatch")    
class MyProfileUpdateView(UpdateView):
    model = MyProfile
    fields = ["name","status", "gender", "age", "phoneno","email", "address", "description", "pic"]
    




@method_decorator(login_required, name="dispatch")    
class MyPostCreateView(CreateView):
    model = MyPost
    fields = ["subject", "msg","pic"]
    def form_valid(self, form):
        self.object= form.save()
       
        self.object.uploaded_by = self.request.user.myprofile
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required, name="dispatch")
class MyPostListView(ListView):
    model = MyPost
    def get_queryset(self):
        si = self.request.GET.get("si")
        if si == None:
            si = ""
        return MyPost.objects.filter(Q(uploaded_by = self.request.user.myprofile)).filter(Q(subject__icontains = si) | Q(msg__icontains = si)).order_by("-id");
 
@method_decorator(login_required, name="dispatch")
class MyPostDetailView(DetailView):
    model = MyPost


@method_decorator(login_required, name="dispatch")    
class MyPostDeleteView(DeleteView):
    model = MyPost


@method_decorator(login_required, name="dispatch")    
class MyProfileListView(ListView):
    model = MyProfile
    def get_queryset(self):
        si = self.request.GET.get("si")
        if si == None:
            si = ""
        profList = MyProfile.objects.filter(Q(name__icontains = si) | Q(address__icontains = si) | Q(email__icontains = si) | Q(phoneno__icontains = si)).order_by("-id");
        for p1 in profList:
            p1.followed = False
            ob = FollowUser.objects.filter(profile = p1,followed_by=self.request.user.myprofile)
            if ob:
                p1.followed = True
        return profList
@method_decorator(login_required, name="dispatch")
class MyProfileDetailView(DetailView):
    model = MyProfile



# # user ke liye banane ke liye code karna h:
# #  view, url, html, link me
# # view me createview ka child banaya, url use view la url banaya
# # use url se jo html chalega wo html banao
# # fir uska link kro sbko jodo