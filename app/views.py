from django.shortcuts import render, redirect
from .models import Category, Product
from django.http import JsonResponse
from app.forms import ProductModelForm, OrderModelForm, CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Q
from app.utils import filter_by_price


# Create your views here.

def index(request, category_id=None):
    search_query = request.GET.get('q', '')
    filter_type = request.GET.get('filter_type', '')

    categories = Category.objects.all()

    if category_id:
        products = Product.objects.filter(category=category_id)
    else:
        products = Product.objects.all()

    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    products = filter_by_price(filter_type, products)

    context = {
        'categories': categories,
        'products': products
    }
    return render(request, 'app/home.html', context)


def detail(request, product_id):
    product = Product.objects.get(id=product_id)
    if not product:
        return JsonResponse(data={'message': 'Oops. Page Not Found', 'status_code': 404})

    context = {
        'product': product
    }
    return render(request, 'app/detail.html', context)


# name = request.POST.get('name')


@login_required(login_url='/admin/')
def create_product(request):
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Product successfully created ✅"
            )
            # add messages

            return redirect('app:create')
    else:
        form = ProductModelForm()

    context = {
        'form': form
    }
    return render(request, 'app/create.html', context)


def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    if product:
        product.delete()
        return redirect('app:index')

    return render(request, 'app/detail.html')


def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            return redirect('app:detail', pk)
    else:
        form = ProductModelForm(instance=product)

    context = {
        'form': form,
        'product': product
    }
    return render(request, 'app/update.html', context)


def create_order(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        print('Order Post sending ....')
        form = OrderModelForm(request.POST)

        if form.is_valid():
            print('form valid')
            order = form.save(commit=False)
            order.product = product

            if order.quantity > product.stock:
                messages.error(request, 'Dont enough quantity')

            else:
                product.stock -= order.quantity
                print('order valid ')
                product.save()
                order.save()

                messages.success(request, 'Order successfully sent ✅')

                return redirect('app:detail', product_id=product.id)

    else:
        form = OrderModelForm()

    if request.method == 'POST' and 'comment_submit' in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.product = product
            comment.save()
            messages.success(request, "Comment added successfully ✅")
            return redirect('app:detail', product_id=product.id)
    else:
        comment_form = CommentForm()



    context = {
        'form': form,
        'product': product,
        'comment_form': comment_form,
        'comments': product.comments.all().order_by('-created_at'),
    }

    return render(request, 'app/detail.html', context)