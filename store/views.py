from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    selected_category = request.GET.get('category')
    search_query = request.GET.get('search')

    if selected_category:
        products = products.filter(category__id=selected_category)

    if search_query:
        products = products.filter(name__icontains=search_query)

    cart_item_count = sum(request.session.get('cart', {}).values())

    return render(request, 'home.html', {
        'categories': categories,
        'products': products,
        'selected_category': int(selected_category) if selected_category else None,
        'search_query': search_query or '',
        'cart_item_count': cart_item_count,
    })


def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_amount = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total = product.price * quantity
        total_amount += total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': total
        })

    cart_item_count = sum(cart.values())

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'cart_item_count': cart_item_count,
    })


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart
    return redirect('cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart

    return redirect('cart')


def product_list(request):
    queryset = Product.objects.all()
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    search_query = request.GET.get('search')

    if selected_category:
        queryset = queryset.filter(category__id=selected_category)

    if search_query:
        queryset = queryset.filter(name__icontains=search_query)

    cart_item_count = sum(request.session.get('cart', {}).values())

    return render(request, 'product_list.html', {
        'products': queryset,
        'categories': categories,
        'selected_category': int(selected_category) if selected_category else None,
        'search_query': search_query or '',
        'cart_item_count': cart_item_count,
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    sizes = product.sizes.all()
    cart_item_count = sum(request.session.get('cart', {}).values())

    return render(request, 'product_detail.html', {
        'product': product,
        'sizes': sizes,
        'cart_item_count': cart_item_count,
    })


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid username')
            return redirect('/login/')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid password')
        else:
            login(request, user)
            return redirect('/product_list/')

    cart_item_count = sum(request.session.get('cart', {}).values())

    return render(request, "login.html", {'cart_item_count': cart_item_count})


def logout_page(request):
    logout(request)
    return redirect('/')


def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already taken')
            return redirect('/register/')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.set_password(password)
        user.save()
        messages.info(request, 'Account created successfully')

    cart_item_count = sum(request.session.get('cart', {}).values())

    return render(request, "register.html", {'cart_item_count': cart_item_count})


def women_products(request):
    women_category = Category.objects.filter(name__iexact='Women').first()
    if women_category:
        products = Product.objects.filter(category=women_category)
    else:
        products = Product.objects.none()

    return render(request, 'women_products.html', {
        'products': products,
    })


def men_products(request):
    products = Product.objects.filter(category__name='Men')
    return render(request, 'men_products.html', {'products': products})

def kids_products(request):
    products = Product.objects.filter(category__name='Kids')
    return render(request, 'kids.html', {'products': products})
def fashion_products(request):
    products = Product.objects.filter(category__name='Fashion')
    return render(request, 'fashion.html', {'products': products})
