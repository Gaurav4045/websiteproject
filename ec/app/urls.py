from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from.form import LoginForm,MyPasswordResetForm,MyPasswordChangeForm,MySetPasswordForm

urlpatterns = [
    path('', home, name='home'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('adress/', address, name='adress'),
    path('search/', search, name='search'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('category/<slug:val>/', CategoryView.as_view(), name='category'),
    path("category-title/<val>", CategoryTitle.as_view(), name="category-title"),
    path('product-detail/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    path('adressupdate/<int:pk>/', updateAdress.as_view(), name='adressupdate'),


    #login
    path('registration/',CustomerRegistrationView.as_view(),name='customerregistration'),
    #path('accounts-login/',auth_view.LoginView.as_view(template_name='apps/login.html',authentication_form=LoginForm),name='login'),
    #path('password-reset/',auth_view.PasswordResetView.as_view(template_name='apps/password-reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('password-change/',auth_view.PasswordChangeView.as_view(template_name='apps/passwordchange.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone'),name='password_change'),
    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='apps/passwordchangedone.html',),name='passwordchangedone'),
    path('logout/', auth_view.LogoutView.as_view(next_page='/accounts-login/'), name='logout'),
    path('accounts-login/', auth_view.LoginView.as_view(template_name='apps/login.html', authentication_form=LoginForm), name='login'),

    #reset password
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='apps/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='apps/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='apps/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset/complete/', auth_view.PasswordResetCompleteView.as_view(template_name='apps/password_reset_complete.html'), name='password_reset_complete'),

    #shoping
    path('add-to-cart/', add_cart, name='add-to-cart'),
    path('plus-wishlist/', plus_wishlist, name='plus-wishlist'),
    path('show-wishlist/', show_wishlist, name='show-wishlist'),
    path('minus-wishlist/', minus_wishlist, name='minus-wishlist'),
    path('cart/', showcart, name='showcart'),
    path('checkout/', Checkout.as_view(), name='checkout'),  # Replace with the correct view
    path('pluscart/', pluscart, name='pluscart'),
    path('minuscart/', minuscart, name='minuscart'),
    path('removecart/', removecart, name='removecart'),
    path('paymentdone/', PaymentDone.as_view(), name='paymentdone'),
    path('order/', OrderView.as_view(), name='order'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
