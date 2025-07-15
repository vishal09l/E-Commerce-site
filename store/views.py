from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product, Cart, CartItem
from django.contrib.auth import authenticate, login, logout


def get_cart_count(request):
    session_id = request.session.session_key
    if session_id:
        cart = Cart.objects.filter(cart_id=session_id).first()
        if cart:
            return CartItem.objects.filter(cart=cart, is_active=True).count()
    return 0


def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    selected_category = request.GET.get('category')
    search_query = request.GET.get('search')

    if selected_category:
        products = products.filter(category__id=selected_category)
    if search_query:
        products = products.filter(name__icontains=search_query)

    cart_item_count = get_cart_count(request)

    return render(request, 'home.html', {
        'categories': categories,
        'products': products,
        'selected_category': int(selected_category) if selected_category else None,
        'search_query': search_query or '',
        'cart_item_count': cart_item_count,
    })


def cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    selected_size = request.POST.get('selected_size')

    try:
        cart = Cart.objects.get(cart_id=cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=cart_id(request))
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, size=selected_size)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1,
            size=selected_size
        )

    return redirect('cart')


def remove_from_cart(request, product_id):
    try:
        cart = Cart.objects.get(cart_id=cart_id(request))
        cart_item = CartItem.objects.get(product__id=product_id, cart=cart)
        cart_item.delete()
    except:
        pass
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 30
        grand_total = total + tax
    except Cart.DoesNotExist:
        cart_items = []
        tax = 0
        grand_total = 0

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand': grand_total,
        'cart_item_count': get_cart_count(request),
    }
    return render(request, 'cart.html', context)


def remove_one_from_cart(request, product_id):
    selected_size = request.GET.get('size')
    print("Selected Size:", selected_size)

    try:
        cart = Cart.objects.get(cart_id=cart_id(request))
        print("Cart:", cart)

        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.filter(product=product, cart=cart, size=selected_size).first()
        print("Cart Item:", cart_item)

        if cart_item:
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                print("Quantity decreased")
            else:
                cart_item.delete()
                print("Item deleted")
    except Cart.DoesNotExist:
        print("Cart not found")

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

    return render(request, 'product_list.html', {
        'products': queryset,
        'categories': categories,
        'selected_category': int(selected_category) if selected_category else None,
        'search_query': search_query or '',
        'cart_item_count': get_cart_count(request),
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    sizes = product.sizes.all()

    return render(request, 'product_detail.html', {
        'product': product,
        'sizes': sizes,
        'cart_item_count': get_cart_count(request),
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
            if user.is_staff:
                return redirect('/admin/')
            else:
                return redirect('/')

    return render(request, "login.html", {'cart_item_count': get_cart_count(request)})


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
            username=username,
            is_staff=False
        )
        user.set_password(password)
        user.save()
        messages.info(request, 'Account created successfully')
        return redirect('/login/')

    return render(request, "register.html", {'cart_item_count': get_cart_count(request)})


def women_products(request):
    women_category = Category.objects.filter(name__iexact='Women').first()
    if women_category:
        products = Product.objects.filter(category=women_category)
    else:
        products = Product.objects.none()

    return render(request, 'women_products.html', {
        'products': products,
        'cart_item_count': get_cart_count(request),
    })


def men_products(request):
    products = Product.objects.filter(category__name='Men')
    return render(request, 'men_products.html', {
        'products': products,
        'cart_item_count': get_cart_count(request),
    })


def kids_products(request):
    products = Product.objects.filter(category__name='Kids')
    return render(request, 'kids.html', {
        'products': products,
        'cart_item_count': get_cart_count(request),
    })


def fashion_products(request):
    products = Product.objects.filter(category__name='Fashion')
    return render(request, 'fashion.html', {
        'products': products,
        'cart_item_count': get_cart_count(request),
    })
