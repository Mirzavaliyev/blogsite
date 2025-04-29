from multiprocessing.resource_tracker import register
from .forms import CommentForm, PostForm

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post, Category
from django.utils.text import slugify
from django.contrib.auth.models import User
from .models import Post, Category, PostView
from .forms import CommentForm 

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def home(request):
    category_id = request.GET.get('category')
    categories = Category.objects.all()
    if category_id:
        posts = Post.objects.filter(category_id=category_id).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/home.html', {'page_obj': page_obj, 'categories': categories})
@login_required
def create_post(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        category_id = request.POST['category']
        image = request.FILES.get('image')
        category = get_object_or_404(Category, id=category_id)
        Post.objects.create(
            title=title,
            content=content,
            category=category,
            image=image,
            author=request.user,
            slug=slugify(title)
        )
        return redirect('home')
    return render(request, 'main/create_post.html', {'categories': categories}


        )
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'main/login.html', {'error': 'Noto‘g‘ri username yoki parol'})
    return render(request, 'main/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

def about(request):
    return render(request, 'main/about.html')  # optional: about sahifasi bo‘lsa

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    # Foydalanuvchining IP manzilini olish
    ip_address = get_client_ip(request)
    # IP manzil allaqachon postni ko‘rganmi, tekshirish
    if not PostView.objects.filter(post=post, ip_address=ip_address).exists():
        # Agar ko‘rmagan bo‘lsa, ko‘rishni qo‘shish
        PostView.objects.create(post=post, ip_address=ip_address)
        post.views_count += 1
        post.save()

    # Izohlarni olish
    comments = post.comments.all()

    # Izoh qo‘shish logikasi
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')  # Foydalanuvchi login qilmagan bo‘lsa
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', slug=slug)
    else:
        form = CommentForm()

    next_post = Post.objects.filter(id__gt=post.id).order_by('id').first()
    previous_post = Post.objects.filter(id__lt=post.id).order_by('-id').first()
    return render(request, 'main/post_detail.html', {
        'post': post,
        'next_post': next_post,
        'previous_post': previous_post,
        'comments': comments,
        'form': form
    })
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password != password_confirm:
            return render(request, 'main/register.html', {'error': 'Parol mos kelmadi'})
        if User.objects.filter(username=username).exists():
            return render(request, 'main/register.html', {'error': 'Bu username avvaldan mavjud'})
        if User.objects.filter(email=email).exists():
            return render(request, 'main/register.html', {'error': "Bu email avvaldan mavjud"})
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        login(request, user)
        return redirect('home')

    return render(request, 'main/register.html')
    
@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user != post.author and not request.user.is_superuser:
        return redirect('post_detail', slug=slug)  # Faqat muallif yoki admin tahrirlashi mumkin
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'main/edit_post.html', {'form': form, 'post': post})    