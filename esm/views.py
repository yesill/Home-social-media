from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .forms import RegisterForm, LoginForm
#--------------------------------
#hata verdiğine aldırma hata yok çalışıyor
from post.forms import PostForm
from post.models import Post
from comment.forms import CommentForm
from comment.models import Comment
#--------------------------------
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "index.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        if User.objects.filter(email=email).exists():
            messages.warning(request,"bu mail adresi kullanımda!")

        else:
            if User.objects.filter(username=username).exists():
                messages.warning(request,"kulanıcı adı kullanımda!")

            else:
                try:
                    new_user = User(username=username, email=email)
                    new_user.set_password(password)
                    new_user.save()
                    login(request, new_user)
                    return redirect("home")
                except:
                    messages.warning(request, "something went wrong! try again")

    return render(request, "register.html")


def loginUser(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            messages.warning(request, "KUllanıcı adı veya şifre hatalı!")
            return render(request, "login.html")

        login(request, user)
        return redirect("home")

    return render(request, "login.html")


def logoutUser(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("index")


def profile(request):
    if request.user.is_authenticated:

        if "bio" in str(request.POST):
            user = User.objects.filter(id=request.user.id)[0]
            user.first_name = request.POST['bio']
            print(f"{user.first_name}")
            user.save()
            return redirect("profile")

        if "post_submit" in str(request.POST):
            form = PostForm(request.POST or None)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                #profile a dönmesi lazım ki yeni post akış ekranında gözüksün :T
                return redirect("profile")

        if "like_submit" in str(request.POST):
            print(f"like submit")
            #request içerisinden post id çekiliyor.(ilkel yöntem)
            post_id = str(request.POST).split('!:!')[1]
            #id'si alınan postu tamamen alıyoruz
            post = Post.objects.filter(id=post_id)[0]
            #request içerisinden username'i alıyoruz
            username = request.user.username
            #user beğenenler arasında yok ise ekliyoruz
            if not username in post.likers:
                post.likers.append(username)
            #user beğenenler arasında var ise çıkartıyoruz
            else:
                post.likers.remove(username)
            post.save()

        posts = Post.objects.filter(author=request.user)[::-1][:20]
        context = {
            "posts": posts,
        }

        return render(request, "profile.html", context)

    return redirect("index")


def home(request):
    if request.user.is_authenticated:

        if "post_submit" in str(request.POST):
            form = PostForm(request.POST or None)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                #home a dönmesi lazım ki yeni post akış ekranında gözüksün :T
                return redirect("home")

        if "like_submit" in str(request.POST):
            #request içerisinden post id çekiliyor.(ilkel yöntem)
            post_id = str(request.POST).split('!:!')[1]
            #id'si alınan postu tamamen alıyoruz
            post = Post.objects.filter(id=post_id)[0]
            #request içerisinden username'i alıyoruz
            username = request.user.username
            #user beğenenler arasında yok ise ekliyoruz
            if not username in post.likers:
                post.likers.append(username)
            #user beğenenler arasında var ise çıkartıyoruz
            else:
                post.likers.remove(username)
            post.save()

        else:
            posts = Post.objects.filter()[::-1][:20]
            context = {
                "posts": posts,
            }
            return render(request, "home.html", context)

    #giriş yapılı değilse indexe yönlendir.
    return redirect("index")


def detail(request, id):
    if request.user.is_authenticated:

        if "like_submit_comment" in str(request.POST):
            #request içerisinden comment id çekiliyor.(ilkel yöntem)
            comment_id = str(request.POST).split('!:!')[1]
            #id'si alınan commenti tamamen alıyoruz
            comment = Comment.objects.filter(id=comment_id)[0]
            #request içerisinden username'i alıyoruz
            username = request.user.username
            #user beğenenler arasında yok ise ekliyoruz
            if not username in comment.likers:
                comment.likers.append(username)
            #user beğenenler arasında var ise çıkartıyoruz
            else:
                comment.likers.remove(username)
            comment.save()

        if "like_submit_post" in str(request.POST):
            #id'si bilinen postu tamamen alıyoruz
            post = Post.objects.filter(id=id)[0]
            #request içerisinden username'i alıyoruz
            username = request.user.username
            #user beğenenler arasında yok ise ekliyoruz
            if not username in post.likers:
                post.likers.append(username)
            #user beğenenler arasında var ise çıkartıyoruz
            else:
                post.likers.remove(username)
            post.save()

        if "comment_submit" in str(request.POST):
            form = CommentForm(request.POST or None)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.post_id = id
                comment.save()

        post = get_object_or_404(Post, id=id)
        comments = Comment.objects.filter(post_id=id)[::-1][:20]
        context = {
            "post": post,
            "comments": comments,
        }
        return render(request, "detail.html", context)

    return redirect(index)
