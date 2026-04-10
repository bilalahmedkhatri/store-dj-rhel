from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('products/', views.products_view, name='products'),
    path('products/<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('not-found/', views.not_found_view, name='not_found'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/', views.add_to_cart_view, name='cart_add'),
    path('cart/update/<slug:slug>/', views.cart_update_view, name='cart_update'),
    path('cart/remove/<slug:slug>/', views.cart_remove_view, name='cart_remove'),
    path('checkout/', views.checkout_view, name='checkout'),
    
    # categories
    path('categories/', views.category_list, name='category_list'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('category/<int:category_id>/<slug:slug>/', views.category_detail, name='category_detail_slug'),
    path('catalog/', views.all_products, name='all_products'),

    # extra pages
    path('about-us/', views.about_us, name='about_us'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('faqs/', views.faqs, name='faqs'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-and-conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('shipping-policy/', views.shipping_policy, name='shipping_policy'),
    path('return-policy/', views.return_policy, name='return_policy'),
    path('refund-policy/', views.return_policy, name='refund_policy'),
    path('payment-methods/', views.payment_methods, name='payment_methods'),
]
