"""
URL configuration for Bookstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views
from .views import CategoryView, BookDetailView, CategoryTitle, CustomerRegistrationView, ProfileView, updateAddress, \
    PaymentComplete, checkout, Add_to_cart, BookCheckoutView, BookCheckoutView1, SearchResultView
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm

urlpatterns = [
    path('',views.home,name='Home'),
    # path('search/',SearchResultView.as_view(),name = 'search_result'),
    path('search/',views.SearchResultView,name= 'search_result'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path("category/<slug:val>",CategoryView.as_view(),name="category"),
    path("category-title/<val>", CategoryTitle.as_view(), name="category-title"),
    path("bookDetail/<int:pk>", BookDetailView.as_view(), name="bookdetail"),

    path('profile/',ProfileView.as_view(),name = "profile"),
    path('address/', views.address, name="address"),
    path('updateAddress/<int:pk>', updateAddress.as_view(), name="updateAddress"),

    #cart
    path('add_to_cart/',Add_to_cart,name="add_to_cart"),
    path('cart/',views.show_cart,name='show_cart'),
    path('checkout/<int:pk>/',BookCheckoutView.as_view(),name = 'checkout'),
    path('checkout1/',BookCheckoutView1.as_view(),name = 'checkout1'),
    path('complete/',PaymentComplete,name='complete'),

    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    # path('cart/', cart, name='mycart'),
    # path('cart/add/<int:book_id>/', add_to_cart, name="add_to_cart"),
    # path('cart/remove/<int:book_id>/', remove_from_cart, name="remove_from_cart"),


    #login authentication
    path("registration/", CustomerRegistrationView.as_view(), name="CustomerRegistration"),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='login.html',
        authentication_form=LoginForm)  , name='login'),
        path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='changepassword.html',
        form_class=MyPasswordChangeForm,success_url='/passwordchangedone'),name='changepassword'),
    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'),
         name='passwordchange'),
    path('logout/',auth_view.LogoutView.as_view(next_page='login'),name='logout'),

    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='password_reset.html',
        form_class=MyPasswordResetForm),name='password_reset'),
    path('password-reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='password_reset_done.html')
         ,name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',
        form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
]
