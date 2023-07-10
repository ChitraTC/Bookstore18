from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView, ListView
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from .models import Book, Customer, Cart, Order
from django.http import JsonResponse, request


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


class CategoryView(View):
    def get(self, request, val):
        book = Book.objects.filter(category=val)
        # count the number of title of respective category and return the title
        title = Book.objects.filter(category=val).values('title')
        return render(request, "category.html", locals())


class BookDetailView(View):
    def get(self, request, pk):
        book = Book.objects.get(pk=pk)
        return render(request, "bookdetail.html", locals())


class BookDetailView1(DetailView):
    model = Book
    context_object_name = 'books'
    template_name = 'bookdetail.html'

class SearchResultView1(ListView):
    model = Book
    template_name = 'search_result.html'

    def get_queryset(self):
        query=self.request.GET.get('q')
        return Book.objects.filter(
            Q(title=query) | Q(author=query)
        )

def SearchResultView(request):
        query=request.GET['query']
        allbook=Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
        params = {'allbook' : allbook}
        return render(request,'search_result.html',params)

class CategoryTitle(View):
    def get(self, request, val):
        book = Book.objects.filter(title=val)
        title = Book.objects.filter(category=book[0].category).values('title')
        return render(request, "category.html", locals())


# class BookDetailView(DetailView):
#     model = Book
#     context_object_name = 'books'
#     template_name = 'bookdetail.html'

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'CustomerRegistration.html', locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User Registration Success!!!")
        else:
            messages.warning(request, "Invalid Credentials")
        return render(request, 'CustomerRegistration.html', locals())


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'profile.html', locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, state=state,
                           zipcode=zipcode)
            reg.save()
            messages.success(request, "Profile Saved Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'profile.html', locals())


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'address.html', locals())


class updateAddress(View):
    def get(self, request, b_id):
        add = Customer.objects.get(pk=b_id)
        form = CustomerProfileForm(instance=add)
        return render(request, 'updateAddress.html', locals())

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Profile Updated Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect("address")


def Add_to_cart(request):
    user = request.user
    book_id = request.GET.get('b_id')
    book = Book.objects.get(id=book_id)
    Cart(user=user, book=book).save()
    return redirect('/cart')


def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.book.price
        amount = amount + value
    totalamount = amount + 40
    return render(request, 'add_to_cart.html', locals())


class checkout(View):
    model = Book
    template_name = 'checkout.html'

class checkout1(View):
    model = Book
    template_name = 'checkout.html'


# def checkout(View):
#     def get(self,request):
#         return render(request,'checkout.html',locals())


def PaymentComplete(request, pk):
    book = Book.objects.get(id=pk)
    Order.objects.create(
        book=book
    )
    return JsonResponse('Payment Completed', safe=False)


@login_required
def cart1(request):
    cart_qs = Cart.objects.filter(user=request.user)
    if cart_qs.exists():
        cart_obj = cart_qs.first()
        cart_items = CartItem.objects.filter(cart=cart_obj)
    else:
        cart_obj = None
        cart_items = []

    context = {
        'cart': cart_obj,
        'cart_items': cart_items
    }
    return render(request, 'add_to_cart.html', context)


@login_required
def add_to_cart1(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart_qs = Cart.objects.filter(user=request.user)
    if cart_qs.exists():
        cart_obj = cart_qs.first()
    else:
        cart_obj = Cart.objects.create(user=request.user, total_price=Decimal)

    cart_item, created = CartItem.objects.get_or_create(book=book, cart=cart_obj)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    cart_obj.total_price += Decimal(str(book.price))
    cart_obj.save()
    return redirect('add_to_cart')


@login_required
def remove_from_cart1(request, b_id):
    book = get_object_or_404(Book, id=b_id)
    cart_qs = Cart.objects.filter(user=request.user)
    if cart_qs.exists():
        cart_obj = cart_qs.first()
        cart_item_qs = CartItem.objects.filter(book=book, cart=cart_obj)
        if cart_item_qs.exists():
            cart_item = cart_item_qs.first()
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
            cart_obj.total_price -= Decimal(str(book.price))
            cart_obj.save()
    return redirect('add_to_cart')


def plus_cart(request):
    if request.method == 'GET':
        book_id = request.GET['book_id']
        c = Cart.objects.get(Q(book=book_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.book.price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }

        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        book_id = request.GET['book_id']
        c = Cart.objects.get(Q(book=book_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.book.price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }

        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        book_id = request.GET['book_id']
        c = Cart.objects.get(Q(book=book_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.book.price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

class BookCheckoutView(DetailView):
    model = Book
    template_name = 'checkout.html'

class BookCheckoutView1(View):
    model = Book
    template_name = 'checkout1.html'

def PaymentComplete(request,pk):
    product = Book.objects.get(id=pk)
    Order.objects.create(
        product=product
    )
    return JsonResponse('Payment Completed', safe=False)