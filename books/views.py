from django.contrib import messages
from django.http import Http404, JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from books.forms import BookForm, CommentForm
from books.models import YEAR_CHOICES, Books, Comment, WatchedLinks
from books.utils import q_search
from django.contrib.auth.decorators import login_required

def catalog(request, category_slug=None):
    page = request.GET.get('page', 1)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)

    if category_slug == 'all':
        books = Books.objects.all()
    elif query:
        books = q_search(query)
    else:
        books = Books.objects.filter(category__slug = category_slug)
        if not books.exists():
            raise Http404()
    if order_by and order_by != 'default':
        books = books.order_by(order_by)
        
    paginator = Paginator(books, 3)
    current_page = paginator.page(int(page))    
    context = {
        "title": "Catalog",
        "books": current_page,
        "slug_url": category_slug,
    }
    return render(request, "books/catalog.html", context)

def book(request, book_slug):
    book = Books.objects.get(slug=book_slug)
    category_all = book.category.all()
    categories_filtered = ", ".join([category.name for category in category_all])
    
    pdf_link = None
    if request.user.is_authenticated:
        if book.pdf_file and "Електронні книги" in categories_filtered and request.user.role == 0 and \
            request.user.abonement_set.filter(abonement=True, abonement_end__gte=timezone.now()).exists():
            pdf_link = book.pdf_file.url
    if request.method == 'POST':
        if not request.user.is_authenticated: 
            messages.warning(request, 'Ви повинні бути авторизовані.')
            return redirect(reverse('user:login'))
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.book = book
            comment.save()
            return redirect('catalog:book', book_slug=book_slug)
    else:
        form = CommentForm()
        
    category_slug_url = request.GET.get('category_slug', 'all')
    comments = Comment.objects.filter(book=book)
    context = {
        'book': book,
        'categories_filtered': categories_filtered,
        'pdf_link': pdf_link,
        'form': form,
        'comments': comments,
        'category_slug_url': category_slug_url,
    }
    return render(request, "books/book.html", context)

@login_required
def update_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if comment.user != request.user:
        messages.error(request, 'Це не ваш відгук.')
        return redirect('catalog:book', book_slug=comment.book.slug)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш відгук був успішно оновлений.')
            return redirect('catalog:book', book_slug=comment.book.slug)
        else:
            messages.error(request, 'Помилка при введенні.')
    return redirect(request.META['HTTP_REFERER'])


@login_required
def check_watched_link(request):
    if request.user.role != 0:
        messages.warning(request, 'Ви не є читачем.')
        return redirect(reverse('main:index'))
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Books, id=book_id)
        if not WatchedLinks.objects.filter(user=request.user, book=book).exists():
            WatchedLinks.objects.create(user=request.user, book=book)
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def watched_links(request):
    if request.user.role != 0:
        messages.warning(request, 'Ви не є читачем.')
        return redirect(reverse('main:index'))
    watched_links = WatchedLinks.objects.filter(user=request.user, book__pdf_file__isnull=False)

    context = {
        'watched_links': watched_links,
    }
    return render(request, 'books/watched_links.html', context)

@login_required
def create_book(request):
    if request.user.role != 1:
        return render(request, 'includes/404.html', status=404) 

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            if not book.quantity:
                book.quantity = 0
            if not book.is_being_read:
                book.is_being_read = 0
            if not book.pages:
                book.pages = 0
            if not book.author:
                book.author = ""
            book.save()
            form.save_m2m()
            messages.success(request, f'Книгу "{book.name}" успішно створено')
            return redirect(reverse('catalog:book', kwargs={'book_slug': book.slug}))
    else:
        form = BookForm()
    context = {
        'form': form,
        'YEAR_CHOICES': dict(YEAR_CHOICES),
    }
    return render(request, 'books/book_form.html', context)

@login_required
def update_book(request, book_slug):
    if request.user.role != 1:
        return render(request, 'includes/404.html', status=404) 

    book = get_object_or_404(Books, slug=book_slug)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            if not book.quantity:
                book.quantity = 0
            if not book.is_being_read:
                book.is_being_read = 0
            if not book.pages:
                book.pages = 0
            if not book.author:
                book.author = ""
            book.save()
            form.save_m2m()
            messages.success(request, f'Книгу "{book.name}" успішно оновлено')
            return redirect(reverse('catalog:book', kwargs={'book_slug': book.slug}))
    else:
        form = BookForm(instance=book)
    context = {
        'form': form,
        'YEAR_CHOICES': dict(YEAR_CHOICES),
        'book': book,
    }
    return render(request, 'books/book_form.html', context)
