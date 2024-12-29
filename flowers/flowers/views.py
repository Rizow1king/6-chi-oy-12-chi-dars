from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import *
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate


def index(request: WSGIRequest):
    flowers = Flowers.objects.filter(published=True)
    context = {
        'flowers': flowers
    }

    return render(request, 'index.html', context)


def category(request: WSGIRequest, type_id):
    type = get_object_or_404(Categories, id=type_id)
    flowers = Flowers.objects.filter(type_id=type_id, published=True)
    context = {
        'type': type,
        'flowers': flowers
    }

    return render(request, 'type_detail.html', context)


def flower(request: WSGIRequest, flower_id):
    flower = get_object_or_404(Flowers, id=flower_id, published=True)

    context = {
        'flower': flower,
        "form": CommentForm(),
        "comments": Comment.objects.filter(flower_id=flower_id)
    }
    return render(request, 'detail.html', context)


def add_species(request: WSGIRequest):
    if request.method == 'POST':
        form = CategoriesForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            species = form.create()
            return redirect('type_detail', type_id=species.id)
    form = CategoriesForm()
    context = {
        'form': form,
        'title': "O'simlik turi qo'shish"
    }
    return render(request, 'add_species.html', context)


def add_flowers(request: WSGIRequest):
    if request.method == 'POST':
        form = FlowerForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            flowers = form.create()
            return redirect('flower_detail', flower_id=flowers.pk)

    form = FlowerForm()
    context = {
        'form': form,
        'title': "Gul qo'shish"
    }
    return render(request, 'add_flowers.html', context)


def update_species(request: WSGIRequest, type_id):
    species = get_object_or_404(Categories, id=type_id)

    if request.method == 'POST':
        form = CategoriesForm(data=request.POST)
        if form.is_valid():
            form.update(species)
            return redirect('type_detail', type_id=species.id)

    form = CategoriesForm(initial={
        'name': species.name,
        'definition': species.definition
    })

    context = {
        'form': form
    }

    return render(request, 'add_species.html', context)


def update_flowers(request: WSGIRequest, flower_id):
    flowers = get_object_or_404(Flowers, id=flower_id)
    if request.method == 'POST':
        form = FlowerForm(data=request.POST)
        if form.is_valid():
            form.update(flowers)
            return redirect('flower_detail')
    form = FlowerForm(initial={
        'name': flowers.name,
        'description': flowers.description,
        'price': flowers.price,
        'published': flowers.published,
        'type': flowers.type,
        'quantity': flowers.quantity
    })
    context = {
        'form': form
    }
    return render(request, 'add_flowers.html', context)


def delete_type(request, type_id):
    type = get_object_or_404(Categories, id=type_id)

    if request.method == 'POST':
        type.delete()
        messages.success(request, "Tur muvaffaqiyatli tarzda o'chirildi!")
        return redirect('home')

    messages.warning(request, "Ushbu tur o'chirib tashlamoqchimisiz!")
    return render(request, 'confirm_delete.html', {'type': type})


def delete_flowers(request, flower_id):
    flower = get_object_or_404(Flowers, id=flower_id)

    if request.method == 'POST':
        flower.delete()
        messages.success(request, "Gul muvaffaqiyatli tarzda o'chirildi!")
        return redirect('home')

    messages.warning(request, "Ushbu gulni o'chirib tashlamoqchimisiz!")
    return render(request, 'confirm_delete_for_flowers.html', {'flower': flower})


def register(request: WSGIRequest):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            password_confirm = form.cleaned_data.get('password_confirm')
            if password_confirm == password:
                user = User.objects.create_user(
                    form.cleaned_data.get("username"),
                    form.cleaned_data.get("email"),
                    password
                )
                messages.success(request, "Akkaunt muvaffaqiyatli qo'shildi!!")
                return redirect('login')
            else:
                print("Form errors:", form.errors)
    else:
        form = RegisterForm()
    context = {
        "form": form
    }
    return render(request, "auth/register.html", context)


def login_view(request: WSGIRequest):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            messages.success(request, "Xush kelibsiz!!!")
            login(request, user)
            return redirect('home')
    context = {
        "form": LoginForm()
    }
    return render(request, "auth/login.html", context)


def logout_view(request: WSGIRequest):
    logout(request)
    return redirect('login')


def terms(request: WSGIRequest):
    return render(request, "terms.html")


def comment_save(request: WSGIRequest, flower_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            flower = get_object_or_404(Flowers, pk=flower_id)
            form = CommentForm(data=request.POST)
            if form.is_valid():
                comment = Comment.objects.create(
                    text=form.cleaned_data.get("text"),
                    author=request.user,
                    flower=flower
                )
                messages.success(request, "Comment qo'shildi!!!")
            else:
                print(form.errors)
        return redirect('flower_detail', flower_id=flower_id)
    messages.error(request, "Avval login qiling!!!")
    return redirect('login')


def comment_delete(request: WSGIRequest, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_id)
        if request.user == comment.author or request.user.is_superuser:
            flower_id = comment.flower.pk
            comment.delete()
            messages.success(request, "Comment o'chirildi!!!")
            return redirect('flower_detail', flower_id=flower_id)
    messages.error(request, "Avval login qiling!!!")
    return redirect('login')


def comment_update(request: WSGIRequest, comment_id):
    comments = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        form = CategoriesForm(data=request.POST)
        if form.is_valid():
            flower_id = comments.flower.pk
            form.update(comments)
            return redirect('flower_detail', flower_id=flower_id)

    form = CommentForm(initial={
        'text': comments.text,
        })

    context = {
        'form': form
    }

    return render(request, 'detail.html', context)
